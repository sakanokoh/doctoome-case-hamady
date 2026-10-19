# Étude de cas Doctoome – Questionnaire diabète de type 2

Analyse réalisée par Hamady Sakanoko dans le cadre du processus de recrutement
Data Engineer / Data Analyst. Les consignes d'origine sont dans `README_init.md`
et `README_init_FR.md`, les données (synthétiques) fournies dans `data/`.

## Reproduire l'analyse

J'ai travaillé avec Python 3.11.9 sous Windows. Pour tout relancer depuis zéro :

```bash
git clone https://github.com/sakanokoh/doctoome-case-hamady.git
cd doctoome-case-hamady
python -m venv VotreNomEnvVirtuel
VotreNomEnvVirtuel\Scripts\activate        
pip install -r requirements.txt
jupyter notebook
```

Puis exécuter les notebooks dans l'ordre, avec « Restart & Run All » :
1. `notebooks/01_data-quality-check.ipynb` : contrôles qualité
2. `notebooks/02_data-cleaning.ipynb` : nettoyage, écrit `data_clean/` (non versionné, régénéré ici)
3. `notebooks/03_data-analysis.ipynb` : analyse, écrit les graphiques dans `figures/`


Puis « Restart & Run All » : le notebook exécute les fichiers du dossier `sql/`
dans l'ordre et régénère tous les résultats et graphiques.

## Outils

- **DuckDB** pour le SQL, directement sur les fichiers Parquet, sans serveur à installer
- **pandas** pour les manipulations ponctuelles côté Python
- **matplotlib** pour les graphiques


## Organisation du dépôt

| Dossier | Contenu |
|---|---|
| `data/` | données fournies (Parquet), jamais modifiées |
| `notebooks/` | les 3 notebooks : qualité, nettoyage, analyse |
| `figures/` | graphiques produits par le notebook 03 |
| `presentation/` | slides (PDF et PowerPoint) |


## Démarche et priorités 

Doctoome mène des campagnes d'acquisition (Google Ads, réseaux sociaux, email) et veut que les personnes concernées aillent jusqu'au résultat. J'ai choisi les axes selon une question : **qu'est-ce qui aide Doctoome à décider ?**

| Piste | Choix | Pourquoi |
|---|---|---|
| Qualité des données | En premier (notebooks 01-02) | Sans elle, aucun chiffre n'est fiable |
| Funnel | Priorité 1 | Montre où l'on perd les gens, donc où agir vite |
| Acquisition | Priorité 2 | Savoir quel canal rapporte des résultats permet d'arbitrer entre les campagnes |
| Démographie | Priorité 3 | Vérifie que le trafic atteint le public concerné, pas seulement du volume |
| Comportement | Intégré au Funnel | Les abandons et l'appareil utilisé sont le comportement observable |
| Évolution | En contexte | 9 semaines ne suffisent pas pour conclure à une tendance |
| Réponses détaillées | Écartée | Le résultat en découle directement ; données de santé sensibles |


## Hypothèses et choix de nettoyage

#### 01_data-quality-check.ipynb
`notebooks/01_data-quality-check.ipynb` contrôle la qualité des données (complétude, unicité, validité, cohérence). Chaque requête est suivie d'un constat, et un récapitulatif final liste les décisions appliquées au nettoyage.

#### 02_data-cleaning.ipynb
`notebooks/02_data-cleaning.ipynb` applique ces décisions, écrit les tables propres dans `data_clean/` et construit `sessions_analysis` (une ligne par session) pour l'analyse.

#### 03_data-analysis.ipynb**
`notebooks/03_data-analysis.ipynb` part uniquement de `sessions_analysis`. Choix de calcul : le taux de résultat est rapporté aux arrivées (sessions) ; la part de `possible_risk` est rapportée aux résultats ; les semaines commencent le lundi ; les tranches `under_18` (60 sessions) et `unknown` sont exclues du graphique par âge, car trop petites ou non interprétables.


### Hypothèses pouvant affecter les conclusions :
- La dernière réponse est la bonne : elle est cohérente avec le résultat dans tous les cas (vérifié au notebook 01).
- Une session sans résultat est comptée comme non terminée, y compris les 105 qui ont répondu aux 5 questions. S'il s'agit d'un défaut d'enregistrement, le taux de résultat passerait de 43.7 % à 44.1 % : l'impact est faible.
- Les 219 sessions `direct` venues du retargeting restent en `direct` : le retargeting est donc mieux mesuré par campagne que par source.
- L'âge est calculé à ± 1 an, à partir de l'année de naissance seulement.
- Les liens observés (mobile et Q4, canal et taux de résultat) sont des corrélations, pas des causes prouvées.

