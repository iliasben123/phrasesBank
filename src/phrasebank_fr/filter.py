"""Étape 4 : filtrage des phrases inutilisables et attribution des identifiants.

Supprime les fragments, titres, lignes de tableau et doublons exacts.
Les quasi-doublons (même phrase, chiffres différents) sont conservés :
ils seront traités à l'échantillonnage.
"""
import re
from collections import Counter
from typing import Iterable, Iterator

# « : » est exclu volontairement : une phrase qui finit par « : » annonce une liste.
FINAL_PUNCTUATION = (".", "!", "?", "»", ";", ")")


def is_usable(sentence: str, cfg: dict, exclude: list[re.Pattern]) -> bool:
    if any(p.search(sentence) for p in exclude):
        return False
    n_words = len(sentence.split())
    if not cfg["min_words"] <= n_words <= cfg["max_words"]:
        return False
    chars = [c for c in sentence if not c.isspace()]
    if sum(c.isalpha() for c in chars) / len(chars) < cfg["min_alpha_ratio"]:
        return False
    if sum(c.isdigit() for c in chars) / len(chars) > cfg["max_digit_ratio"]:
        return False
    if cfg["require_final_punctuation"] and not sentence.endswith(FINAL_PUNCTUATION):
        return False
    return True


def filter_sentences(rows: Iterable[dict], cfg: dict) -> Iterator[dict]:
    exclude = [re.compile(p, re.IGNORECASE) for p in cfg["exclude_patterns"]]
    seen = set()
    per_doc = Counter()
    for row in rows:
        sentence = row["sentence"]
        key = " ".join(sentence.lower().split())
        if key in seen or not is_usable(sentence, cfg, exclude):
            continue
        seen.add(key)
        per_doc[row["doc_id"]] += 1
        yield {"id": f"{row['doc_id']}_{per_doc[row['doc_id']]:04d}", **row}
