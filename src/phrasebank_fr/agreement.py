"""Étape 7 : accord inter-annotateurs sur les exports JSON de Label Studio.

Chaque annotateur est identifié par son fichier d'export (et par son compte
Label Studio si un même fichier contient plusieurs annotateurs). Une phrase est
identifiée par son `sentence_id`, ce qui permet de comparer des exports venant
de projets Label Studio différents.
"""
import csv
import json
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

LABELS = ["positive", "negative", "neutral", "exclude"]


def load_exports(paths: list[Path]) -> tuple[dict[str, dict[str, str]], dict[str, str], dict[str, set[str]]]:
    """Retourne (labels[annotateur][phrase], texte[phrase], ambigu[phrase] = annotateurs ayant coché « ambigu »)."""
    labels = defaultdict(dict)
    texts = {}
    ambiguous = defaultdict(set)
    for path in paths:
        tasks = json.loads(Path(path).read_text(encoding="utf-8"))
        accounts = {a.get("completed_by") for t in tasks for a in t.get("annotations", [])}
        for task in tasks:
            key = task["data"].get("sentence_id") or task["data"]["text"]
            texts[key] = task["data"]["text"]
            for annotation in task.get("annotations", []):
                if annotation.get("was_cancelled"):
                    continue
                name = Path(path).stem if len(accounts) == 1 else f"{Path(path).stem}:{annotation.get('completed_by')}"
                result = {r["from_name"]: r["value"] for r in annotation["result"]}
                if "sentiment" not in result:
                    continue
                labels[name][key] = result["sentiment"]["choices"][0]
                if result.get("ambiguous", {}).get("choices"):
                    ambiguous[key].add(name)
    return dict(labels), texts, dict(ambiguous)


def cohen_kappa(a: list[str], b: list[str]) -> float:
    n = len(a)
    observed = sum(x == y for x, y in zip(a, b)) / n
    count_a, count_b = Counter(a), Counter(b)
    expected = sum(count_a[c] * count_b[c] for c in set(a) | set(b)) / n**2
    return 1.0 if expected == 1 else (observed - expected) / (1 - expected)


def fleiss_kappa(ratings: list[list[str]]) -> float:
    """`ratings` : une liste de labels par phrase, avec le même nombre d'annotateurs pour chaque phrase."""
    n_items, n_raters = len(ratings), len(ratings[0])
    counts = [Counter(item) for item in ratings]
    categories = set().union(*counts)
    p_items = [(sum(c * c for c in cnt.values()) - n_raters) / (n_raters * (n_raters - 1)) for cnt in counts]
    p_bar = sum(p_items) / n_items
    p_cat = {k: sum(cnt[k] for cnt in counts) / (n_items * n_raters) for k in categories}
    p_e = sum(p * p for p in p_cat.values())
    return 1.0 if p_e == 1 else (p_bar - p_e) / (1 - p_e)


def interpret(kappa: float) -> str:
    """Échelle de Landis et Koch (1977)."""
    for threshold, label in [(0.8, "presque parfait"), (0.6, "substantiel"), (0.4, "modéré"), (0.2, "faible"), (0.0, "très faible")]:
        if kappa > threshold:
            return label
    return "nul ou négatif"


def confusion(a: list[str], b: list[str]) -> dict[tuple[str, str], int]:
    return Counter(zip(a, b))


def report(labels: dict[str, dict[str, str]], texts: dict[str, str], ambiguous: dict[str, set[str]], out: Path) -> None:
    annotators = sorted(labels)
    if len(annotators) < 2:
        raise SystemExit(f"Il faut au moins 2 annotateurs, trouvé(s) : {annotators}")
    common = sorted(set.intersection(*(set(labels[a]) for a in annotators)))
    print(f"Annotateurs : {', '.join(annotators)}")
    print(f"Phrases annotées par tous : {len(common)}\n")

    for name in annotators:
        dist = Counter(labels[name][k] for k in common)
        print(f"  {name:<30} " + "  ".join(f"{lab}={dist[lab]}" for lab in LABELS))
    print()

    for x, y in combinations(annotators, 2):
        a = [labels[x][k] for k in common]
        b = [labels[y][k] for k in common]
        kappa = cohen_kappa(a, b)
        raw = sum(i == j for i, j in zip(a, b)) / len(common)
        print(f"{x} / {y} : accord brut {raw:.0%}, kappa de Cohen {kappa:.3f} ({interpret(kappa)})")
        matrix = confusion(a, b)
        print(f"  {'':<10}" + "".join(f"{lab:>10}" for lab in LABELS) + f"   <- {y}")
        for la in LABELS:
            print(f"  {la:<10}" + "".join(f"{matrix[(la, lb)]:>10}" for lb in LABELS))
        print()

    if len(annotators) >= 3:
        kappa = fleiss_kappa([[labels[a][k] for a in annotators] for k in common])
        print(f"Kappa de Fleiss ({len(annotators)} annotateurs) : {kappa:.3f} ({interpret(kappa)})\n")

    rows = [k for k in common if len({labels[a][k] for a in annotators}) > 1 or k in ambiguous]
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["sentence_id", "desaccord", *annotators, "ambigu_selon", "texte", "decision", "regle_du_guide"])
        for k in sorted(rows, key=lambda k: (len({labels[a][k] for a in annotators}) == 1, k)):
            disagree = len({labels[a][k] for a in annotators}) > 1
            writer.writerow([k, "oui" if disagree else "non", *(labels[a][k] for a in annotators),
                             ", ".join(sorted(ambiguous.get(k, ()))), texts[k], "", ""])
    n_disagree = sum(len({labels[a][k] for a in annotators}) > 1 for k in common)
    print(f"{n_disagree} désaccord(s) et {len(rows) - n_disagree} accord(s) marqué(s) ambigu -> {out}")
