"""Étape 5 : échantillonnage stratifié des phrases à annoter.

Le même nombre de phrases est tiré par secteur (dans la limite des phrases
disponibles), pour que chaque secteur pèse autant dans la mesure d'accord.
Le tirage est reproductible grâce à la graine (seed).
"""
import random
from collections import defaultdict
from typing import Iterable


def stratified_sample(rows: Iterable[dict], sector_of: dict[str, str], n: int, seed: int) -> list[dict]:
    by_sector = defaultdict(list)
    for row in rows:
        by_sector[sector_of.get(row["doc_id"], "Inconnu")].append(row)

    rng = random.Random(seed)
    sectors = sorted(by_sector)
    for sector in sectors:
        rng.shuffle(by_sector[sector])

    # Répartition à tour de rôle : un secteur épuisé laisse sa part aux autres.
    quotas = dict.fromkeys(sectors, 0)
    remaining = n
    while remaining > 0:
        open_sectors = [s for s in sectors if quotas[s] < len(by_sector[s])]
        if not open_sectors:
            break
        for sector in open_sectors[:remaining]:
            quotas[sector] += 1
        remaining = n - sum(quotas.values())

    sample = [row for sector in sectors for row in by_sector[sector][: quotas[sector]]]
    rng.shuffle(sample)  # l'annotateur ne voit pas les secteurs en bloc
    return sample


def to_label_studio(rows: Iterable[dict], sources: dict[str, dict]) -> list[dict]:
    """Format d'import Label Studio : une tâche par phrase, métadonnées dans `data`."""
    tasks = []
    for row in rows:
        source = sources.get(row["doc_id"], {})
        tasks.append({"data": {
            "text": row["sentence"],
            "sentence_id": row["id"],
            "doc_id": row["doc_id"],
            "page": row["page"],
            "company": source.get("company", ""),
            "sector": source.get("sector", ""),
            "doc_type": source.get("doc_type", ""),
            "period": source.get("period", ""),
        }})
    return tasks
