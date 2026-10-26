# Construire un PhraseBank financier en français (contexte marocain)

> Guide de référence pour créer, annoter et publier un jeu de données de **sentiment financier en français**, construit à partir des publications des émetteurs marocains.

---

## Sommaire

1. [Le projet en une page](#1-le-projet-en-une-page)
2. [Le modèle à imiter : Financial PhraseBank](#2-le-modèle-à-imiter--financial-phrasebank)
3. [Comprendre la finance marocaine](#3-comprendre-la-finance-marocaine)
4. [Les documents sources](#4-les-documents-sources)
5. [La langue financière marocaine : ce qui rend l'annotation difficile](#5-la-langue-financière-marocaine--ce-qui-rend-lannotation-difficile)
6. [Méthodologie de construction, étape par étape](#6-méthodologie-de-construction-étape-par-étape)
7. [Le guide d'annotation](#7-le-guide-dannotation)
8. [Mesurer la qualité : l'accord inter-annotateurs](#8-mesurer-la-qualité--laccord-inter-annotateurs)
9. [Format, licence et publication](#9-format-licence-et-publication)
10. [Valoriser le dataset : modèles de référence](#10-valoriser-le-dataset--modèles-de-référence)
11. [Feuille de route](#11-feuille-de-route)
12. [Glossaire](#12-glossaire)
13. [Références](#13-références)

---

## 1. Le projet en une page

**Constat :** les modèles de sentiment financier (FinBERT, etc.) sont entraînés sur des données **anglaises**. Il n'existe pas d'équivalent public du Financial PhraseBank en français, et encore moins adapté au vocabulaire des émetteurs marocains.

**Objectif :** produire un jeu de données de phrases extraites de documents financiers publics marocains, chacune étiquetée **positive / négative / neutre** du point de vue d'un investisseur.

**Livrables visés :**

| Livrable | Pourquoi c'est important |
|---|---|
| Dataset annoté (2 000 à 5 000 phrases) | Le cœur du projet, réutilisable par d'autres |
| Guide d'annotation | Prouve la rigueur méthodologique |
| Mesure d'accord inter-annotateurs | Prouve la qualité des labels |
| Modèles de référence (baselines) | Montre que le dataset est utile |
| Publication Hugging Face + GitHub | Visibilité, lien direct pour le CV |

**Ce que vous démontrez sur un CV :** collecte de données, nettoyage, conception d'une tâche d'annotation, contrôle qualité, fine-tuning de modèles NLP, publication. C'est le cycle complet d'un projet data/IA.

> ⚠️ **Confidentialité :** n'utilisez **que des documents publics**. Aucun document interne de votre stage ne doit entrer dans ce dataset, même anonymisé.

---

## 2. Le modèle à imiter : Financial PhraseBank

Publié par Malo et al. (2014), *« Good debt or bad debt: Detecting semantic orientations in economic texts »*.

| Caractéristique | Financial PhraseBank (anglais) |
|---|---|
| Taille | ~4 840 phrases |
| Source | Actualités financières en anglais sur des sociétés cotées (bourse d'Helsinki) |
| Labels | positif / négatif / neutre |
| Perspective | **Investisseur** : la phrase aurait-elle un effet positif, négatif ou nul sur le cours de l'action ? |
| Annotateurs | 16 personnes avec une formation en finance/économie |
| Particularité | Publié en **sous-ensembles selon le taux d'accord** : 50 %, 66 %, 75 %, 100 % des annotateurs d'accord |
| Distribution | Environ 59 % neutre, 28 % positif, 12 % négatif |

**Les trois idées clés à reprendre :**

1. **La perspective investisseur.** On n'annote pas l'émotion du texte mais son impact probable sur la valeur de l'entreprise. *« Le groupe a réduit ses effectifs de 10 % »* peut être neutre ou positif pour un investisseur (baisse des coûts), même si c'est humainement négatif.
2. **Plusieurs annotateurs par phrase.** Un seul avis ne suffit pas, le sentiment financier est souvent ambigu.
3. **Publier le niveau d'accord.** Ça permet d'entraîner sur les phrases consensuelles et d'étudier les cas ambigus.

---

## 3. Comprendre la finance marocaine

### 3.1 Les acteurs

| Acteur | Rôle | Ce qui vous concerne |
|---|---|---|
| **Bourse de Casablanca** | Marché boursier marocain (environ 75-80 sociétés cotées) | Liste des émetteurs, publications, cours |
| **AMMC** (Autorité Marocaine du Marché des Capitaux, ex-CDVM) | Régulateur des marchés : vise les prospectus, impose les obligations d'information | Source des prospectus et des règles de communication financière |
| **Bank Al-Maghrib (BAM)** | Banque centrale : politique monétaire, taux directeur, supervision bancaire | Ses décisions influencent le sentiment de tout le marché |
| **Maroclear** | Dépositaire central des titres | Peu utile pour vous |
| **Sociétés de bourse** | Intermédiaires qui exécutent les ordres et publient des analyses | Notes de recherche (souvent réservées aux clients) |
| **Sociétés de gestion d'actifs** (Wafa Gestion, CDG Capital Gestion, BMCE Capital Gestion…) | Gèrent des OPCVM (fonds) pour des clients | Les **utilisateurs finaux** d'un outil d'analyse de sentiment |
| **ASFIM** | Association professionnelle des sociétés de gestion | Statistiques sur les fonds |

### 3.2 Le marché

- **Monnaie :** dirham marocain (MAD). Les montants sont souvent exprimés en **MMDH** (milliards de dirhams) ou **MDH** (millions de dirhams).
- **Indices :** le **MASI** (indice global de toutes les valeurs cotées) et des indices plus restreints regroupant les valeurs les plus liquides. Vérifiez les noms en vigueur sur le site de la Bourse, ils ont évolué récemment.
- **Poids des secteurs :** le marché est dominé par les **banques**, les **télécoms** et quelques grands groupes industriels.

| Secteur | Exemples d'émetteurs cotés |
|---|---|
| Banques | Attijariwafa bank, BCP, Bank of Africa, CIH Bank, CDM |
| Télécoms | Maroc Telecom (IAM) |
| Assurances | Wafa Assurance, AtlantaSanad |
| Bâtiment et matériaux | LafargeHolcim Maroc, Ciments du Maroc, Jet Contractors |
| Immobilier | Addoha, Alliances, Résidences Dar Saada |
| Distribution | LabelVie, Auto Hall |
| Mines | Managem, SMI |
| Énergie | TotalEnergies Marketing Maroc, Taqa Morocco, Afriquia Gaz |
| Agroalimentaire | Cosumar, Lesieur Cristal, Centrale Danone |

> Liste indicative : vérifiez sur le site de la Bourse de Casablanca, les cotations changent (introductions, radiations, changements de nom).

### 3.3 Les obligations de communication financière

Les sociétés cotées doivent publier régulièrement, ce qui produit un **flux régulier de documents comparables**, idéal pour un dataset :

| Publication | Fréquence | Contenu typique |
|---|---|---|
| **Indicateurs trimestriels** | Chaque trimestre | Chiffre d'affaires, investissements, endettement, faits marquants. Court et dense en sentiment. |
| **Résultats semestriels** | Juin | Comptes semestriels, commentaires de la direction |
| **Résultats annuels** | Mars-avril | Comptes annuels, perspectives |
| **Rapport financier annuel / rapport ESG** | Annuel | Document long, beaucoup de texte narratif |
| **Communiqués de presse** | Ponctuel | Événements : acquisitions, contrats, changements de dirigeants, avertissements sur résultats (*profit warning*) |
| **Prospectus / note d'information** | À chaque émission (actions, obligations) | Très long, juridique, section « facteurs de risque » |

> Les règles précises (délais, contenu obligatoire) sont fixées par la loi et les circulaires de l'AMMC. Consultez la rubrique réglementation de ammc.ma pour les détails à jour.

### 3.4 Les indicateurs à connaître

Pour annoter correctement, vous devez savoir si la **hausse d'un indicateur est une bonne ou une mauvaise nouvelle**.

**Indicateurs généraux**

| Indicateur | Signification | Hausse = |
|---|---|---|
| Chiffre d'affaires (CA) | Ventes | 🟢 positif |
| EBE / EBITDA | Rentabilité opérationnelle avant amortissements | 🟢 positif |
| Résultat d'exploitation (REX) | Rentabilité de l'activité | 🟢 positif |
| Résultat net / **RNPG** (résultat net part du groupe) | Bénéfice revenant aux actionnaires | 🟢 positif |
| Marge (opérationnelle, nette) | Rentabilité en % | 🟢 positif |
| Endettement net / dette nette | Ce que l'entreprise doit | 🔴 négatif (en général) |
| Gearing (dette / fonds propres) | Levier financier | 🔴 négatif |
| Charges, coûts | Dépenses | 🔴 négatif |
| Investissements (CAPEX) | Dépenses d'avenir | ⚪ souvent neutre ou 🟢, selon le contexte |
| Dividende | Rémunération des actionnaires | 🟢 positif |

**Indicateurs spécifiques aux banques** (très présentes à la Bourse de Casablanca)

| Indicateur | Signification | Hausse = |
|---|---|---|
| **PNB** (produit net bancaire) | Le « chiffre d'affaires » d'une banque | 🟢 positif |
| Marge d'intérêt | Différence entre intérêts perçus et versés | 🟢 positif |
| **Coût du risque** | Provisions pour crédits non remboursés | 🔴 négatif |
| **Créances en souffrance** (taux de CES) | Crédits en difficulté | 🔴 négatif |
| Coefficient d'exploitation | Charges / PNB | 🔴 négatif (plus il est bas, mieux c'est) |
| Ratio de solvabilité | Solidité financière | 🟢 positif |
| Encours de crédits / dépôts | Activité de la banque | 🟢 positif en général |

**Indicateurs spécifiques aux assurances :** primes émises (🟢), sinistralité (🔴), ratio combiné (🔴).

### 3.5 Le contexte macroéconomique qui colore les textes

Les commentaires des émetteurs font souvent référence à :

- les **décisions de taux de Bank Al-Maghrib** ;
- l'**inflation** et le pouvoir d'achat ;
- la **sécheresse** et la campagne agricole (poids important de l'agriculture dans le PIB) ;
- les **prix des matières premières** (énergie, phosphates, blé) ;
- les **grands chantiers** (infrastructures, Coupe du monde 2030), favorables au BTP et aux matériaux.

Ces phrases de contexte posent une question d'annotation importante, traitée en section 7.

---

## 4. Les documents sources

### 4.1 Où les trouver

| Source | Contenu | Remarques |
|---|---|---|
| Sites « Investisseurs » / « Communication financière » des émetteurs | Indicateurs trimestriels, résultats, rapports annuels, communiqués | **La meilleure source**, structurée par date |
| casablanca-bourse.com | Publications des émetteurs | Pratique pour couvrir tous les émetteurs |
| ammc.ma | Prospectus, notes d'information, documents de référence | Documents longs, utiles pour la section « risques » |
| Presse financière (Médias24, L'Économiste, Le Matin Éco, LesEco.ma…) | Articles sur les résultats | ⚠️ Droits d'auteur : pour un dataset publié, privilégiez les documents des émetteurs |

### 4.2 Quels documents privilégier

Pour un **sentiment dense**, prenez d'abord :
1. **Les indicateurs trimestriels et communiqués de résultats** : chaque phrase porte une information chiffrée et orientée.
2. **Les sections « Faits marquants », « Perspectives » et « Mot du Président »** des rapports annuels.
3. **Les sections « Facteurs de risque » des prospectus**, beaucoup de phrases négatives, utiles pour équilibrer.

Évitez au début : les états financiers bruts (tableaux), les mentions légales, les notes annexes très techniques.

### 4.3 Diversité à viser

Pour que le dataset soit représentatif, équilibrez selon :
- le **secteur** (pas seulement des banques) ;
- le **type de document** ;
- la **période** : incluez des années difficiles (2020 avec le Covid, années de sécheresse, poussée d'inflation 2022-2023) pour avoir assez de phrases négatives ;
- la **taille de l'émetteur** (grandes capitalisations et petites).

### 4.4 Collecte : bonnes pratiques

- Téléchargement manuel au début (20 à 50 PDF), automatisation ensuite.
- Si vous scrapez : respectez le `robots.txt`, limitez la fréquence des requêtes, identifiez votre script.
- Tenez un **registre des sources** (`sources.csv`) : émetteur, type de document, date, URL, date de téléchargement. C'est indispensable pour la traçabilité.

---

## 5. La langue financière marocaine : ce qui rend l'annotation difficile

### 5.1 Un ton très policé

La communication financière marocaine est **rarement ouvertement négative**. Les mauvaises nouvelles sont euphémisées :

| Formulation | Sens réel probable |
|---|---|
| « Dans un contexte difficile, le groupe a fait preuve de **résilience** » | Résultats en baisse ou stagnants |
| « Le chiffre d'affaires **s'inscrit en léger retrait** » | Baisse |
| « Le résultat net **se maintient** à… » | Stagnation, souvent légèrement décevant |
| « Le groupe a poursuivi ses efforts de **maîtrise des charges** » | Pression sur les marges |
| « Une **normalisation** du coût du risque » | Hausse du coût du risque (négatif) |
| « Un **effet de base défavorable** » | Baisse par rapport à l'année précédente |
| « Une **performance solide** » / « une **progression soutenue** » | Clairement positif |

C'est précisément **la valeur ajoutée de votre dataset** : un modèle entraîné sur de l'anglais ou sur du français généraliste rate ces nuances.

### 5.2 Le vocabulaire de la variation

Constituez un lexique au fil de l'annotation, il vous servira de baseline (section 10) :

- **Hausse :** progresse, croît, augmente, s'améliore, se renforce, s'apprécie, bondit, en hausse de, en amélioration, en progression
- **Baisse :** recule, baisse, diminue, se replie, se contracte, se dégrade, s'effrite, en retrait, en repli, en recul
- **Stabilité :** se stabilise, se maintient, demeure stable, s'établit à, ressort à, atteint

> ⚠️ **Le verbe ne suffit pas.** « Le coût du risque **recule** » est **positif**. « L'endettement **progresse** » est **négatif**. Le sentiment dépend du couple (indicateur, direction).

### 5.3 Autres particularités

- **Chiffres et unités :** « 3,2 MMDH », « +5,4 % », « 12,1 Md MAD ». Gardez-les dans la phrase, ils sont porteurs de sens.
- **Comparaisons implicites :** « par rapport à la même période de l'exercice précédent », « à fin septembre ».
- **Documents bilingues :** certains émetteurs publient en français et en anglais, parfois en arabe. Ne gardez que le français pour ce dataset (l'anglais pourrait servir plus tard pour un dataset parallèle).
- **Phrases longues et composées :** une phrase peut contenir une bonne et une mauvaise nouvelle (voir les règles en section 7).

---

## 6. Méthodologie de construction, étape par étape

```
 1. Collecte     2. Extraction   3. Segmentation   4. Filtrage     5. Échantillonnage
 PDF publics ──► texte brut ───► phrases ────────► phrases utiles ► lot à annoter
                                                                         │
 9. Publication ◄── 8. Consolidation ◄── 7. Annotation ◄── 6. Guide + pilote
```

### Étape 1 : Collecte
Voir section 4. Objectif initial : **30 à 50 documents** couvrant au moins 6 secteurs.

### Étape 2 : Extraction du texte
- **PyMuPDF** (`fitz`) : rapide, bon pour le texte.
- **pdfplumber** : meilleur pour repérer les tableaux et les exclure.
- PDF scannés (images) : OCR avec **Tesseract** (langue `fra`). Évitez-les au début.

Pièges : en-têtes et pieds de page répétés, numéros de page, colonnes multiples, césures de mots en fin de ligne, puces.

### Étape 3 : Segmentation en phrases
Ne coupez pas naïvement sur les points : « 3,2 MMDH. », « M. Dupont », « S.A. », « +5,4 % vs. 2023 » posent problème.
- **spaCy** avec le modèle français (`fr_core_news_sm` ou `fr_core_news_md`) ;
- ou **pySBD**, conçu pour la segmentation robuste.

Vérifiez manuellement un échantillon de 100 phrases.

### Étape 4 : Filtrage
Supprimez :
- les phrases trop courtes (< 6 mots) ou trop longues (> 60 mots) ;
- les doublons et quasi-doublons (les mêmes formules reviennent d'un trimestre à l'autre) ;
- les lignes de tableau, titres, mentions légales ;
- les phrases sans aucun contenu financier (optionnel, via une liste de mots-clés).

### Étape 5 : Échantillonnage
Problème : dans un corpus brut, **la grande majorité des phrases sont neutres**. Si vous annotez au hasard, vous aurez très peu de négatives.

Solutions :
- **Échantillonnage stratifié** par secteur, type de document et année.
- **Pré-filtrage orienté** : utilisez le lexique (section 5.2) ou un LLM pour estimer le sentiment, puis tirez davantage de phrases potentiellement négatives.
- **Documentez-le.** Un dataset dont la distribution a été rééquilibrée doit le dire clairement.

### Étape 6 : Guide d'annotation et pilote
- Rédigez une première version du guide (section 7).
- Annotez **100 phrases pilotes** avec au moins un autre annotateur.
- Mesurez l'accord, discutez les désaccords, **corrigez le guide**. Recommencez si l'accord est faible.

### Étape 7 : Annotation à grande échelle
**Outils open source** (inutile d'en coder un) :

| Outil | Points forts |
|---|---|
| **Label Studio** | Le plus utilisé, interface simple, gestion multi-annotateurs, export CSV/JSON |
| **Argilla** | Bien intégré à Hugging Face, adapté à l'annotation assistée par modèle |
| **Doccano** | Léger, simple à installer |

> 💡 Votre profil fullstack : vous pourriez aussi créer une petite interface d'annotation sur mesure. C'est un bon exercice, mais **pas une priorité**. Commencez avec Label Studio.

**Qui annote ?**
- Idéalement **3 annotateurs par phrase** (le vote majoritaire tranche).
- Profils : vous-même, des camarades en finance/économie, des contacts du secteur.
- Minimum réaliste pour un projet personnel : **vous + 1 ou 2 personnes** sur un sous-ensemble (pour mesurer l'accord), vous seul sur le reste.

**Annotation assistée par LLM (optionnelle, à documenter) :**
1. Un LLM pré-annote les phrases.
2. Un humain valide ou corrige.
3. Vous mesurez **l'accord entre le LLM et les humains**. C'est en soi un résultat intéressant.

⚠️ Risque : l'annotateur humain a tendance à accepter la suggestion (biais d'ancrage). Pour le sous-ensemble servant à mesurer l'accord, annotez **sans** pré-annotation.

### Étape 8 : Consolidation
- Label final = **vote majoritaire**.
- Égalité : **adjudication** par une personne de référence, ou la phrase est marquée ambiguë.
- Stockez le **taux d'accord** de chaque phrase, comme le PhraseBank original.

### Étape 9 : Publication
Voir section 9.

---

## 7. Le guide d'annotation

C'est **le document le plus important du projet**. Un bon guide rend l'annotation reproductible.

### 7.1 La question à se poser

> **« Si j'étais investisseur et que je lisais uniquement cette phrase, penserais-je que la valeur de l'entreprise va plutôt monter, plutôt baisser, ou cela n'a pas d'effet ? »**

### 7.2 Définition des labels

| Label | Définition | Exemples |
|---|---|---|
| **Positif** | Information favorable à la valeur de l'entreprise | « Le PNB progresse de 8,2 % à 14,3 MMDH. » · « Le Conseil propose un dividende en hausse de 10 %. » · « Le groupe a remporté un contrat de 2 MMDH. » |
| **Négatif** | Information défavorable à la valeur de l'entreprise | « Le résultat net part du groupe recule de 15 %. » · « Le coût du risque s'alourdit à 1,9 MMDH. » · « L'endettement net atteint 9 MMDH, en hausse de 25 %. » |
| **Neutre** | Information factuelle sans orientation claire, ou sans impact sur la valeur | « Le Conseil d'administration s'est réuni le 18 mars 2025. » · « Le chiffre d'affaires s'établit à 2,1 MMDH. » (sans comparaison) · « La société opère dans le secteur du ciment. » |

### 7.3 Règles pour les cas difficiles

| Cas | Règle proposée | Exemple |
|---|---|---|
| Chiffre sans comparaison | **Neutre** | « Les investissements s'élèvent à 450 MDH. » |
| Hausse d'un indicateur « négatif » | **Négatif** | « Les charges d'exploitation augmentent de 12 %. » |
| Baisse d'un indicateur « négatif » | **Positif** | « Le taux de créances en souffrance s'améliore à 7,1 %. » |
| Phrase mixte, un élément domine | Label de l'élément **le plus important pour l'investisseur** (résultat > CA > coûts) | « Malgré la baisse du CA, le résultat net progresse de 12 %. » → positif |
| Phrase mixte équilibrée | **Neutre**, et marquer comme ambiguë | « Le CA progresse de 3 % tandis que la marge recule de 3 points. » |
| Contexte macro sans lien direct | **Neutre** | « L'inflation s'est établie à 4 % en 2023. » |
| Contexte macro avec impact explicite | Selon l'impact | « La hausse des prix de l'énergie a pesé sur les marges. » → négatif |
| Perspectives / prévisions | Annoter selon l'orientation annoncée | « Le groupe prévoit une croissance à deux chiffres en 2025. » → positif |
| Euphémisme | Annoter le **sens réel** | « Le résultat net se maintient malgré un contexte exigeant. » → neutre ou négatif selon le guide (à trancher en pilote) |
| Facteur de risque (prospectus) | **Négatif** s'il décrit un risque spécifique, **neutre** s'il est générique ou juridique | « La société est fortement dépendante d'un client unique. » → négatif |
| Variation faible (< 1 %) | **Neutre** | « Le CA est quasi stable à +0,4 %. » |

### 7.4 Ce qu'on n'utilise pas pour annoter
- Ses connaissances externes sur l'entreprise ou le cours de bourse réel.
- Le contexte des phrases voisines (on annote **la phrase seule**, comme le PhraseBank original).
- Son opinion personnelle sur l'entreprise ou le secteur.

### 7.5 Option : labels supplémentaires
Vous pouvez enrichir le dataset avec des métadonnées utiles pour des analyses futures :
- **aspect** : chiffre d'affaires, rentabilité, dette, dividende, risque, stratégie, macro… ;
- **intensité** : faible / forte ;
- **ambiguïté** : case à cocher.

> Commencez **sans** ces options. Ajoutez-les seulement si l'annotation de base est fluide.

---

## 8. Mesurer la qualité : l'accord inter-annotateurs

Sans mesure d'accord, un dataset n'est pas crédible.

| Mesure | Quand l'utiliser |
|---|---|
| **Cohen's kappa (κ)** | 2 annotateurs |
| **Fleiss' kappa** | 3 annotateurs ou plus, tous sur les mêmes phrases |
| **Krippendorff's alpha (α)** | Cas général (nombre variable d'annotateurs, données manquantes) |

**Interprétation usuelle du kappa** (Landis & Koch) :

| κ | Accord |
|---|---|
| < 0,20 | Faible |
| 0,21 – 0,40 | Passable |
| 0,41 – 0,60 | Modéré |
| 0,61 – 0,80 | **Substantiel** ← objectif |
| > 0,80 | Presque parfait |

Pour le sentiment financier, un κ autour de 0,6-0,7 est déjà un bon résultat : la tâche est subjective.

**En Python :** `sklearn.metrics.cohen_kappa_score`, `statsmodels.stats.inter_rater.fleiss_kappa`, le paquet `krippendorff`.

**Après chaque mesure :** examinez la **matrice de confusion entre annotateurs**. Si les désaccords sont surtout neutre ↔ positif sur les euphémismes, c'est une règle du guide à clarifier.

---

## 9. Format, licence et publication

### 9.1 Format des données

**JSONL** (une ligne JSON par phrase) ou **CSV**. Champs recommandés :

```json
{
  "id": "iam_2024_t3_0042",
  "sentence": "Le chiffre d'affaires consolidé progresse de 3,1 % à 27,4 MMDH.",
  "label": "positive",
  "agreement": 1.0,
  "n_annotators": 3,
  "company": "Maroc Telecom",
  "sector": "Télécommunications",
  "doc_type": "indicateurs_trimestriels",
  "period": "2024-T3",
  "source_url": "https://...",
  "split": "train"
}
```

> Les phrases d'exemple de ce guide sont **inventées pour l'illustration**. Les chiffres réels viendront de vos documents.

**Découpage :** train / validation / test (par exemple 70 / 15 / 15). Idéalement, **découpez par document ou par émetteur** pour éviter qu'un modèle « triche » en reconnaissant des formulations d'un même document dans le train et le test.

**Sous-ensembles par accord**, comme l'original : `all_agree`, `75_agree`, `66_agree`, `50_agree`.

### 9.2 Licence et droits
- Les documents sont publics, mais **leur contenu reste protégé**. Publier des phrases isolées à des fins de recherche est une pratique courante (le PhraseBank original est sous licence **CC BY-NC-SA 3.0**).
- Conservez toujours la **source** de chaque phrase.
- Choisissez une licence non commerciale (CC BY-NC-SA 4.0) pour rester prudent.
- Ne publiez pas les PDF eux-mêmes, seulement les phrases et les liens.

### 9.3 Publication
- **Hugging Face Datasets** : créez un dépôt de dataset avec une **dataset card** (README) qui décrit : la motivation, les sources, la méthode d'annotation, l'accord, la distribution des labels, les limites et biais connus.
- **GitHub** : le code (extraction, segmentation, scripts de calcul d'accord, baselines) et le guide d'annotation.
- Optionnel : un court rapport technique ou un article de blog qui raconte la démarche, très efficace pour un CV.

---

## 10. Valoriser le dataset : modèles de référence

Un dataset sans expériences reste abstrait. Entraînez quelques **baselines** et comparez-les (métrique principale : **F1 macro**, adaptée aux classes déséquilibrées) :

| # | Modèle | Ce qu'il montre |
|---|---|---|
| 1 | **Lexique** (règles sur indicateur + direction, section 5.2) | Plancher de performance, très interprétable |
| 2 | **TF-IDF + régression logistique** | Baseline de machine learning classique |
| 3 | **FinBERT anglais** sur phrases traduites | Les modèles anglais suffisent-ils ? |
| 4 | **Modèle multilingue** (XLM-RoBERTa, mDeBERTa) fine-tuné | Apport du multilingue |
| 5 | **Modèle français** (CamemBERT, FlauBERT) fine-tuné | Probablement le meilleur rapport qualité/coût |
| 6 | **LLM en zero-shot / few-shot** | Comparaison avec l'approche moderne sans entraînement |
| 7 | Modèle entraîné sur **Financial PhraseBank traduit** puis testé sur votre dataset | **Expérience clé** : un dataset marocain natif apporte-t-il plus qu'une traduction ? |

L'expérience 7 répond directement à la question « pourquoi créer ce dataset ? ». C'est l'argument central à mettre en avant.

---

## 11. Feuille de route

| Phase | Durée indicative | Résultat |
|---|---|---|
| **0. Apprentissage du domaine** | 1 semaine | Lecture de ce guide, de 5 communiqués de résultats, du papier PhraseBank |
| **1. Collecte** | 1 semaine | 30-50 PDF + `sources.csv` |
| **2. Extraction + segmentation + filtrage** | 1-2 semaines | Pipeline Python → corpus de phrases nettoyées |
| **3. Guide + pilote** | 1 semaine | Guide v1, 100 phrases annotées par 2-3 personnes, premier kappa |
| **4. Annotation** | 3-4 semaines | 1 000 phrases (v1), puis extension vers 2 000-5 000 |
| **5. Consolidation + statistiques** | 1 semaine | Dataset v1 avec labels, accord, splits |
| **6. Baselines** | 2 semaines | Tableau comparatif des modèles |
| **7. Publication** | 1 semaine | Hugging Face + GitHub + README / dataset card |

> **Version minimale publiable :** 1 000 phrases, 2 annotateurs sur 200 d'entre elles, 3 baselines. Mieux vaut un petit dataset propre et bien documenté qu'un gros dataset bâclé.

---

## 12. Glossaire

| Terme | Définition |
|---|---|
| **AMMC** | Autorité Marocaine du Marché des Capitaux, régulateur des marchés |
| **BAM** | Bank Al-Maghrib, banque centrale du Maroc |
| **CA** | Chiffre d'affaires |
| **CAPEX** | Dépenses d'investissement |
| **CES** | Créances en souffrance (crédits non remboursés) |
| **Coefficient d'exploitation** | Charges générales / PNB d'une banque (plus bas = plus efficace) |
| **Coût du risque** | Provisions passées par une banque pour couvrir les crédits douteux |
| **EBE / EBITDA** | Excédent brut d'exploitation, rentabilité avant amortissements |
| **Émetteur** | Entité qui émet des titres (actions, obligations) sur le marché |
| **Gearing** | Endettement net / fonds propres |
| **MASI** | Indice global de la Bourse de Casablanca |
| **MDH / MMDH** | Millions / milliards de dirhams |
| **Note d'information / prospectus** | Document visé par l'AMMC lors d'une émission de titres |
| **OPCVM** | Organisme de placement collectif en valeurs mobilières (fonds d'investissement) |
| **PNB** | Produit net bancaire, l'équivalent du CA pour une banque |
| **Profit warning** | Avertissement sur résultats : annonce de résultats inférieurs aux attentes |
| **REX** | Résultat d'exploitation |
| **RNPG** | Résultat net part du groupe |
| **Sinistralité** | Coût des sinistres pour un assureur |
| --- | --- |
| **Accord inter-annotateurs** | Mesure de la cohérence entre plusieurs annotateurs |
| **Adjudication** | Décision finale d'un expert en cas de désaccord |
| **Baseline** | Modèle de référence simple servant de point de comparaison |
| **Dataset card** | Fiche descriptive d'un dataset (sources, méthode, limites) |
| **F1 macro** | Moyenne du F1 de chaque classe, sans pondération par la taille |
| **Fine-tuning** | Adapter un modèle pré-entraîné à une tâche précise |
| **Segmentation** | Découpage d'un texte en phrases |
| **Zero-shot / few-shot** | Utiliser un modèle sans exemple / avec quelques exemples |

---

## 13. Références

**Article fondateur**
- Malo, P., Sinha, A., Korhonen, P., Wallenius, J., & Takala, P. (2014). *Good debt or bad debt: Detecting semantic orientations in economic texts.* Journal of the Association for Information Science and Technology.

**Modèles**
- Araci, D. (2019). *FinBERT: Financial Sentiment Analysis with Pre-trained Language Models.*
- Martin, L. et al. (2020). *CamemBERT: a Tasty French Language Model.* ACL.
- Le, H. et al. (2020). *FlauBERT: Unsupervised Language Model Pre-training for French.* LREC.

**Méthodologie d'annotation**
- Landis, J. R., & Koch, G. G. (1977). *The measurement of observer agreement for categorical data.* Biometrics.
- Gebru, T. et al. (2021). *Datasheets for Datasets.* Communications of the ACM.

**Sites**
- Bourse de Casablanca : casablanca-bourse.com
- AMMC : ammc.ma
- Bank Al-Maghrib : bkam.ma
- Label Studio : labelstud.io
- Hugging Face Datasets : huggingface.co/datasets

---

*Document de travail : à enrichir au fil du projet, notamment la section 7 (règles du guide) après chaque phase pilote.*
