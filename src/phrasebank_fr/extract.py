"""Étape 2 : extraction des blocs de texte des PDF.

Un « bloc » est un paragraphe tel que PyMuPDF le détecte sur la page.
Les en-têtes et pieds de page sont repérés parce qu'ils se trouvent dans
les marges haute ou basse ET se répètent sur de nombreuses pages.
Seules les pages déclarées dans la colonne `pages` du registre sont gardées.
"""
import re
from collections import Counter
from pathlib import Path

import pymupdf

from .sources import page_selection


def _in_margin(block: tuple, page_height: float, margin_ratio: float) -> bool:
    _, y0, _, y1 = block[:4]
    return y1 <= page_height * margin_ratio or y0 >= page_height * (1 - margin_ratio)


def _repetition_key(text: str) -> str:
    # Les numéros de page changent d'une page à l'autre : on les neutralise.
    return re.sub(r"\d+", "0", " ".join(text.split())).lower()


def _clean_block(text: str) -> str:
    text = re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", " ", text)  # caractères de contrôle (ex. \x07)
    text = re.sub(r"(\w)-\n([a-zà-ÿ])", r"\1\2", text)  # recolle les césures
    return " ".join(text.split())


def extract_blocks(
    pdf_path: Path,
    repeated_block_ratio: float,
    margin_ratio: float,
    keep_pages: set[int] | None = None,
) -> list[dict]:
    # pages = liste de (texte, est_dans_une_marge) par page
    with pymupdf.open(pdf_path) as doc:
        pages = [
            # block = (x0, y0, x1, y1, texte, numéro, type) ; type 0 = texte, 1 = image
            [(b[4], _in_margin(b, page.rect.height, margin_ratio))
             for b in page.get_text("blocks") if b[6] == 0]
            for page in doc
        ]

    # Les répétitions sont comptées sur toutes les pages, même celles qu'on ne garde pas.
    margin_counts = Counter(
        key for page in pages for key in {_repetition_key(t) for t, in_margin in page if in_margin}
    )
    threshold = max(2, repeated_block_ratio * len(pages))

    blocks = []
    for page_num, page in enumerate(pages, start=1):
        if keep_pages is not None and page_num not in keep_pages:
            continue
        for raw, in_margin in page:
            if in_margin and margin_counts[_repetition_key(raw)] >= threshold:
                continue
            text = _clean_block(raw)
            if text:
                blocks.append({"doc_id": pdf_path.stem, "page": page_num, "text": text})
    return blocks


def extract_all(raw_dir: Path, sources_path: Path, repeated_block_ratio: float, margin_ratio: float):
    selection = page_selection(sources_path)
    for pdf_path in sorted(raw_dir.glob("*.pdf")):
        yield from extract_blocks(pdf_path, repeated_block_ratio, margin_ratio, selection.get(pdf_path.stem))
