#!/usr/bin/env python3
"""Build data/publications.yaml from a plain list of DOIs.

Metadata comes from Crossref, open-access links from Unpaywall, and every
answer is cached in pubsrc/pubcache.json (committed) so the site builds even
if the APIs are slow or offline.

Inputs
------
pubsrc/publications.dois.txt      one DOI per line; '#' starts a comment
pubsrc/publications_extra.yaml    full manual records for items with no DOI
pubsrc/publications_overrides.yaml  per-DOI field overrides, e.g.
    10.1038/s41567-024-00001-2:
      free_full_text_url: "https://arxiv.org/pdf/2401.00001"
      hide: true          # keep out of the website

Usage
-----
python scripts/build_pubs.py              # only fetch DOIs not yet cached
python scripts/build_pubs.py --refresh     # re-fetch everything
python scripts/build_pubs.py --offline     # cache only, never touch network
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
# Inputs live outside data/ because Hugo tries to parse every file in data/
# as a data file, and a .txt list is not a format it understands.
SRC = ROOT / "pubsrc"
DOIS = SRC / "publications.dois.txt"
EXTRA = SRC / "publications_extra.yaml"
OVERRIDES = SRC / "publications_overrides.yaml"
CACHE = SRC / "pubcache.json"
OUT = ROOT / "data" / "publications.yaml"

# Crossref and Unpaywall both ask for a contact address; it buys faster,
# more reliable service and is not used for anything else.
EMAIL = "yuewen.fang@csic.es"
UA = f"ymatterlab-site/1.0 (https://ymatterlab.github.io; mailto:{EMAIL})"

MONTH_NAMES = {1: "jan", 2: "feb", 3: "mar", 4: "apr", 5: "may", 6: "jun",
               7: "jul", 8: "aug", 9: "sep", 10: "oct", 11: "nov", 12: "dec"}

# Names to force into their canonical spelling.
NAME_FIXES = {
    "Yue Wen Fang": "Yue-Wen Fang",
    "Yuewen Fang": "Yue-Wen Fang",
}


def log(msg: str) -> None:
    sys.stderr.write(msg + "\n")


def get_json(url: str, tries: int = 3) -> dict | None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code in (404, 422):
                return None
            if attempt == tries - 1:
                raise
        except Exception:
            if attempt == tries - 1:
                raise
        time.sleep(2 * (attempt + 1))
    return None


def strip_tags(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text or "")
    return re.sub(r"\s+", " ", text).strip()


def slug_key(record: dict) -> str:
    first = (record.get("authors", "").split(",")[0] or "anon").split()[-1]
    word = next((w for w in re.findall(r"[A-Za-z]+", record.get("title", "")) if len(w) > 3), "paper")
    return f"{first}_{word}_{record.get('year', '')}".lower()


def from_crossref(doi: str) -> dict | None:
    data = get_json(f"https://api.crossref.org/works/{urllib.parse.quote(doi)}?mailto={EMAIL}")
    if not data:
        return None
    m = data["message"]

    title = strip_tags((m.get("title") or [""])[0])
    if m.get("subtitle") and strip_tags(m["subtitle"][0]) not in title:
        title = f"{title}: {strip_tags(m['subtitle'][0])}"

    authors = []
    for a in m.get("author", []):
        if a.get("name"):
            name = a["name"]
        else:
            name = f"{a.get('given', '')} {a.get('family', '')}".strip()
        name = re.sub(r"\s+", " ", name)
        authors.append(NAME_FIXES.get(name, name))

    date = (m.get("published") or m.get("published-print") or m.get("published-online")
            or m.get("issued") or {})
    parts = (date.get("date-parts") or [[]])[0]
    year = str(parts[0]) if parts else ""
    month = int(parts[1]) if len(parts) > 1 else 0
    if not year:
        log(f"warning: {doi} has no publication year in Crossref")
        return None

    rec = {
        "key": "",
        "type": "article" if m.get("type", "").startswith("journal") else m.get("type", "article"),
        "title": title,
        "authors": ", ".join(authors),
        "journal": strip_tags((m.get("container-title") or m.get("short-container-title") or [""])[0]),
        "year": year,
        "sort_year": int(year),
        "sort_month": month,
        "sort_date": int(year) * 100 + month,
        "doi": m.get("DOI", doi),
        "doi_url": f"https://doi.org/{m.get('DOI', doi)}",
    }
    if month:
        rec["month"] = MONTH_NAMES[month]
    if m.get("volume"):
        rec["volume"] = str(m["volume"])
    if m.get("issue"):
        rec["number"] = str(m["issue"])
    if m.get("page"):
        rec["pages"] = str(m["page"]).replace("--", "-")
    rec["link"] = (m.get("resource", {}).get("primary", {}).get("URL")
                   or rec["doi_url"])
    rec["key"] = slug_key(rec)
    return rec


def from_unpaywall(doi: str) -> dict:
    data = get_json(f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi)}?email={EMAIL}")
    if not data:
        return {}
    loc = data.get("best_oa_location")
    if not loc:
        return {}
    url = loc.get("url_for_pdf") or loc.get("url_for_landing_page") or loc.get("url")
    if not url:
        return {}
    if "arxiv.org" in url:
        source = "arXiv"
    elif loc.get("host_type") == "publisher":
        source = "Open access at journal"
    else:
        source = loc.get("repository_institution") or "Repository"
    return {"free_full_text_url": url, "free_full_text_source": source}


def read_dois() -> list[str]:
    dois = []
    for line in DOIS.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        line = re.sub(r"^(?:https?://)?(?:dx\.)?doi\.org/", "", line, flags=re.I)
        dois.append(line.lower())
    seen, unique = set(), []
    for d in dois:
        if d in seen:
            log(f"note: duplicate DOI in list, ignored: {d}")
            continue
        seen.add(d)
        unique.append(d)
    return unique


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true", help="re-fetch every DOI")
    ap.add_argument("--offline", action="store_true", help="use the cache only")
    args = ap.parse_args()

    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    overrides = yaml.safe_load(OVERRIDES.read_text(encoding="utf-8")) if OVERRIDES.exists() else {}
    extra = yaml.safe_load(EXTRA.read_text(encoding="utf-8")) if EXTRA.exists() else []
    overrides = overrides or {}
    extra = extra or []

    records, fetched, failed = [], 0, []
    for doi in read_dois():
        rec = cache.get(doi)
        if rec is None or args.refresh:
            if args.offline:
                log(f"error: {doi} not in cache and --offline was given")
                failed.append(doi)
                continue
            try:
                rec = from_crossref(doi)
            except Exception as exc:
                log(f"error: Crossref failed for {doi}: {exc}")
                failed.append(doi)
                continue
            if rec is None:
                log(f"error: Crossref has no record for {doi}")
                failed.append(doi)
                continue
            try:
                rec.update(from_unpaywall(doi))
            except Exception as exc:
                log(f"note: Unpaywall failed for {doi} ({exc}); continuing")
            cache[doi] = rec
            fetched += 1
            log(f"fetched {doi} -- {rec['title'][:60]}")
            time.sleep(0.3)
        merged = dict(rec)
        merged.update({k: v for k, v in (overrides.get(doi) or {}).items() if k != "hide"})
        if (overrides.get(doi) or {}).get("hide"):
            continue
        records.append(merged)

    for rec in extra:
        rec = dict(rec)
        rec.setdefault("sort_month", 0)
        rec.setdefault("sort_year", int(rec["year"]))
        rec.setdefault("sort_date", int(rec["year"]) * 100 + rec["sort_month"])
        records.append(rec)

    records.sort(key=lambda r: (r["sort_date"], r.get("title", "")), reverse=True)

    CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                     encoding="utf-8")
    header = ("# AUTO-GENERATED by scripts/build_pubs.py -- do not edit by hand.\n"
              "# Add a DOI to pubsrc/publications.dois.txt, then run the script.\n")
    OUT.write_text(header + yaml.safe_dump(records, allow_unicode=True, sort_keys=False,
                                           width=10**6, default_flow_style=False),
                   encoding="utf-8")
    log(f"wrote {OUT.relative_to(ROOT)}: {len(records)} entries ({fetched} newly fetched)")
    if failed:
        log(f"FAILED for {len(failed)} DOI(s): {', '.join(failed)}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
