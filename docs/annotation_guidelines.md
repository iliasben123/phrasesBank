# Guide d'annotation : PhraseBank FR

**Version 1.0 (pilote)**, 26/10/2026

Ce guide est le contrat entre les annotateurs. Deux personnes qui l'appliquent sur la même phrase doivent arriver au même label. Quand ce n'est pas le cas, c'est le guide qu'on corrige, pas l'annotateur.

Tous les exemples sont de **vraies phrases du corpus**. L'identifiant entre crochets renvoie à `data/processed/sentences.jsonl`.

---

## 1. La question à se poser

> **« Si j'étais investisseur dans cette entreprise et que je lisais uniquement cette phrase, penserais-je que la valeur de l'entreprise va plutôt monter, plutôt baisser, ou cela n'a pas d'effet ? »**

Trois principes :

1. **Perspective investisseur.** On juge l'effet sur la valeur de l'entreprise qui publie le document, pas l'émotion du texte ni son effet sur la société.
2. **La phrase seule.** On n'utilise ni les phrases voisines, ni ses connaissances sur l'entreprise, ni le cours de bourse réel.
3. **Ce qui est écrit, pas ce qu'on devine.** Si l'impact n'est ni explicite ni évident, c'est **neutre**.

---

## 2. Les labels

| Label | Quand l'utiliser | Raccourci Label Studio |
|---|---|---|
| **Positif** | Information favorable à la valeur de l'entreprise | `1` |
| **Négatif** | Information défavorable à la valeur de l'entreprise | `2` |
| **Neutre** | Fait sans orientation, chiffre sans comparaison, contexte sans lien explicite avec l'entreprise | `3` |
| **À exclure** | La ligne n'est pas une phrase annotable (voir section 4) | `4` |

**Case « ambigu »** (optionnelle) : à cocher **en plus** du label quand vous avez hésité entre deux labels. Elle ne change pas le label, mais elle aide à repérer les règles à clarifier.

**Commentaire** (optionnel) : une ligne pour expliquer une hésitation. Très utile pendant le pilote.

---

## 3. Procédure de décision

```
1. Est-ce une phrase annotable ?                  non → À EXCLURE (section 4)
          │ oui
2. Parle-t-elle de l'entreprise, de ses filiales,
   ou d'un élément qui l'affecte EXPLICITEMENT ?   non → NEUTRE (section 5.6)
          │ oui
3. Y a-t-il une direction (hausse, baisse,
   comparaison, qualificatif clair) ?              non → NEUTRE (section 5.1)
          │ oui
4. Cette direction est-elle bonne pour
   l'investisseur ? (table section 6)              oui → POSITIF / non → NÉGATIF
          │ plusieurs directions contraires
5. Appliquer la hiérarchie (section 5.3)
```

---

## 4. Ce qui est « à exclure »

| Cas | Exemple |
|---|---|
| Question (interview) | « Un mot pour conclure sur les perspectives de LafargeHolcim Maroc ? » [lhm_2025_rapport_financier_0041] |
| Titre, intitulé de tableau, ligne de tableau | « Tableau : Situation financière à fin 2025 par rapport à fin 2024. » |
| Note de bas de page, renvoi, définition méthodologique | « Le coefficient d'exploitation était de 44,5% (2) Hors don séisme (3) Résultat net/Moyenne total bilan… » [awb_2023_resultats_annuels_0003] |
| Phrase coupée, incompréhensible ou mal extraite du PDF | |
| Texte qui n'est pas en français | |
| Liste de noms, d'adresses ou de filiales sans verbe | « Cie minière d'Oumejrane Maroc 100.00% NC(**) » |

⚠️ **Un intertitre collé au début de la phrase ne suffit pas pour exclure.** Ignorez l'intertitre et annotez la phrase.
Par exemple, *« ACTIVITÉ EN PROGRESSION EN DÉPIT DU CONTEXTE ÉCONOMIQUE DÉFAVORABLE Le produit net bancaire consolidé s'élève à 29,9 milliards de dirhams, en amélioration de 15,5%… »* → **positif**.