## Recommandations

1. **Vérifier l'affichage de la Q4 sur mobile**, puis tester une version simplifiée (moins de choix, libellés plus courts) auprès d'une partie des visiteurs.
2. **Renforcer les canaux qui transforment le mieux** (email, liens depuis d'autres sites, assistants IA) et revoir `diabetes_social_awareness`, la campagne la plus faible.
3. **Étendre la logique de `diabetes_45plus`** : c'est le ciblage par l'âge qui ramène le public concerné.
4. **Mieux mesurer** : enregistrer le coût de chaque canal, indiquer la source sur tous les liens, et relier la fin du questionnaire à un bouton « Valider mes réponses » pour expliquer les 105 sessions sans résultat.

## Réponses aux 4 questions

### 1. Quels sont les résultats les plus importants ?
- **43.7 % des visiteurs obtiennent un résultat.** Les deux plus grosses pertes : 35.5 % repartent sans commencer, et 13.5 % abandonnent entre Q3 et Q4.
- **La perte à la Q4 vient surtout du mobile** (64.5 % du trafic) : 16.9 % de perte, contre 8.0 % sur ordinateur.
- **Volume ≠ qualité** : Google apporte la moitié du trafic mais transforme moins (39.0 à 43.1 %) que l'email (64.7 %), les liens depuis d'autres sites (referral, 60.4 %) et les assistants IA (52.9 %). Les réseaux sociaux sont le canal le plus faible (28.9 %).
- **`diabetes_45plus` touche le bon public** : 87.9 % de 45 ans et plus, 39.5 % de `possible_risk`, soit 21.7 % de tous les `possible_risk` avec 12.8 % du trafic.
- **L'âge est le seul levier de ciblage** : la part de `possible_risk` passe de 8.4 % (18-24 ans) à 33.7 % (65 ans et plus). La région et le genre ne font pas de différence.
- **Le trafic (+68 %) et le taux de résultat (40.0 % → 47.1 %) progressent** sur les 9 semaines, sans que `diabetes_45plus` l'explique.

### 2. Quelles questions restent sans réponse ?
- Pourquoi 35.5 % des visiteurs partent sans commencer ? Les données ne disent rien de ce qu'ils voient sur la page.
- La perte à la Q4 sur mobile vient-elle de l'affichage ? On observe un lien, pas une cause.
- Les 105 sessions qui ont répondu aux 5 questions sans résultat : abandon ou problème technique ?
- Quelle est la vraie source des 219 sessions `direct` venues de la campagne de retargeting ?
- Qu'est-ce qui fait monter le taux de résultat au fil des semaines ?
- Que font les personnes après leur résultat ? Le questionnaire ne mesure pas la suite.
- Les données couvrent seulement 9 semaines d'un même été : on ne peut pas distinguer une vraie progression d'un effet de saison.

### 3. Quelles données supplémentaires collecteriez-vous ?
- **Le coût de chaque canal et campagne**, pour calculer un coût par résultat et par `possible_risk`.
- **La source complète sur tous les liens** (`utm_source`, `utm_medium`), avec le réseau social précis.
- **Le comportement sur la page d'accueil** : temps passé, défilement, pour comprendre les 35.5 % qui ne commencent pas.
- **La taille d'écran**, pour vérifier l'hypothèse d'un problème d'affichage de la Q4 sur mobile.
- **Les clics vers une offre de soins après le résultat**, pour mesurer ce que le questionnaire déclenche.

### 4. Que recommanderiez-vous de suivre si le questionnaire restait actif pendant 12 mois ?
- **Chaque semaine** : taux de début, taux de résultat et perte entre Q3 et Q4, par appareil, en particulier avant et après une version simplifiée de la Q4.
- **Par canal et par campagne** : taux de résultat, part de `possible_risk`, et coût par résultat une fois les coûts disponibles.
- **Le ciblage** : part des 45 ans et plus et de `possible_risk` dans chaque campagne.
- **Après le résultat** : part des personnes qui cliquent vers une offre de soins.
- **La qualité de la mesure** : écart entre « 5 réponses » et « résultat », part du trafic sans source fiable, doublons et libellés mal écrits.
- **La saisonnalité** : l'évolution mois par mois sur l'année complète, pour distinguer une vraie progression d'un effet de saison.
