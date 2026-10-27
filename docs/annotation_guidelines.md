# Guide d'annotation : PhraseBank FR

**Version 1.1**, 27/10/2026

Ce guide est le contrat entre les annotateurs. Deux personnes qui l'appliquent sur la même phrase doivent arriver au même label. Quand ce n'est pas le cas, c'est le guide qu'on corrige, pas l'annotateur.

Tous les exemples sont de **vraies phrases du corpus**. L'identifiant entre crochets renvoie à `data/processed/sentences.jsonl`. La mention *[retirée du corpus]* signale une phrase que le pipeline élimine désormais, mais qui reste un bon exemple si elle apparaît dans un autre document.

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
| Question (interview) | « Un mot pour conclure sur les perspectives de LafargeHolcim Maroc ? » [retirée du corpus] |
| Titre, intitulé de tableau, ligne de tableau | « Tableau : Situation financière à fin 2025 par rapport à fin 2024. » |
| Note de bas de page, renvoi, définition méthodologique | « Le coefficient d'exploitation était de 44,5% (2) Hors don séisme (3) Résultat net/Moyenne total bilan… » [retirée du corpus] |
| Phrase coupée, incompréhensible ou mal extraite du PDF | |
| Texte qui n'est pas en français | |
| Liste de noms, d'adresses ou de filiales sans verbe | « Cie minière d'Oumejrane Maroc 100.00% NC(**) » |
| Phrase **contradictoire** (erreur manifeste dans le document source) | « …Wafa gestion a réalisé un résultat net **en hausse** de 1% **de 93,8 millions à 85,3 millions** de dirhams. » [awb_2024_rapport_financier_d4d746c7] : le texte dit « hausse », les chiffres disent baisse |

⚠️ **Ne corrigez pas le document à la place de l'émetteur.** Si les mots et les chiffres se contredisent, on ne peut pas savoir lequel est faux : la phrase est **à exclure**, même si l'un des deux sens vous semble plus probable.

⚠️ **Un intertitre collé au début de la phrase ne suffit pas pour exclure.** Ignorez l'intertitre et annotez la phrase.
Par exemple, *« ACTIVITÉ EN PROGRESSION EN DÉPIT DU CONTEXTE ÉCONOMIQUE DÉFAVORABLE Le produit net bancaire consolidé s'élève à 29,9 milliards de dirhams, en amélioration de 15,5%… »* → **positif**.

---

## 5. Règles pour les cas difficiles

### 5.1 Chiffre sans comparaison → neutre

> « Le Conseil d'Administration propose la distribution d'un dividende de 96 DH par action au titre de l'exercice 2025. » [lhm_2025_rapport_financier_d553d189] → **neutre**

Sans point de comparaison, on ne sait pas si c'est une bonne ou une mauvaise nouvelle. Même règle pour un chiffre d'affaires, des investissements ou un effectif cités seuls.

### 5.2 Le dividende

| Situation | Label | Exemple |
|---|---|---|
| Montant seul | **Neutre** | [lhm_2025_rapport_financier_d553d189] ci-dessus |
| Dividende en hausse, ou distribution exceptionnelle en plus | **Positif** | « …propose la mise en distribution à titre exceptionnel d'une somme globale de 94.487.143,00 DH… soit 1 dirham par action. » [csr_2025_rapport_financier_03692a9f] |
| Dividende en baisse ou supprimé | **Négatif** | |
| Dividende cité comme élément comptable (flux de trésorerie, variation des capitaux propres) | **Neutre** | « La distribution des dividendes pour -547.8 MDH ; » |

### 5.3 Phrase mixte : la hiérarchie des indicateurs

Quand une phrase contient des informations de sens contraire, l'indicateur **le plus haut dans la hiérarchie** l'emporte :

1. **Résultat net / RNPG**
2. **Résultat d'exploitation, EBITDA / EBE, EBITA**
3. **Chiffre d'affaires / PNB / marge d'intérêt**
4. **Coûts, coût du risque, indicateurs secondaires (parc clients, volumes…)**

> « Le résultat d'exploitation augmente de 18,6% pour s'établir à 13,8 milliards de dirhams **malgré la progression du coût du risque (+24,9%)**… » [awb_2023_resultats_annuels_6a20db52] → **positif** (le résultat d'exploitation, niveau 2, l'emporte sur le coût du risque, niveau 4)

Si les deux éléments sont **au même niveau** et de force comparable → **neutre** + case **ambigu**.

### 5.4 Éléments exceptionnels et non récurrents

C'est le cas le plus fréquent dans les résultats 2025-2026 (accord Wana Corporate chez Maroc Telecom, redressement fiscal chez Cosumar). Règles :

