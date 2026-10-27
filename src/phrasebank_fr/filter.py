"""Étape 4 : filtrage des phrases inutilisables et attribution des identifiants.

Supprime les fragments, titres, lignes de tableau, questions et doublons exacts.
Les quasi-doublons (même phrase, chiffres différents) sont conservés :
ils seront traités à l'échantillonnage.

L'identifiant est dérivé du texte de la phrase (et non d'un compteur) : il reste
le même quand on modifie les filtres ou les pages retenues, ce qui garde le lien
avec les annotations déjà faites.
"""
import hashlib
import re
from typing import Iterable, Iterator

# « : » est exclu volontairement : une phrase qui finit par « : » annonce une liste.
# « ? » aussi : les questions (interviews) ne sont pas annotables.
FINAL_PUNCTUATION = (".", "!", "»", ";", ")")


def normalize(sentence: str) -> str:
    return " ".join(sentence.lower().split())


def sentence_id(doc_id: str, sentence: str) -> str:
    digest = hashlib.sha1(normalize(sentence).encode("utf-8")).hexdigest()[:8]
    return f"{doc_id}_{digest}"


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
    for row in rows:
        sentence = row["sentence"]
        key = normalize(sentence)
        if key in seen or not is_usable(sentence, cfg, exclude):
            continue
        seen.add(key)
        yield {"id": sentence_id(row["doc_id"], sentence), **row}
