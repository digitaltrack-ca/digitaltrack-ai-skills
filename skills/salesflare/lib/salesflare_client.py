#!/usr/bin/env python3
"""Import lead rows from CSV into Salesflare.

The script intentionally depends only on Python's standard library. It performs
read-only lookups during dry runs and only writes to Salesflare when --commit is
passed.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from datetime import date, datetime, time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen


API_BASE = "https://api.salesflare.com"
LOCAL_TZ = datetime.now().astimezone().tzinfo

LEAD_COLUMNS = [
    "company_name",
    "domain",
    "website",
    "contact_first",
    "contact_last",
    "contact_name",
    "email",
    "phone",
    "title",
    "linkedin",
    "lead_source",
    "tags",
    "opportunity_name",
    "opportunity_value",
    "stage",
    "next_task_due",
    "next_task",
    "note",
]

IMPORT_COLUMNS = LEAD_COLUMNS + [
    "import_status",
    "imported_at",
    "salesflare_account_id",
    "salesflare_contact_id",
    "salesflare_opportunity_id",
    "salesflare_task_id",
    "salesflare_note_id",
    "import_message",
]


class SalesflareError(RuntimeError):
    pass


def get_salesflare_api_key() -> str:
    api_key = os.environ.get("SALESFLARE_API_KEY", "").strip()
    if api_key:
        return api_key

    if sys.platform != "win32":
        return ""

    try:
        import winreg

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
            value, _ = winreg.QueryValueEx(key, "SALESFLARE_API_KEY")
            return str(value).strip()
    except OSError:
        return ""


def clean(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def compact_payload(payload: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in payload.items():
        if value is None or value == "":
            continue
        if isinstance(value, (list, dict)) and not value:
            continue
        result[key] = value
    return result


def parse_tags(value: str) -> list[str]:
    value = clean(value)
    if not value:
        return []
    separator = ";" if ";" in value else ","
    return [part.strip() for part in value.split(separator) if part.strip()]


def parse_money(value: str) -> float | None:
    value = clean(value)
    if not value:
        return None
    normalized = re.sub(r"[$,\s]", "", value)
    try:
        return float(normalized)
    except ValueError as exc:
        raise SalesflareError(f"Invalid opportunity_value: {value}") from exc


def normalize_domain(domain: str, website: str, email: str) -> str:
    domain = clean(domain).lower()
    if domain:
        return domain.removeprefix("www.")

    website = clean(website)
    if website:
        parsed = urlparse(website if "://" in website else f"https://{website}")
        if parsed.netloc:
            return parsed.netloc.lower().removeprefix("www.")

    email = clean(email)
    if "@" in email:
        return email.rsplit("@", 1)[1].lower()

    return ""


def normalize_website(website: str, domain: str) -> str:
    website = clean(website)
    if website:
        return website if "://" in website else f"https://{website}"
    domain = clean(domain)
    return f"https://{domain}" if domain else ""


def normalize_due_date(value: str) -> str:
    value = clean(value)
    if not value:
        return ""
    try:
        due_date = date.fromisoformat(value)
    except ValueError:
        return value
    due_at = datetime.combine(due_date, time(hour=9), tzinfo=LOCAL_TZ)
    return due_at.isoformat()


def normalize_row(row: dict[str, str]) -> dict[str, str]:
    normalized = {column: clean(row.get(column, "")) for column in LEAD_COLUMNS}
    normalized["domain"] = normalize_domain(
        normalized["domain"], normalized["website"], normalized["email"]
    )
    normalized["website"] = normalize_website(normalized["website"], normalized["domain"])
    if not normalized["contact_name"]:
        normalized["contact_name"] = " ".join(
            part for part in [normalized["contact_first"], normalized["contact_last"]] if part
        )
    return normalized


def is_blank_row(row: dict[str, str]) -> bool:
    return not any(clean(row.get(column, "")) for column in LEAD_COLUMNS)


def row_label(row: dict[str, str]) -> str:
    return (
        row.get("contact_name")
        or row.get("email")
        or row.get("company_name")
        or row.get("domain")
        or "unnamed row"
    )


class SalesflareClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._stages: list[dict[str, Any]] | None = None

    def request(
        self,
        method: str,
        path: str,
        query: dict[str, Any] | None = None,
        payload: dict[str, Any] | None = None,
    ) -> Any:
        url = f"{API_BASE}{path}"
        if query:
            query = {key: value for key, value in query.items() if value not in (None, "", [])}
            if query:
                url = f"{url}?{urlencode(query, doseq=True)}"

        body = None
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }
        if payload is not None:
            body = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"

        request = Request(url, data=body, headers=headers, method=method.upper())
        try:
            with urlopen(request, timeout=30) as response:
                raw = response.read().decode("utf-8")
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise SalesflareError(f"{method.upper()} {path} failed: {exc.code} {detail}") from exc

        if not raw:
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return raw

    @staticmethod
    def records(response: Any) -> list[dict[str, Any]]:
        if isinstance(response, list):
            return [item for item in response if isinstance(item, dict)]
        if isinstance(response, dict):
            for key in ("data", "items", "results"):
                value = response.get(key)
                if isinstance(value, list):
                    return [item for item in value if isinstance(item, dict)]
            return [response] if response.get("id") else []
        return []

    @staticmethod
    def record_id(response: Any) -> str:
        if isinstance(response, list):
            for item in response:
                if isinstance(item, dict) and item.get("id") is not None:
                    return str(item["id"])
        if isinstance(response, dict):
            value = response.get("id")
            return str(value) if value is not None else ""
        return ""

    def first_record(self, path: str, query: dict[str, Any]) -> dict[str, Any] | None:
        response = self.request("GET", path, query=query)
        records = self.records(response)
        return records[0] if records else None

    def find_account(self, row: dict[str, str]) -> dict[str, Any] | None:
        if row["domain"]:
            record = self.first_record("/accounts", {"domain": [row["domain"]], "limit": 1})
            if record:
                return record
        if row["company_name"]:
            return self.first_record("/accounts", {"search": row["company_name"], "limit": 1})
        return None

    def find_contact(self, row: dict[str, str]) -> dict[str, Any] | None:
        if row["email"]:
            record = self.first_record("/contacts", {"email": row["email"], "limit": 1})
            if record:
                return record
        if row["contact_name"]:
            return self.first_record("/contacts", {"name": row["contact_name"], "limit": 1})
        return None

    def find_opportunity(self, account_id: str, name: str) -> dict[str, Any] | None:
        if not account_id or not name:
            return None
        return self.first_record(
            "/opportunities",
            {"account": account_id, "name": name, "limit": 1, "details": True},
        )

    def resolve_stage_id(self, stage: str) -> int | None:
        stage = clean(stage)
        if not stage:
            return None
        if stage.isdigit():
            return int(stage)
        if self._stages is None:
            self._stages = self.records(self.request("GET", "/stages"))
        for item in self._stages:
            if clean(item.get("name")).lower() == stage.lower():
                return int(item["id"])
        raise SalesflareError(f"Could not find Salesflare stage named: {stage}")


def account_payload(row: dict[str, str]) -> dict[str, Any]:
    return compact_payload(
        {
            "name": row["company_name"],
            "domain": row["domain"],
            "website": row["website"],
            "tags": parse_tags(row["tags"]),
        }
    )


def contact_payload(row: dict[str, str], account_id: str) -> dict[str, Any]:
    social_profiles: list[Any] = []
    if row["linkedin"]:
        social_profiles.append({"type": "linkedin", "url": row["linkedin"]})

    return compact_payload(
        {
            "email": row["email"],
            "firstname": row["contact_first"],
            "lastname": row["contact_last"],
            "name": row["contact_name"],
            "phone_number": row["phone"],
            "account": int(account_id) if account_id else None,
            "position": compact_payload(
                {"role": row["title"], "organisation": row["company_name"]}
            ),
            "social_profiles": social_profiles,
            "tags": parse_tags(row["tags"]),
        }
    )


def opportunity_payload(
    client: SalesflareClient, row: dict[str, str], account_id: str, contact_id: str
) -> dict[str, Any]:
    return compact_payload(
        {
            "account": int(account_id),
            "name": row["opportunity_name"],
            "value": parse_money(row["opportunity_value"]),
            "stage": client.resolve_stage_id(row["stage"]),
            "main_contact": int(contact_id) if contact_id else None,
            "tags": parse_tags(row["tags"]),
        }
    )


def task_payload(row: dict[str, str], account_id: str) -> dict[str, Any]:
    return compact_payload(
        {
            "account": int(account_id) if account_id else None,
            "description": row["next_task"],
            "reminder_date": normalize_due_date(row["next_task_due"]),
        }
    )


def note_payload(row: dict[str, str], account_id: str, imported_at: str) -> dict[str, Any]:
    lines = [f"Imported to Salesflare from CSV at {imported_at}."]
    if row["lead_source"]:
        lines.append(f"Lead source: {row['lead_source']}")
    if row["next_task"]:
        lines.append(f"Next task: {row['next_task']}")
    if row["note"]:
        lines.append("")
        lines.append(row["note"])

    return {
        "account": int(account_id),
        "body": "\n".join(lines),
        "date": imported_at,
    }


def validate_row(row: dict[str, str]) -> None:
    if not row["company_name"] and not row["domain"]:
        raise SalesflareError("Missing company_name or domain.")
    if not row["email"] and not row["contact_name"]:
        raise SalesflareError("Missing email or contact_name.")


def import_row(client: SalesflareClient, row: dict[str, str], commit: bool) -> dict[str, str]:
    validate_row(row)
    imported_at = datetime.now(LOCAL_TZ).isoformat(timespec="seconds")
    messages: list[str] = []
    ids = {
        "salesflare_account_id": "",
        "salesflare_contact_id": "",
        "salesflare_opportunity_id": "",
        "salesflare_task_id": "",
        "salesflare_note_id": "",
    }

    existing_account = client.find_account(row)
    payload = account_payload(row)
    if existing_account:
        account_id = str(existing_account["id"])
        ids["salesflare_account_id"] = account_id
        messages.append(f"update account {account_id}")
        if commit:
            client.request("PUT", f"/accounts/{account_id}", payload=payload)
    else:
        messages.append("create account")
        if commit:
            created = client.request(
                "POST", "/accounts", query={"update_if_exists": "true"}, payload=payload
            )
            ids["salesflare_account_id"] = client.record_id(created)

    account_id = ids["salesflare_account_id"]
    if not account_id and not commit:
        account_id = "0"
    if not account_id:
        raise SalesflareError("Salesflare did not return an account ID.")

    existing_contact = client.find_contact(row)
    payload = contact_payload(row, account_id)
    if existing_contact:
        contact_id = str(existing_contact["id"])
        ids["salesflare_contact_id"] = contact_id
        messages.append(f"update contact {contact_id}")
        if commit:
            client.request("PUT", f"/contacts/{contact_id}", payload=payload)
    else:
        messages.append("create contact")
        if commit:
            created = client.request("POST", "/contacts", query={"force": "true"}, payload=payload)
            ids["salesflare_contact_id"] = client.record_id(created)

    contact_id = ids["salesflare_contact_id"]
    if not contact_id and not commit:
        contact_id = "0"

    if row["opportunity_name"]:
        existing_opportunity = None if not commit else client.find_opportunity(account_id, row["opportunity_name"])
        payload = opportunity_payload(client, row, account_id, contact_id)
        if existing_opportunity:
            opportunity_id = str(existing_opportunity["id"])
            ids["salesflare_opportunity_id"] = opportunity_id
            messages.append(f"update opportunity {opportunity_id}")
            if commit:
                client.request("PUT", f"/opportunities/{opportunity_id}", payload=payload)
        else:
            messages.append("create opportunity")
            if commit:
                created = client.request("POST", "/opportunities", payload=payload)
                ids["salesflare_opportunity_id"] = client.record_id(created)

    if row["next_task"]:
        messages.append("create follow-up task")
        if commit:
            created = client.request("POST", "/tasks", payload=task_payload(row, account_id))
            ids["salesflare_task_id"] = client.record_id(created)

    if row["note"] or row["lead_source"]:
        messages.append("create internal note")
        if commit:
            created = client.request(
                "POST", "/messages", payload=note_payload(row, account_id, imported_at)
            )
            ids["salesflare_note_id"] = client.record_id(created)

    return {
        **row,
        "import_status": "imported" if commit else "dry-run",
        "imported_at": imported_at if commit else "",
        **ids,
        "import_message": "; ".join(messages),
    }


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SalesflareError(f"Input file does not exist: {path}")
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = [column for column in LEAD_COLUMNS if column not in (reader.fieldnames or [])]
        if missing:
            raise SalesflareError(f"Input file is missing columns: {', '.join(missing)}")
        return [normalize_row(row) for row in reader if not is_blank_row(row)]


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def append_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    exists = path.exists() and path.stat().st_size > 0
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        if not exists:
            writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Import lead rows into Salesflare.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Preview actions without writing.")
    mode.add_argument("--commit", action="store_true", help="Write to Salesflare and move rows.")
    parser.add_argument("--input", default="salesflare_leads_to_import.csv")
    parser.add_argument("--imported", default="salesflare_leads_imported.csv")
    parser.add_argument("--limit", type=int, default=0, help="Process only the first N rows.")
    args = parser.parse_args()

    commit = args.commit
    api_key = get_salesflare_api_key()
    if not api_key:
        print("Set SALESFLARE_API_KEY before running this script.", file=sys.stderr)
        return 2

    input_path = Path(args.input)
    imported_path = Path(args.imported)
    client = SalesflareClient(api_key)

    try:
        rows = read_rows(input_path)
        if args.limit:
            rows = rows[: args.limit]
    except SalesflareError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if not rows:
        print(f"No leads found in {input_path}.")
        return 0

    imported_rows: list[dict[str, str]] = []
    remaining_rows: list[dict[str, str]] = []
    failures = 0

    for index, row in enumerate(rows, start=1):
        label = row_label(row)
        try:
            result = import_row(client, row, commit)
            imported_rows.append(result)
            print(f"[{index}] {label}: {result['import_message']}")
        except SalesflareError as exc:
            failures += 1
            remaining_rows.append(row)
            print(f"[{index}] {label}: ERROR: {exc}", file=sys.stderr)

    if commit:
        if imported_rows:
            append_rows(imported_path, IMPORT_COLUMNS, imported_rows)
        untouched_rows = read_rows(input_path)
        processed_keys = {
            tuple(row.get(column, "") for column in LEAD_COLUMNS) for row in imported_rows
        }
        unprocessed_rows = [
            row
            for row in untouched_rows
            if tuple(row.get(column, "") for column in LEAD_COLUMNS) not in processed_keys
        ]
        write_rows(input_path, LEAD_COLUMNS, unprocessed_rows)
        print(f"Committed {len(imported_rows)} row(s). Failed rows remain in {input_path}.")
    else:
        print("Dry run only. No Salesflare records or CSV files were changed.")

    if failures:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
