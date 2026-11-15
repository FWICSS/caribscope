# Done - CaribScope

> Rôle : réalisations vérifiées, chacune avec sa preuve. Mis à jour : 2026-10-18. Prochain identifiant libre : TASK-036.
> Voir aussi : roadmap.md · todo.md · done.md · work-log.md · pending-decision.md · decisions.md · bugs.md · quality-checklist.md

Entrées reconstituées le 2026-10-18 depuis l'historique git (10 commits) et les anciens `TODO.md` et `ROADMAP.md`. Aucun CHANGELOG ni tag. Les correctifs du 2026-09-02 ne figurent pas ici : ils ne sont pas commités (TASK-001).

## 2026-10
### TASK-001 · Relire et commiter le diff local par lots
- Fait le 2026-10-19 : trois lots `6d3dae8` (dépendances et CI), `fb8e908` (head, analytics, KPIs fail-closed, mentions légales), `3829a87` (README, licence, robots, sitemap), puis fusion `ad36b04` avec `origin/master` (Renovate et CI figée), poussée.
- Preuve : `pytest` 90/90 en Python 3.14 avec pandas 3.0.6, plotly 7.1.0, pyarrow 25.0.1 ; `git status` ne liste plus que `pilotage/` et `deploy/COOLIFY.md`, gardés hors du dépôt public (DEC-001).

## 2026-06

### TASK-034 · Étendre les boutons de partage aux cartes Trajectoires, Heatmap, Comparateur et Carte sismique · 2026-06-05
- Réalisé : appel de `share_buttons()` ajouté sur les quatre pages. L'ancien `TODO.md` (ligne 155) et l'ancien `ROADMAP.md` (ligne 66) le donnaient encore à faire.
- Composants : `src/viz/share.py` (`share_buttons()`), pages 1, 4, 6, 12
- Validation : non retrouvée
- Preuve : commit `5fe2802` [vérifié]

### TASK-033 · Lire le PIN KPIs depuis `st.secrets` en plus de l'environnement · 2026-06-03
- Réalisé : `CARIBSCOPE_KPI_PIN` lisible depuis les secrets Streamlit. Le comportement fail-open restait en place à ce commit (BUG-001).
- Composants : `pages/16_📈_KPIs_Internes.py`
- Validation : non retrouvée
- Preuve : commit `f9aa724` [vérifié]

### TASK-032 · Neutraliser l'injection de formule CSV dans la capture email · 2026-06-03
- Réalisé : assainissement des valeurs écrites dans `data/leads/emails.csv`.
- Composants : `src/components/email_capture.py`
- Validation : non retrouvée
- Preuve : commit `fbffa43` [vérifié]

### TASK-031 · Poser la fondation d'acquisition · 2026-06-03
- Réalisé : capture email (home, Ouragan du jour, Saison 2026), helper de partage, page "Saison 2026 en direct" sur le flux NHC `CurrentStorms.json`, dashboard KPIs internes, script Plausible (depuis remplacé par GA4 dans le diff local, DEC-006).
- Composants : `src/components/email_capture.py`, `src/components/analytics.py` (`inject_analytics()`), `src/viz/share.py`, pages 14, 15, 16
- Validation : non retrouvée
- Preuve : commit `f4e606b` [vérifié]
- Origine : TODO.md lignes 138, 139, 155, 161, 191 ; ROADMAP.md lignes 50, 56, 57, 64, 65, 74, 80

## 2026-05

### TASK-030 · Ajouter la page "Ouragan du jour" avec analyses IA · 2026-05-27
- Réalisé : page 14 et correctifs pandas et Streamlit.
- Composants : `pages/14_🌀_Ouragan_du_Jour.py`
- Validation : non retrouvée
- Preuve : commit `4778acd` [vérifié]

### TASK-035 · Configurer Renovate · 2026-05-29
- Réalisé : mises à jour automatisées des dépendances, règles des paquets critiques, migration de configuration.
- Composants : `renovate.json`
- Validation : non retrouvée
- Preuve : commits `dfd7cd7`, `33663ea`, `922a3de` [vérifié]

### TASK-029 · Initialiser l'observatoire caribéen · 2026-05-27
- Réalisé : application Streamlit (trajectoires, statistiques, explorateur, comparateur, analyse, séismes, climat, SST, prédiction Random Forest, dashboard île, heatmap), chargeurs de données, tests pytest.
- Composants : `src/data/loader.py`, `src/analysis/`, `src/ml/` (`build_features()`, `predict_category()`), `src/viz/maps.py` (`plot_track_map()`), `tests/`
- Validation : non retrouvée
- Preuve : commit `223a6fa` [vérifié]
