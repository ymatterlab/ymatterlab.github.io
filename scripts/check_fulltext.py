#!/usr/bin/env python3
"""Audit the free-full-text links in data/publications.yaml.

  python scripts/check_fulltext.py                  # coverage summary
  python scripts/check_fulltext.py --against <rev>  # compare with a git revision
  python scripts/check_fulltext.py --check-links    # HTTP-check every link

--against defaults to the commit before the DOI migration; pass any revision
git understands, e.g. HEAD, HEAD~3, or a commit hash.
"""

from __future__ import annotations

import argparse
import collections
import pathlib
import subprocess
import sys
import urllib.error
import urllib.request

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
CURRENT = ROOT / "data" / "publications.yaml"


def ident(rec: dict) -> str:
    """Match records across revisions: DOI when present, else the key."""
    return (rec.get("doi") or "").lower() or f"key:{rec.get('key', '')}"


def load_current() -> list[dict]:
    return yaml.safe_load(CURRENT.read_text(encoding="utf-8")) or []


def load_revision(rev: str) -> list[dict] | None:
    try:
        blob = subprocess.run(
            ["git", "show", f"{rev}:data/publications.yaml"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout
    except Exception as exc:
        print(f"could not read data/publications.yaml at {rev}: {exc}")
        return None
    return yaml.safe_load(blob) or []


def check_link(url: str, timeout: int = 20) -> str:
    req = urllib.request.Request(url, method="HEAD", headers={
        "User-Agent": "Mozilla/5.0 (compatible; ymatterlab-linkcheck/1.0)"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return f"{resp.status}"
    except urllib.error.HTTPError as exc:
        if exc.code in (403, 405):          # many publishers refuse HEAD
            return f"{exc.code} (likely fine)"
        return f"{exc.code}"
    except Exception as exc:
        return f"error: {type(exc).__name__}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--against", metavar="REV", help="git revision to compare with")
    ap.add_argument("--check-links", action="store_true", help="HTTP-check each link")
    args = ap.parse_args()

    recs = load_current()
    with_ft = [r for r in recs if r.get("free_full_text_url")]
    print(f"{len(recs)} publications, {len(with_ft)} with a free full text link "
          f"({100 * len(with_ft) // max(len(recs), 1)}%)\n")

    sources = collections.Counter(r.get("free_full_text_source", "(none)") for r in with_ft)
    print("by source:")
    for src, n in sources.most_common():
        print(f"  {n:3d}  {src}")

    missing = [r for r in recs if not r.get("free_full_text_url")]
    if missing:
        print(f"\nno free full text ({len(missing)}):")
        for r in sorted(missing, key=lambda r: -r["sort_date"]):
            print(f"  {r['year']}  {r.get('doi', '-'):32s}  {r['title'][:58]}")

    if args.against:
        before = load_revision(args.against)
        if before is not None:
            had = {ident(r): r for r in before if r.get("free_full_text_url")}
            has = {ident(r) for r in with_ft}
            lost = [r for k, r in had.items() if k not in has]
            print(f"\ncompared with {args.against}: {len(had)} had a link, "
                  f"{len(with_ft)} do now")
            if lost:
                print(f"REGRESSIONS -- these lost their link ({len(lost)}):")
                for r in sorted(lost, key=lambda r: -r["sort_date"]):
                    print(f"  {r['year']}  {r.get('doi', '-')}")
                    print(f"        was: {r['free_full_text_url']}")
                print("\nrestore any of these in pubsrc/publications_overrides.yaml:")
                for r in lost[:3]:
                    print(f"  {r.get('doi', 'DOI')}:")
                    print(f"    free_full_text_url: \"{r['free_full_text_url']}\"")
                    print(f"    free_full_text_source: \"{r.get('free_full_text_source', 'arXiv')}\"")
            else:
                print("no regressions.")

    if args.check_links:
        print(f"\nchecking {len(with_ft)} links...")
        bad = []
        for r in with_ft:
            status = check_link(r["free_full_text_url"])
            if not (status.startswith("2") or "likely fine" in status):
                bad.append((r, status))
                print(f"  {status:22s} {r.get('doi', '-')}  {r['free_full_text_url']}")
        print(f"{len(with_ft) - len(bad)}/{len(with_ft)} reachable")
        return 1 if bad else 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
