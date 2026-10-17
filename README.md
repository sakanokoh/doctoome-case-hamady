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

```

Puis « Restart & Run All » : le notebook exécute les fichiers du dossier `sql/`
dans l'ordre et régénère tous les résultats et graphiques.

## Outils

- **DuckDB** pour le SQL, directement sur les fichiers Parquet, sans serveur à installer
- **pandas** pour les manipulations ponctuelles côté Python
- **matplotlib** pour les graphiques


## Organisation du dépôt

| Dossier | Contenu |
|---|---|
| `notebooks/` | l'analyse commentée |

## Hypothèses et choix de nettoyage

### 01_data-quality-check.ipynb
`notebooks/01_data-quality-check.ipynb` contrôle la qualité des données (complétude, unicité, validité, cohérence). Chaque requête est suivie d'un constat, et un récapitulatif final liste les décisions appliquées au nettoyage.

## Réponses aux 4 questions
