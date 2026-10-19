# 🌀 CaribScope

[![Live Demo](https://img.shields.io/badge/Live-caribscope.fwicss.fr-blue?logo=streamlit)](https://caribscope.fwicss.fr)
[![GitHub Stars](https://img.shields.io/github/stars/FWICSS/caribscope?style=social)](https://github.com/FWICSS/caribscope/stargazers)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Data: NOAA HURDAT2](https://img.shields.io/badge/Data-NOAA%20HURDAT2-orange)](https://www.nhc.noaa.gov/data/)

**Observatoire open source caribéen — 170 ans de données NOAA HURDAT2, séismes USGS, tendances climatiques et prédiction IA, en un seul outil interactif.**

---

## Ce que tu peux explorer

- 🌀 **Trajectoires** — Toutes les trajectoires caribéennes depuis 1851, filtrées par nom, année, décennie ou catégorie Saffir-Simpson
- 📊 **Statistiques** — 170 ans de records : ouragan le plus intense, saisons les plus actives, évolution décennale
- 🔍 **Explorateur** — Profil complet d'un ouragan ou d'une île (Martinique, Guadeloupe, Haïti, Cuba...)
- ⚡ **Comparateur** — Deux ouragans côte à côte (ex : IRMA 2017 vs DEAN 2007)
- 🧪 **Analyse** — Filtrage, agrégation et export CSV personnalisés
- 🌍 **Séismes** — Carte sismique caribéenne + statistiques historiques USGS (M ≥ 2.5)
- 🌡️ **Climat** — Tendances de température et température de surface de l'océan (SST) depuis 1980
- 🤖 **Prédiction IA** — Catégorie Saffir-Simpson prédite par Random Forest (scikit-learn)

---

## Démarrage rapide

```bash
git clone https://github.com/FWICSS/caribscope.git
pip install -r requirements.txt
streamlit run app.py
```

Ouvre `http://localhost:8501`

### Configuration

Toutes les variables sont optionnelles en local. En production, elles se
définissent dans les variables d'environnement de l'hébergeur.

| Variable | Rôle | Défaut |
|---|---|---|
| `GA4_MEASUREMENT_ID` | Identifiant Google Analytics 4 (`G-XXXXXXXXXX`). Vide : aucune mesure d'audience, aucun cookie. | vide |
| `CARIBSCOPE_KPI_PIN` | Code d'accès du tableau de bord interne. **Obligatoire** si `CARIBSCOPE_ENV=production`. | vide |
| `CARIBSCOPE_ENV` | `production` active le refus d'accès au tableau de bord interne sans PIN. | vide |
| `CARIBSCOPE_BASE_URL` | URL publique, utilisée pour les liens canoniques et de partage. | `https://caribscope.fwicss.fr` |

La mesure d'audience n'est chargée qu'après consentement explicite du visiteur
(Consent Mode v2), conformément aux exigences de la CNIL.

---

## Sources de données

| Module | Source | Couverture |
|---|---|---|
| 🌀 Ouragans | [NOAA HURDAT2](https://www.nhc.noaa.gov/data/hurdat/hurdat2-1851-2022-050423.txt) | 1851–2022 · ~1 700 systèmes |
| 🌍 Séismes | [USGS Earthquake Catalog](https://earthquake.usgs.gov/fdsnws/event/1/) | Caraïbes · M ≥ 2.5 |
| 🌡️ SST | Dataset synthétique Caraïbes | 1980–2025 |

Mise à jour annuelle via `scripts/update_hurdat2.py`.

---

## Stack

`Streamlit` · `Plotly` · `pandas` · `scikit-learn` · `Docker` · `Coolify`

---

## Contribuer

```bash
git checkout -b feature/ma-feature
git commit -m "feat: description"
git push origin feature/ma-feature
```

Ouvre une PR vers `develop` — [issues bienvenues](https://github.com/FWICSS/caribscope/issues).

---

## Licence

[MIT](LICENSE) — données NOAA et USGS en accès public.

**Dimitri Aigle** · [GitHub](https://github.com/dimitriaigle) · [LinkedIn](https://linkedin.com/in/dimitriaigle)