| Situation | Label | Exemple |
|---|---|---|
| La phrase donne la tendance **hors éléments exceptionnels** | Annoter cette tendance sous-jacente | « Hormis cet élément non récurrent, l'EBITA ressort en hausse de 6,8%… » [iam_2026_s1_rapport_financier_da9a0280] → **positif** |
| | | « Retraité des éléments exceptionnels, le Résultat Net Part du Groupe ressort en amélioration par rapport à l'exercice 2024. » [csr_2025_rapport_financier_f495f7ce] → **positif** |
| Baisse expliquée **uniquement** par un produit exceptionnel **de l'année précédente** (effet de base) | **Neutre** + ambigu | « La baisse de l'EBITA par rapport au premier semestre 2025 s'explique principalement par le produit exceptionnel enregistré dans le cadre de l'accord conclu avec Wana Corporate en 2025. » [iam_2026_s1_rapport_financier_ad0a3f68] |
| Baisse causée par une charge exceptionnelle **de l'année en cours** | **Négatif** (c'est une vraie perte de la période) | « …le Résultat Net Part du Groupe s'établit à 704 MDh, en diminution de 146 MDh… sous l'effet de l'impact du redressement fiscal enregistré en 2025… » [csr_2025_rapport_financier_6c1ea9b2] |

**Pourquoi l'effet de base est neutre :** l'investisseur savait déjà que le produit de l'année précédente ne se répéterait pas. La baisse est mécanique et ne dit rien de la performance actuelle.

**Même avec un mot fort.** La règle s'applique aussi quand la phrase dit « forte baisse », dès lors que **la seule explication donnée** est l'élément exceptionnel de l'année précédente :

> « Au premier semestre 2026, le Résultat Net Part du Groupe atteint 2 482 millions de dirhams, **en forte baisse** par rapport à la même période en 2025, **qui avait enregistré des recettes exceptionnelles** dans le cadre de l'accord conclu avec Wana Corporate. » [iam_2026_s1_rapport_financier_f6439053] → **neutre** + ambigu

Si la phrase cite **aussi** une cause opérationnelle (« …et du recul de l'activité mobile »), la baisse n'est plus seulement mécanique → **négatif**.

### 5.5 Stabilité et faibles variations

| Situation | Label | Exemple |
|---|---|---|
| Stabilité sans qualificatif | **Neutre** | |
| Stabilité qualifiée positivement (« à un niveau élevé », « solide ») ou expliquée par des causes positives | **Positif** | « Le taux de marge d'EBITDA se maintient à un niveau élevé de 50,2%, grâce à la progression du chiffre d'affaires… » [iam_2026_s1_rapport_financier_682a2885] |
| Variation très faible (< 1 % ou < 1 point) sans commentaire | **Neutre** | « Cosumar a assuré l'approvisionnement de 88,9% du marché national contre 89,5% en 2024. » [csr_2025_rapport_financier_1c086a5a] |
| Notation financière **confirmée** sans changement | **Neutre** | « En janvier 2025, Fitch confirme la note d'Attijariwafa bank à BB/Stable… » [awb_2024_rapport_financier_467d16b9] |
| Notation ou perspective **relevée** | **Positif** | « …S&P a relevé les perspectives d'Attijariwafa bank de stable à positive… » [awb_2024_rapport_financier_5939ab4c] |

### 5.6 Contexte macroéconomique et de marché

**Règle :** le contexte (économie, inflation, prix des matières premières, climat, marchés des métaux) est **neutre**, **sauf si la phrase relie explicitement ce contexte à l'activité de l'entreprise**.

| Situation | Label | Exemple |
|---|---|---|
| Macro générale | **Neutre** | « L'économie mondiale a démontré une résilience notable en 2024. » [awb_2024_rapport_financier_c653d8c7] |
| Prix ou volumes de marché, sans lien écrit avec l'entreprise | **Neutre** | « Ainsi, par rapport à décembre 2023, le prix du Brent a diminué de 3,94 $ le baril… » [awb_2024_rapport_financier_84b069d6] |
| | | « Les achats ont été solides au T1 avec 244 tonnes, puis au T3 avec 220 tonnes… » [retirée du corpus] |
| Contexte **explicitement relié** à l'activité de l'entreprise | Selon l'impact | « Les taux de remplissage des barrages… ont atteint des niveaux historiquement bas… **desservant les périmètres de Doukkala et Tadla**. » [csr_2025_rapport_financier_83a9a346] → **négatif** (les zones d'approvisionnement de Cosumar sont nommées) |
| | | « Les précipitations exceptionnelles enregistrées en fin d'année sont un signal encourageant de reprise de performance **pour la production locale**. » [csr_2025_rapport_financier_9595eb7d] → **positif** |

⚠️ **Piège :** pour Managem, un cours de l'or record *semble* positif. Mais si la phrase ne parle que du marché de l'or, elle reste **neutre** : on n'ajoute pas de raisonnement absent du texte.

Ces cas ont produit la majorité des hésitations du pilote. Ils sont tous **neutres** :