---

## 5. Règles pour les cas difficiles

### 5.1 Chiffre sans comparaison → neutre

> « Le Conseil d'Administration propose la distribution d'un dividende de 96 DH par action au titre de l'exercice 2025. » [lhm_2025_rapport_financier_0073] → **neutre**

Sans point de comparaison, on ne sait pas si c'est une bonne ou une mauvaise nouvelle. Même règle pour un chiffre d'affaires, des investissements ou un effectif cités seuls.

### 5.2 Le dividende

| Situation | Label | Exemple |
|---|---|---|
| Montant seul | **Neutre** | [lhm_2025_rapport_financier_0073] ci-dessus |
| Dividende en hausse, ou distribution exceptionnelle en plus | **Positif** | « …propose la mise en distribution à titre exceptionnel d'une somme globale de 94.487.143,00 DH… soit 1 dirham par action. » [csr_2025_rapport_financier_0162] |
| Dividende en baisse ou supprimé | **Négatif** | |
| Dividende cité comme élément comptable (flux de trésorerie, variation des capitaux propres) | **Neutre** | « La distribution des dividendes pour -547.8 MDH ; » |

### 5.3 Phrase mixte : la hiérarchie des indicateurs

Quand une phrase contient des informations de sens contraire, l'indicateur **le plus haut dans la hiérarchie** l'emporte :

1. **Résultat net / RNPG**
2. **Résultat d'exploitation, EBITDA / EBE, EBITA**
3. **Chiffre d'affaires / PNB / marge d'intérêt**
4. **Coûts, coût du risque, indicateurs secondaires (parc clients, volumes…)**

> « Le résultat d'exploitation augmente de 18,6% pour s'établir à 13,8 milliards de dirhams **malgré la progression du coût du risque (+24,9%)**… » [awb_2023_resultats_annuels_0022] → **positif** (le résultat d'exploitation, niveau 2, l'emporte sur le coût du risque, niveau 4)

Si les deux éléments sont **au même niveau** et de force comparable → **neutre** + case **ambigu**.

### 5.4 Éléments exceptionnels et non récurrents

C'est le cas le plus fréquent dans les résultats 2025-2026 (accord Wana Corporate chez Maroc Telecom, redressement fiscal chez Cosumar). Règles :

| Situation | Label | Exemple |
|---|---|---|
| La phrase donne la tendance **hors éléments exceptionnels** | Annoter cette tendance sous-jacente | « Hormis cet élément non récurrent, l'EBITA ressort en hausse de 6,8%… » [iam_2026_s1_rapport_financier_0036] → **positif** |
| | | « Retraité des éléments exceptionnels, le Résultat Net Part du Groupe ressort en amélioration par rapport à l'exercice 2024. » [csr_2025_rapport_financier_0064] → **positif** |
| Baisse expliquée **uniquement** par un produit exceptionnel **de l'année précédente** (effet de base) | **Neutre** + ambigu | « La baisse de l'EBITA par rapport au premier semestre 2025 s'explique principalement par le produit exceptionnel enregistré dans le cadre de l'accord conclu avec Wana Corporate en 2025. » [iam_2026_s1_rapport_financier_0035] |
| Baisse causée par une charge exceptionnelle **de l'année en cours** | **Négatif** (c'est une vraie perte de la période) | « …le Résultat Net Part du Groupe s'établit à 704 MDh, en diminution de 146 MDh… sous l'effet de l'impact du redressement fiscal enregistré en 2025… » [csr_2025_rapport_financier_0063] |

**Pourquoi l'effet de base est neutre :** l'investisseur savait déjà que le produit de l'année précédente ne se répéterait pas. La baisse est mécanique et ne dit rien de la performance actuelle.

### 5.5 Stabilité et faibles variations

