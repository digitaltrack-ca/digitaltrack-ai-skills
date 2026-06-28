#!/usr/bin/env python3
"""Create a local Google Search Console indexing readiness report.

This script intentionally does not use Google's Indexing API. It validates
URLs, checks sitemap presence, and creates a manual Search Console checklist.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import html
import html.parser
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


WEBMASTERS_SCOPE = "https://www.googleapis.com/auth/webmasters"
WEBMASTERS_READONLY_SCOPE = "https://www.googleapis.com/auth/webmasters.readonly"


class TitleParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._in_title = False
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.parts.append(data)

    @property
    def title(self) -> str:
        return " ".join(" ".join(self.parts).split())


def fetch(url: str, timeout: int = 20) -> tuple[int | None, str, str, bytes, str | None]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "DigitalTrack-GSC-Indexing-Workflow/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read(500_000)
            return (
                response.status,
                response.geturl(),
                response.headers.get("content-type", ""),
                body,
                None,
            )
    except urllib.error.HTTPError as exc:
        body = exc.read(100_000)
        return exc.code, exc.geturl(), exc.headers.get("content-type", ""), body, None
    except Exception as exc:  # noqa: BLE001 - report the failure in CSV/Markdown.
        return None, url, "", b"", f"{type(exc).__name__}: {exc}"


def google_api_request(
    method: str,
    url: str,
    token: str,
    payload: dict[str, object] | None = None,
    timeout: int = 30,
) -> tuple[int | None, dict[str, object] | None, str | None]:
    data = None
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace").strip()
            return response.status, json.loads(body) if body else {}, None
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace").strip()
        return exc.code, None, body or str(exc)
    except Exception as exc:  # noqa: BLE001 - report the API failure.
        return None, None, f"{type(exc).__name__}: {exc}"


def get_access_token(args: argparse.Namespace, readonly: bool = False) -> tuple[str | None, str | None]:
    if args.access_token:
        return args.access_token, None

    env_token = os.environ.get("GSC_ACCESS_TOKEN")
    if env_token:
        return env_token, None

    if not args.credentials:
        return None, "No API token provided. Use --access-token, GSC_ACCESS_TOKEN, or --credentials with a service account JSON."

    credentials_path = Path(args.credentials)
    try:
        credential_info = json.loads(credentials_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - keep the message actionable.
        return None, f"Could not read credentials JSON: {type(exc).__name__}: {exc}"

    if credential_info.get("type") != "service_account":
        return None, (
            "Credentials file is not a service account JSON. "
            "For OAuth client JSON, get a bearer token separately and pass --access-token or set GSC_ACCESS_TOKEN."
        )

    try:
        from google.auth.transport.requests import Request  # type: ignore
        from google.oauth2 import service_account  # type: ignore
    except ImportError:
        return None, "Service account JSON requires the optional google-auth package. Install google-auth or pass --access-token."

    scopes = [WEBMASTERS_READONLY_SCOPE if readonly else WEBMASTERS_SCOPE]
    try:
        credentials = service_account.Credentials.from_service_account_file(str(credentials_path), scopes=scopes)
        credentials.refresh(Request())
    except Exception as exc:  # noqa: BLE001
        return None, f"Could not refresh service account credentials: {type(exc).__name__}: {exc}"

    return credentials.token, None


def read_urls(path: Path) -> list[str]:
    urls: list[str] = []
    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if " #" in line:
            line = line.split(" #", 1)[0].strip()
        urls.append(line)
    return urls


def extract_sitemap_urls(body: bytes) -> set[str]:
    text = body.decode("utf-8-sig", errors="replace")
    return {match.strip() for match in re.findall(r"<loc>\s*(.*?)\s*</loc>", text, re.I | re.S)}


def normalize_for_compare(url: str) -> str:
    parsed = urllib.parse.urlsplit(url.strip())
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    path = parsed.path.rstrip("/") or "/"
    return urllib.parse.urlunsplit((scheme, netloc, path, "", ""))


def page_title(body: bytes, content_type: str) -> str:
    if "html" not in content_type.lower() and b"<html" not in body[:5000].lower():
        return ""
    parser = TitleParser()
    try:
        parser.feed(body.decode("utf-8", errors="replace"))
    except Exception:
        return ""
    return parser.title


def meta_description(body: bytes, content_type: str) -> str:
    if "html" not in content_type.lower() and b"<html" not in body[:5000].lower():
        return ""
    text = body.decode("utf-8", errors="replace")
    match = re.search(
        r'<meta\s+[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']',
        text,
        flags=re.I | re.S,
    )
    if not match:
        match = re.search(
            r'<meta\s+[^>]*content=["\']([^"\']*)["\'][^>]*name=["\']description["\']',
            text,
            flags=re.I | re.S,
        )
    return " ".join(html.unescape(match.group(1)).split()) if match else ""


def same_site(url: str, site: str) -> bool:
    return urllib.parse.urlsplit(url).netloc.lower() == urllib.parse.urlsplit(site).netloc.lower()


def action_for(row: dict[str, str]) -> str:
    if row["error"]:
        return "Fix live URL error before GSC request"
    if row["http_status"] != "200":
        return "Fix non-200 status before GSC request"
    if row["same_site"] != "yes":
        return "Fix wrong-domain final URL"
    if row["looks_html"] != "yes":
        return "Confirm page is HTML/indexable before GSC request"
    if row["in_sitemap"] != "yes":
        return "Add final URL to sitemap, then resubmit sitemap"
    if row["redirected"] == "yes":
        return "Use final canonical URL for GSC inspection"
    return "Ready for manual URL Inspection and request indexing"


def inspect_url(url: str, site: str, sitemap_urls: set[str]) -> dict[str, str]:
    status, final_url, content_type, body, error = fetch(url)
    final_norm = normalize_for_compare(final_url)
    sitemap_norms = {normalize_for_compare(item) for item in sitemap_urls}
    parsed = urllib.parse.urlsplit(url)
    notes: list[str] = []

    if parsed.scheme != "https":
        notes.append("Input URL is not HTTPS.")
    if parsed.netloc.lower().startswith("www."):
        notes.append("Input URL uses www; confirm canonical preference.")
    if parsed.query:
        notes.append("Input URL has query parameters.")

    row = {
        "url": url,
        "final_url": final_url,
        "http_status": "" if status is None else str(status),
        "redirected": "yes" if normalize_for_compare(url) != final_norm else "no",
        "same_site": "yes" if same_site(final_url, site) else "no",
        "in_sitemap": "yes" if final_norm in sitemap_norms else "no",
        "looks_html": "yes" if ("html" in content_type.lower() or b"<html" in body[:5000].lower()) else "no",
        "title": page_title(body, content_type),
        "meta_description": meta_description(body, content_type),
        "error": error or "",
        "recommended_action": "",
        "notes": " ".join(notes),
        "gsc_inspection_verdict": "",
        "gsc_coverage_state": "",
        "gsc_indexing_state": "",
        "gsc_last_crawl_time": "",
        "gsc_google_canonical": "",
        "gsc_user_canonical": "",
        "gsc_api_error": "",
    }
    row["recommended_action"] = action_for(row)
    return row


def submit_sitemap(site: str, sitemap: str, token: str) -> str:
    site_url = urllib.parse.quote(site, safe="")
    feedpath = urllib.parse.quote(sitemap, safe="")
    endpoint = f"https://www.googleapis.com/webmasters/v3/sites/{site_url}/sitemaps/{feedpath}"
    status, _body, error = google_api_request("PUT", endpoint, token)
    if 200 <= (status or 0) < 300:
        return f"Sitemap submitted successfully: {sitemap}"
    return f"Sitemap submission failed ({status or 'no status'}): {error or 'unknown error'}"


def add_gsc_inspection(row: dict[str, str], site: str, token: str, language_code: str) -> None:
    payload = {
        "inspectionUrl": row["final_url"] or row["url"],
        "siteUrl": site,
        "languageCode": language_code,
    }
    status, body, error = google_api_request(
        "POST",
        "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect",
        token,
        payload,
    )
    if error or not body:
        row["gsc_api_error"] = f"{status or 'no status'}: {error or 'empty response'}"
        return

    inspection_result = body.get("inspectionResult", {})
    if not isinstance(inspection_result, dict):
        row["gsc_api_error"] = "Unexpected URL Inspection API response shape."
        return

    index_status = inspection_result.get("indexStatusResult", {})
    if not isinstance(index_status, dict):
        row["gsc_api_error"] = "URL Inspection response did not include indexStatusResult."
        return

    row["gsc_inspection_verdict"] = str(index_status.get("verdict", ""))
    row["gsc_coverage_state"] = str(index_status.get("coverageState", ""))
    row["gsc_indexing_state"] = str(index_status.get("indexingState", ""))
    row["gsc_last_crawl_time"] = str(index_status.get("lastCrawlTime", ""))
    row["gsc_google_canonical"] = str(index_status.get("googleCanonical", ""))
    row["gsc_user_canonical"] = str(index_status.get("userCanonical", ""))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fields = [
        "url",
        "final_url",
        "http_status",
        "redirected",
        "same_site",
        "in_sitemap",
        "looks_html",
        "title",
        "meta_description",
        "recommended_action",
        "gsc_inspection_verdict",
        "gsc_coverage_state",
        "gsc_indexing_state",
        "gsc_last_crawl_time",
        "gsc_google_canonical",
        "gsc_user_canonical",
        "gsc_api_error",
        "notes",
        "error",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, str]], site: str, sitemap: str, api_messages: list[str]) -> None:
    groups: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        groups.setdefault(row["recommended_action"], []).append(row)

    lines = [
        "# GSC Indexing Checklist",
        "",
        f"Date: {dt.date.today().isoformat()}",
        "",
        f"Search Console property: `{site}`",
        f"Sitemap: `{sitemap}`",
        "",
        "Use this report to decide which URLs are ready for manual Google Search Console URL Inspection and request indexing.",
        "",
    ]
    if api_messages:
        lines.extend(["## API Notes", ""])
        for message in api_messages:
            lines.append(f"- {message}")
        lines.append("")

    for action in sorted(groups):
        lines.extend([f"## {action}", ""])
        for row in groups[action]:
            details = [
                f"status {row['http_status'] or 'n/a'}",
                f"sitemap {row['in_sitemap']}",
                f"redirected {row['redirected']}",
            ]
            if row["title"]:
                details.append(f"title: {row['title']}")
            if row["meta_description"]:
                details.append(f"meta: {row['meta_description']}")
            if row["gsc_inspection_verdict"]:
                details.append(f"GSC verdict: {row['gsc_inspection_verdict']}")
            if row["gsc_coverage_state"]:
                details.append(f"GSC coverage: {row['gsc_coverage_state']}")
            if row["gsc_last_crawl_time"]:
                details.append(f"GSC last crawl: {row['gsc_last_crawl_time']}")
            if row["gsc_api_error"]:
                details.append(f"GSC API error: {row['gsc_api_error']}")
            if row["notes"]:
                details.append(f"notes: {row['notes']}")
            if row["error"]:
                details.append(f"error: {row['error']}")
            lines.append(f"- `{row['url']}` -> `{row['final_url']}` ({'; '.join(details)})")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def timestamped_path(path: Path) -> Path:
    stamp = dt.datetime.now().strftime("%H%M%S")
    return path.with_name(f"{path.stem}-{stamp}{path.suffix}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--urls", required=True, type=Path, help="Newline-separated URL list.")
    parser.add_argument("--site", required=True, help="Search Console site property.")
    parser.add_argument("--sitemap", required=True, help="Live sitemap URL.")
    parser.add_argument("--output-dir", default=".", type=Path, help="Report output directory.")
    parser.add_argument("--submit-sitemap", action="store_true", help="Submit the sitemap through the official Search Console API.")
    parser.add_argument("--inspect-index", action="store_true", help="Use the official URL Inspection API to add indexed-status fields.")
    parser.add_argument("--credentials", type=Path, help="Optional service account JSON. The account must have access to the Search Console property.")
    parser.add_argument("--access-token", help="Optional OAuth bearer token. Can also be supplied via GSC_ACCESS_TOKEN.")
    parser.add_argument("--language-code", default="en-US", help="Language code for URL Inspection API messages. Default: en-US.")
    args = parser.parse_args(argv)

    urls = read_urls(args.urls)
    if not urls:
        print(f"No URLs found in {args.urls}", file=sys.stderr)
        return 2

    sitemap_status, sitemap_final, _content_type, sitemap_body, sitemap_error = fetch(args.sitemap)
    if sitemap_error or sitemap_status != 200:
        print(f"Could not fetch sitemap {args.sitemap}: {sitemap_error or sitemap_status}", file=sys.stderr)
        return 2

    sitemap_urls = extract_sitemap_urls(sitemap_body)
    if not sitemap_urls:
        print(f"No <loc> URLs found in sitemap {sitemap_final}", file=sys.stderr)
        return 2

    rows = [inspect_url(url, args.site, sitemap_urls) for url in urls]

    api_messages: list[str] = []
    if args.submit_sitemap or args.inspect_index:
        token, token_error = get_access_token(args, readonly=not args.submit_sitemap)
        if token_error or not token:
            api_messages.append(f"Skipped Search Console API actions: {token_error or 'no token available'}")
        else:
            if args.submit_sitemap:
                api_messages.append(submit_sitemap(args.site, args.sitemap, token))
            if args.inspect_index:
                for row in rows:
                    add_gsc_inspection(row, args.site, token, args.language_code)
                api_messages.append("URL Inspection API check completed for report rows.")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    today = dt.date.today().isoformat()
    csv_path = args.output_dir / f"gsc-indexing-report-{today}.csv"
    md_path = args.output_dir / f"gsc-indexing-checklist-{today}.md"
    try:
        write_csv(csv_path, rows)
    except PermissionError:
        csv_path = timestamped_path(csv_path)
        write_csv(csv_path, rows)

    try:
        write_markdown(md_path, rows, args.site, args.sitemap, api_messages)
    except PermissionError:
        md_path = timestamped_path(md_path)
        write_markdown(md_path, rows, args.site, args.sitemap, api_messages)

    print(f"Wrote {csv_path}")
    print(f"Wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
