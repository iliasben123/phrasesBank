"""Étape 1 : registre des documents sources et téléchargement des PDF.

Chaque document est déclaré dans data/sources/sources.csv. Un PDF peut aussi
être déposé à la main dans data/raw/ sous le nom <doc_id>.pdf.
"""
import csv
import re
import time
from datetime import date
from pathlib import Path

import requests

FIELDS = ["doc_id", "company", "sector", "doc_type", "period", "pages", "url", "downloaded_at"]
USER_AGENT = "phrasebank-fr/0.1 (projet de recherche personnel)"
DELAY_SECONDS = 1.0  # politesse envers les serveurs


def read_sources(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_pages(spec: str) -> set[int] | None:
    """« 2;6-36 » -> {2, 6, 7, …, 36}. Une valeur vide signifie toutes les pages."""
    if not spec.strip():
        return None
    pages = set()
    for part in re.split(r"[;,]", spec):
        part = part.strip()
        if part:
            start, _, end = part.partition("-")
            pages.update(range(int(start), int(end or start) + 1))
    return pages


def page_selection(sources_path: Path) -> dict[str, set[int] | None]:
    if not sources_path.exists():
        return {}
    return {row["doc_id"]: parse_pages(row.get("pages") or "") for row in read_sources(sources_path)}


def write_sources(path: Path, rows: list[dict]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def download_missing(sources_path: Path, raw_dir: Path) -> int:
    """Télécharge les PDF déclarés dans le registre et absents de raw_dir."""
    rows = read_sources(sources_path)
    raw_dir.mkdir(parents=True, exist_ok=True)
    downloaded = 0
    for row in rows:
        target = raw_dir / f"{row['doc_id']}.pdf"
        if target.exists() or not row["url"]:
            continue
        try:
            resp = requests.get(row["url"], headers={"User-Agent": USER_AGENT}, timeout=60)
            resp.raise_for_status()
        except requests.RequestException as exc:
            print(f"[échec] {row['doc_id']} : {exc}")
            continue
        if not resp.content.startswith(b"%PDF"):
            print(f"[ignoré] {row['doc_id']} : la réponse n'est pas un PDF")
            continue
        target.write_bytes(resp.content)
        row["downloaded_at"] = date.today().isoformat()
        downloaded += 1
        print(f"[ok] {row['doc_id']}")
        time.sleep(DELAY_SECONDS)
    write_sources(sources_path, rows)
    return downloaded