| Type de phrase | Exemple du pilote |
|---|---|
| Changes et devises | « …l'USDMAD a chuté de 11,20%. » |
| Politique monétaire | « En début d'année, la Fed a maintenu un biais restrictif alors que la BCE a accéléré son assouplissement, ce qui a pesé sur l'euro. » |
| Cours d'une matière première, même très commentés | « Au printemps, la hausse s'est prolongée jusqu'à un sommet de clôture proche de $3424… » |
| Perspectives d'un marché, pas de l'entreprise | « Les perspectives pour 2026 et au-delà restent favorables en volume pour l'électrification, mais moins intensives en cobalt par véhicule. » |
| Sensibilité générale aux risques | « Ces projections restent sensibles aux fluctuations des cours des matières premières… » [awb_2024_rapport_financier_b11adb6d] |

**Test rapide :** remplacez mentalement le nom de l'entreprise par celui d'un concurrent. Si la phrase reste aussi vraie, elle ne parle pas de l'entreprise → **neutre**.

> Depuis la v1.1, les pages de revue des marchés du rapport Managem (p. 60 à 65) ne sont plus extraites : ces phrases n'apparaîtront plus dans les prochains lots. Les exemples ci-dessus n'ont donc pas d'identifiant.

### 5.7 Euphémismes et contexte « difficile »

La communication financière marocaine adoucit les mauvaises nouvelles (voir `GUIDE_PHRASEBANK_FR.md`, section 5). Règles :

| Situation | Label | Exemple |
|---|---|---|
| Description d'un contexte difficile, sans performance | **Neutre** | « Attijariwafa bank publie ses résultats annuels dans un contexte régional et international toujours difficile et incertain… » [awb_2023_resultats_annuels_70f94b49] |
| Formule adoucie qui cache une baisse (« en léger retrait », « se replie », « effet de base défavorable ») | **Négatif** | |
| « Se dégrade », « déficit » | **Négatif** | « Le résultat des opérations de crédit-bail et de location se dégrade enregistrant un déficit de 6,9 millions de dirhams… » [awb_2024_rapport_financier_d7ababf9] |

### 5.8 Hausse d'un indicateur « négatif »

Le **verbe ne suffit pas** : c'est le couple *(indicateur, direction)* qui compte (table section 6).

> « Pour leur part, les autres charges bancaires augmentent de 8,4% à 1,9 milliard de dirhams. » [awb_2024_rapport_financier_8d92fae0] → **négatif**

### 5.9 Événements d'entreprise sans chiffre

| Situation | Label | Exemple |
|---|---|---|
| Lancement commercial courant, nouvelle offre | **Neutre** | « Lancement au Maroc de l'offre TOD comprenant trois nouvelles formules d'abonnement. » [iam_2026_s1_rapport_financier_9a1ead2c] |
| Distinction, prix, certification non financière | **Neutre** | « En 2025, LafargeHolcim Maroc a reçu le prix du Fonds Hassan II pour l'Environnement… » [lhm_2025_rapport_financier_d7c92939] |
| Évolution réglementaire dont l'impact n'est pas précisé | **Neutre** | « Symétrie totale des tarifs d'interconnexion mobile à partir du 1er février 2027. » [iam_2026_s1_rapport_financier_0d61bac6] |
| Licence, contrat, acquisition, nouvelle capacité **au bénéfice clair** | **Positif** (+ ambigu si le bénéfice n'est pas explicite) | « En Mauritanie, attribution d'une licence 5G à Mauritel pour une durée d'exploitation de dix ans. » [iam_2026_s1_rapport_financier_0136ff93] → positif + ambigu |
| Record, seuil franchi | **Positif** | « Le chiffre d'affaires franchit pour la première fois le seuil des 10 milliards de dirhams… » [mng_2025_rapport_financier_b05dedb9] |

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
   - exporter les annotations de chacun (Label Studio → **Export** → **JSON**) dans `data/annotations/` ;
   - calculer l'accord (Cohen's kappa à 2 annotateurs, Fleiss' kappa à 3 ou plus) et lister les désaccords et les cases « ambigu » :
     ```
     python -m phrasebank_fr agreement data/annotations/annotateur1.json data/annotations/annotateur2.json
     ```
     Le fichier `data/annotations/desaccords.csv` s'ouvre dans Excel. Les colonnes `decision` et `regle_du_guide` servent à noter le résultat de la discussion ;
   - discuter chaque désaccord et **modifier ce guide** (nouvelle version, voir section 8) ;
   - objectif : **κ ≥ 0,6**. En dessous, faire un second pilote de 100 phrases avec le guide corrigé.

---

## 8. Historique des versions

| Version | Date | Changements |
|---|---|---|
| 1.0 | 26/10/2026 | Version initiale, écrite à partir des cas rencontrés dans les rapports Attijariwafa bank, Maroc Telecom, LafargeHolcim Maroc, Managem et Cosumar |
| 1.1 | 27/10/2026 | Après le pilote annoté par un premier annotateur (12 phrases marquées ambiguës sur 100). Ajouts : phrase contradictoire → à exclure (section 4) ; effet de base même avec « forte baisse » (5.4) ; changes, politique monétaire, perspectives de marché et test du concurrent (5.6) ; commande `agreement` (section 7). Identifiants de phrases stables, dérivés du texte |
