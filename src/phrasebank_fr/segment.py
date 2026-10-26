"""Étape 3 : découpage des blocs en phrases.

pySBD gère les pièges du français financier : « 3,2 MMDH. », « M. », « S.A. ».
Les listes à puces sont découpées avant, chaque puce devenant une phrase.
"""
import re
from typing import Iterable, Iterator

import pysbd

#  : puce de la police Symbol, fréquente dans les PDF exportés depuis Word
BULLETS = re.compile(r"\s*[•▪●■◦›]\s*")
# Marqueur en tête de phrase : chiffre isolé (puce mal décodée, ex. « 3 La hausse… »)
# ou numérotation de section (« 5-4-1 Le résultat… »), suivi d'une majuscule.
LEADING_MARKER = re.compile(r"^(\d|\d+(-\d+)+)\s+(?=[A-ZÀ-Ý])")


def segment_blocks(blocks: Iterable[dict], language: str = "fr") -> Iterator[dict]:
    segmenter = pysbd.Segmenter(language=language, clean=False)
    for block in blocks:
        for item in BULLETS.split(block["text"]):
            for sentence in segmenter.segment(item):
                sentence = LEADING_MARKER.sub("", sentence.strip())
                if sentence:
                    yield {"doc_id": block["doc_id"], "page": block["page"], "sentence": sentence}
