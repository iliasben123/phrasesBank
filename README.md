# PhraseBank FR : sentiment financier en français

Jeu de données de phrases extraites des publications financières **publiques** des émetteurs marocains (Bourse de Casablanca, AMMC), annotées **positif / négatif / neutre** du point de vue d'un investisseur. C'est l'équivalent en français du [Financial PhraseBank](https://www.researchgate.net/publication/251231107) (Malo et al., 2014).

> Méthodologie complète : [docs/GUIDE_PHRASEBANK_FR.md](docs/GUIDE_PHRASEBANK_FR.md)
> Guide d'annotation : [docs/annotation_guidelines.md](docs/annotation_guidelines.md)

## Architecture

```
                    ┌─────────────── pipeline de données (src/phrasebank_fr) ───────────────┐
sources.csv ──►  download  ──►  extract  ──►  segment  ──►  filter  ──►  sentences.jsonl
 (registre)      PDF bruts      blocs de      phrases       phrases          │
                 data/raw/      texte         brutes        exploitables     ▼
                                data/interim/               data/processed/  annotation
                                                                             (Label Studio)
                                                                               │
          dataset publié  ◄──  consolidation + accord  ◄─────  data/annotations/
          (Hugging Face)        (à venir)
```

| Étape | Module | Entrée | Sortie |
|---|---|---|---|
| 1. Collecte | `sources.py` | `data/sources/sources.csv` | `data/raw/<doc_id>.pdf` |
| 2. Extraction | `extract.py` | PDF | `data/interim/blocks.jsonl` |
| 3. Segmentation | `segment.py` | blocs | `data/interim/sentences_raw.jsonl` |
| 4. Filtrage | `filter.py` | phrases brutes | `data/processed/sentences.jsonl` |
| 5. Échantillonnage | `sample.py` | phrases exploitables | `data/annotations/pilot_100.json` |
| 6. Annotation | Label Studio (`configs/label_studio.xml`) | tâches | `data/annotations/` |
| 7. Consolidation + accord | *à venir* | | |
| 8. Baselines | *à venir* | | |

Les paramètres (seuils de filtrage, détection des en-têtes) sont dans `configs/pipeline.yaml`.

## Structure

```
configs/            paramètres du pipeline
data/sources/       registre des documents (versionné)
data/raw/           PDF (non versionnés)
data/interim/       sorties intermédiaires
data/processed/     phrases prêtes à annoter
data/annotations/   exports d'annotation
docs/               guide méthodologique, guide d'annotation
notebooks/          exploration
src/phrasebank_fr/  code du pipeline
tests/              tests
```

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -e ".[dev]"
```

## Utilisation

1. Déclarer chaque document dans `data/sources/sources.csv` :

   | Champ | Exemple |
   |---|---|
   | `doc_id` | `iam_2024_t3` (devient le nom du PDF) |
   | `company` | `Maroc Telecom` |
   | `sector` | `Télécommunications` |
   | `doc_type` | `indicateurs_trimestriels`, `resultats_annuels`, `communique`, `rapport_annuel`, `prospectus` |
   | `period` | `2024-T3`, `2024-S1`, `2024` |
   | `pages` | pages à garder : `6-36`, `2;6-36` (vide = tout le document) |
   | `url` | lien direct vers le PDF (optionnel) |
   | `downloaded_at` | rempli automatiquement |

2. Télécharger les PDF, ou les déposer à la main dans `data/raw/<doc_id>.pdf` :
   ```bash
   python -m phrasebank_fr download
   ```
3. Produire les phrases :
   ```bash
   python -m phrasebank_fr run      # = extract + segment + filter
   ```
4. Tirer un échantillon à annoter (même nombre de phrases par secteur, tirage reproductible) :
   ```bash
   python -m phrasebank_fr sample --n 100 --seed 42 --name pilot_100
   ```

## Annotation avec Label Studio

```bash
pip install label-studio
label-studio start
```

1. Créer un projet, puis dans **Settings > Labeling Interface > Code**, coller le contenu de `configs/label_studio.xml`.
2. **Import** : charger `data/annotations/pilot_100.json`.
3. Annoter en suivant [docs/annotation_guidelines.md](docs/annotation_guidelines.md). Raccourcis : `1` positif, `2` négatif, `3` neutre, `4` à exclure.
4. **Export** au format JSON, dans `data/annotations/`.

Chaque annotateur travaille avec son propre compte, sans voir les labels des autres.

## Tests

```bash
pytest
```

## Licence

Code : MIT. Dataset : CC BY-NC-SA 4.0 (phrases issues de documents publics, sources référencées).