| Situation | Label | Exemple |
|---|---|---|
| Stabilité sans qualificatif | **Neutre** | |
| Stabilité qualifiée positivement (« à un niveau élevé », « solide ») ou expliquée par des causes positives | **Positif** | « Le taux de marge d'EBITDA se maintient à un niveau élevé de 50,2%, grâce à la progression du chiffre d'affaires… » [iam_2026_s1_rapport_financier_0033] |
| Variation très faible (< 1 % ou < 1 point) sans commentaire | **Neutre** | « Cosumar a assuré l'approvisionnement de 88,9% du marché national contre 89,5% en 2024. » [csr_2025_rapport_financier_0102] |
| Notation financière **confirmée** sans changement | **Neutre** | « En janvier 2025, Fitch confirme la note d'Attijariwafa bank à BB/Stable… » [awb_2024_rapport_financier_0011] |
| Notation ou perspective **relevée** | **Positif** | « …S&P a relevé les perspectives d'Attijariwafa bank de stable à positive… » [awb_2024_rapport_financier_0019] |

### 5.6 Contexte macroéconomique et de marché

**Règle :** le contexte (économie, inflation, prix des matières premières, climat, marchés des métaux) est **neutre**, **sauf si la phrase relie explicitement ce contexte à l'activité de l'entreprise**.

| Situation | Label | Exemple |
|---|---|---|
| Macro générale | **Neutre** | « L'économie mondiale a démontré une résilience notable en 2024. » [awb_2024_rapport_financier_0024] |
| Prix ou volumes de marché, sans lien écrit avec l'entreprise | **Neutre** | « Ainsi, par rapport à décembre 2023, le prix du Brent a diminué de 3,94 $ le baril… » [awb_2024_rapport_financier_0037] |
| | | « Les achats ont été solides au T1 avec 244 tonnes, puis au T3 avec 220 tonnes… » [mng_2025_rapport_financier_0131] |
| Contexte **explicitement relié** à l'activité de l'entreprise | Selon l'impact | « Les taux de remplissage des barrages… ont atteint des niveaux historiquement bas… **desservant les périmètres de Doukkala et Tadla**. » [csr_2025_rapport_financier_0039] → **négatif** (les zones d'approvisionnement de Cosumar sont nommées) |
| | | « Les précipitations exceptionnelles enregistrées en fin d'année sont un signal encourageant de reprise de performance **pour la production locale**. » [csr_2025_rapport_financier_0025] → **positif** |

⚠️ **Piège :** pour Managem, un cours de l'or record *semble* positif. Mais si la phrase ne parle que du marché de l'or, elle reste **neutre** : on n'ajoute pas de raisonnement absent du texte.

### 5.7 Euphémismes et contexte « difficile »

La communication financière marocaine adoucit les mauvaises nouvelles (voir `GUIDE_PHRASEBANK_FR.md`, section 5). Règles :

| Situation | Label | Exemple |
|---|---|---|
| Description d'un contexte difficile, sans performance | **Neutre** | « Attijariwafa bank publie ses résultats annuels dans un contexte régional et international toujours difficile et incertain… » [awb_2023_resultats_annuels_0004] |
| Formule adoucie qui cache une baisse (« en léger retrait », « se replie », « effet de base défavorable ») | **Négatif** | |
| « Se dégrade », « déficit » | **Négatif** | « Le résultat des opérations de crédit-bail et de location se dégrade enregistrant un déficit de 6,9 millions de dirhams… » [awb_2024_rapport_financier_0250] |

### 5.8 Hausse d'un indicateur « négatif »

Le **verbe ne suffit pas** : c'est le couple *(indicateur, direction)* qui compte (table section 6).

> « Pour leur part, les autres charges bancaires augmentent de 8,4% à 1,9 milliard de dirhams. » [awb_2024_rapport_financier_0254] → **négatif**

### 5.9 Événements d'entreprise sans chiffre

