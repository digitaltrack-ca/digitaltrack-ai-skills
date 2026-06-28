#!/usr/bin/env python3
"""
IndexNow URL Submission Tool — DigitalTrack WAT Skill
Submit URLs to Bing/IndexNow for fast crawl prioritization.

Usage:
  python indexnow_submit.py setup  --domain sabormexkitchen.com
  python indexnow_submit.py submit --domain sabormexkitchen.com
  python indexnow_submit.py submit --domain sabormexkitchen.com --url https://sabormexkitchen.com/menu
  python indexnow_submit.py list
"""

import sys
import json
import uuid
import argparse
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from pathlib import Path

CONFIG_FILE = Path(__file__).parent.parent / "config" / "keys.json"
INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"

STATUS_MESSAGES = {
    200: "OK — URLs submitted successfully",
    202: "Accepted — key validation pending (normal on first submission)",
    400: "Bad Request — check URL format or JSON payload",
    403: "Forbidden — key file not found or key mismatch. Host the key .txt file first.",
    422: "Unprocessable Entity — URLs don't match host or key schema mismatch",
    429: "Too Many Requests — wait and retry",
}


def load_config():
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    return {}


def save_config(cfg):
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2), encoding="utf-8")


def _clean_domain(raw):
    if "://" in raw:
        raw = raw.split("://", 1)[1]
    return raw.rstrip("/").split("/")[0]


def cmd_setup(args):
    domain = _clean_domain(args.domain)
    cfg = load_config()

    if domain in cfg:
        key = cfg[domain]["key"]
        print(f"[already configured] {domain}")
    else:
        key = uuid.uuid4().hex  # 32 hex chars — meets IndexNow 8-128 char requirement
        cfg[domain] = {"key": key}
        save_config(cfg)
        print(f"[key generated] {domain}")

    key_file = f"{key}.txt"
    key_url = f"https://{domain}/{key_file}"

    print(f"\n  Key:      {key}")
    print(f"  Key URL:  {key_url}")
    print()
    print("ACTION REQUIRED — host the key file at the root of the domain:")
    print(f"  File name:    {key_file}")
    print(f"  File content: {key}  (plain text, UTF-8, no trailing newline)")
    print(f"  Public URL:   {key_url}")
    print()
    print("Platform instructions:")
    print("  Lovable:    Run /lovable and send:")
    print(f'    "Add a static file at the site root: /{key_file}')
    print(f'     The file must return plain text: {key}')
    print(f'     No HTML wrapping — raw text only."')
    print()
    print("  Builderall: Upload the .txt file to the root public folder via File Manager.")
    print()
    print("After hosting the file, verify it's live:")
    print(f"  curl {key_url}")
    print()
    print("Then submit:")
    print(f"  python indexnow_submit.py submit --domain {domain}")


def fetch_sitemap_urls(sitemap_url):
    req = urllib.request.Request(
        sitemap_url,
        headers={"User-Agent": "IndexNow-DigitalTrack/1.0"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        xml_data = resp.read()

    root = ET.fromstring(xml_data)

    # Handle sitemap index (nested sitemaps)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    nested = root.findall(".//sm:sitemap/sm:loc", ns)
    if nested:
        all_urls = []
        for loc in nested:
            all_urls.extend(fetch_sitemap_urls(loc.text.strip()))
        return all_urls

    return [loc.text.strip() for loc in root.findall(".//sm:loc", ns) if loc.text]


def submit_urls(domain, urls, key):
    key_location = f"https://{domain}/{key}.txt"
    payload = {
        "host": domain,
        "key": key,
        "keyLocation": key_location,
        "urlList": urls,
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        INDEXNOW_ENDPOINT,
        data=data,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "IndexNow-DigitalTrack/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        return e.code


def cmd_submit(args):
    domain = _clean_domain(args.domain)
    cfg = load_config()

    if domain not in cfg:
        print(f"[error] {domain} not configured.")
        print(f"  Run: python indexnow_submit.py setup --domain {domain}")
        sys.exit(1)

    key = cfg[domain]["key"]

    if args.url:
        urls = [args.url]
        print(f"Submitting 1 URL for {domain} ...")
    else:
        sitemap = args.sitemap or f"https://{domain}/sitemap.xml"
        print(f"Fetching sitemap: {sitemap}")
        try:
            urls = fetch_sitemap_urls(sitemap)
        except Exception as e:
            print(f"[error] Could not fetch sitemap: {e}")
            sys.exit(1)
        print(f"Found {len(urls)} URLs")

    # IndexNow allows up to 10,000 URLs per POST; chunk if needed
    chunk_size = 10000
    chunks = [urls[i:i + chunk_size] for i in range(0, len(urls), chunk_size)]

    for i, chunk in enumerate(chunks, 1):
        if len(chunks) > 1:
            print(f"Submitting batch {i}/{len(chunks)} ({len(chunk)} URLs)...")
        status = submit_urls(domain, chunk, key)
        msg = STATUS_MESSAGES.get(status, f"HTTP {status}")
        print(f"Response: {status} — {msg}")

        if status in (200, 202):
            print(f"[success] {len(chunk)} URLs submitted")
            for url in chunk[:5]:
                print(f"  {url}")
            if len(chunk) > 5:
                print(f"  ... and {len(chunk) - 5} more")
        else:
            print("[failed] Check the error above. Common fix: verify the key file is live.")
            if status == 403:
                print(f"  Expected at: https://{domain}/{key}.txt")
                print(f"  Run setup for instructions: python indexnow_submit.py setup --domain {domain}")
            sys.exit(1)


def cmd_list(args):
    cfg = load_config()
    if not cfg:
        print("No domains configured. Run: python indexnow_submit.py setup --domain <domain>")
        return
    print(f"\n{'Domain':<45} Key")
    print("-" * 80)
    for domain, data in cfg.items():
        print(f"{domain:<45} {data['key']}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="IndexNow URL submission tool — DigitalTrack WAT Skill",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd")

    p_setup = sub.add_parser("setup", help="Generate key for a domain and show hosting instructions")
    p_setup.add_argument("--domain", required=True, help="Domain (e.g. sabormexkitchen.com)")

    p_submit = sub.add_parser("submit", help="Submit URLs from sitemap or a single URL")
    p_submit.add_argument("--domain", required=True, help="Domain (e.g. sabormexkitchen.com)")
    p_submit.add_argument("--sitemap", help="Sitemap URL override (default: https://<domain>/sitemap.xml)")
    p_submit.add_argument("--url", help="Submit a single URL instead of full sitemap")

    sub.add_parser("list", help="List all configured domains and keys")

    args = parser.parse_args()

    if args.cmd == "setup":
        cmd_setup(args)
    elif args.cmd == "submit":
        cmd_submit(args)
    elif args.cmd == "list":
        cmd_list(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