| Situation | Label | Exemple |
|---|---|---|
| Lancement commercial courant, nouvelle offre | **Neutre** | « Lancement au Maroc de l'offre TOD comprenant trois nouvelles formules d'abonnement. » [iam_2026_s1_rapport_financier_0007] |
| Distinction, prix, certification non financière | **Neutre** | « En 2025, LafargeHolcim Maroc a reçu le prix du Fonds Hassan II pour l'Environnement… » [lhm_2025_rapport_financier_0057] |
| Évolution réglementaire dont l'impact n'est pas précisé | **Neutre** | « Symétrie totale des tarifs d'interconnexion mobile à partir du 1er février 2027. » [iam_2026_s1_rapport_financier_0021] |
| Licence, contrat, acquisition, nouvelle capacité **au bénéfice clair** | **Positif** (+ ambigu si le bénéfice n'est pas explicite) | « En Mauritanie, attribution d'une licence 5G à Mauritel pour une durée d'exploitation de dix ans. » [iam_2026_s1_rapport_financier_0013] → positif + ambigu |
| Record, seuil franchi | **Positif** | « Le chiffre d'affaires franchit pour la première fois le seuil des 10 milliards de dirhams… » [mng_2025_rapport_financier_0007] |

### 5.10 Prévisions et perspectives

On annote **l'orientation annoncée**, même si elle est au conditionnel.

- Prévision de croissance de l'entreprise → **positif**
- Prévision de baisse, avertissement → **négatif**
- Mise en garde juridique standard (« ces objectifs pourraient ne pas être réalisés… ») → **neutre**

---

## 6. Table des indicateurs

| Indicateur | Hausse = | Baisse = |
|---|---|---|
| Chiffre d'affaires, PNB, marge d'intérêt, marge sur commissions | 🟢 positif | 🔴 négatif |
| EBITDA / EBE, EBITA, résultat d'exploitation | 🟢 positif | 🔴 négatif |
| Résultat net, RNPG | 🟢 positif | 🔴 négatif |
| Marges (%) | 🟢 positif | 🔴 négatif |
| Dividende | 🟢 positif | 🔴 négatif |
| Parc clients, volumes, parts de marché, production | 🟢 positif | 🔴 négatif |
| Flux de trésorerie opérationnels (CFFO) | 🟢 positif | 🔴 négatif |
| Charges, coûts, coût du risque | 🔴 négatif | 🟢 positif |
| Créances en souffrance, taux de contentialité | 🔴 négatif | 🟢 positif |
| Coefficient d'exploitation | 🔴 négatif | 🟢 positif |
| Endettement net, gearing, dette nette / EBITDA | 🔴 négatif | 🟢 positif |
| Investissements (CAPEX) | ⚪ neutre | ⚪ neutre (sauf commentaire explicite) |

---

## 7. Déroulement du pilote

1. **100 phrases**, tirées au hasard avec le même nombre par secteur (`python -m phrasebank_fr sample`).
2. **Au moins 2 annotateurs**, chacun **seul**, sans discuter, sans regarder les labels de l'autre.
3. Lire ce guide **avant** de commencer, puis le garder ouvert.
4. Compter **20 à 30 minutes** pour 100 phrases. Ne pas rester bloqué : choisir, cocher « ambigu », passer à la suite.
5. Après le pilote :
   - calculer l'accord (Cohen's kappa à 2 annotateurs, Fleiss' kappa à 3 ou plus) ;
   - lister les désaccords et les cases « ambigu » ;
   - discuter chaque désaccord et **modifier ce guide** (nouvelle version, voir section 8) ;
   - objectif : **κ ≥ 0,6**. En dessous, faire un second pilote de 100 phrases avec le guide corrigé.

---

## 8. Historique des versions

| Version | Date | Changements |
|---|---|---|
| 1.0 | 26/10/2026 | Version initiale, écrite à partir des cas rencontrés dans les rapports Attijariwafa bank, Maroc Telecom, LafargeHolcim Maroc, Managem et Cosumar |
