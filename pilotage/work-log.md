# Work-log - CaribScope

> Rôle : chronologie des interventions, la plus récente en tête. Mis à jour : 2026-11-14. Prochain identifiant libre : sans objet.
> Voir aussi : roadmap.md · todo.md · done.md · work-log.md · pending-decision.md · decisions.md · bugs.md · quality-checklist.md

## 2026-11-14 · Crédit TAFRAP Studio et page Mentions légales réparée (v0.1.0)
- Agent : Claude Code · Branche : `feat/credit-tafrap` (worktree `../Caribscope-worktrees/credit-tafrap`) · Commits : `42d278f` (fix), `2a03ea8` (feat) · Tag local `v0.1.0`, non poussé.
- Travaux : composant `src/components/credit.py` (« Réalisé par TAFRAP Studio », lien `https://tafrap.fr/?utm_source=caribscope.fwicss.fr&utm_medium=credit&utm_campaign=realisations`, nouvel onglet), affiché en pied de l'accueil et de la page Mentions légales ; test `tests/test_credit.py`. Défaut trouvé en passant : la page Mentions légales appelait `inject_head` sans l'importer (NameError en production), corrigé.
- Tests : pytest 103/103 ; rendu Streamlit (AppTest) de l'accueil et des Mentions légales sans exception, crédit présent.
- Versionnage : premier tag `v0.1.0` (projet jusque-là non versionné). `/*.md` et `docs/` sont exclus du dépôt public : notes de version dans le tag annoté, CHANGELOG local dans `docs/CHANGELOG.md` (non suivi).
- Reste à Dim : relire, pousser la branche et le tag, ouvrir la PR.

## 2026-11-13 · Aperçu de partage : titre et image servis aux robots
- Agent : Claude Code · Branche : `fix/apercu-partage` · Commits : voir `git log` (fix(partage))
- Travaux : `deploy/patch_index_html.py` réécrit l'`index.html` du paquet Streamlit à la construction Docker (titre, `lang="fr"`, description, Open Graph, Twitter card, canonique) ; `scripts/` étant ignoré par git, le script vit dans `deploy/`. Tests `tests/test_patch_index_html.py` sur la coquille réelle (5 verts). `static/og-default.jpg` (carte des trajectoires 1980-2025, catégories 3 à 5, 1200x630) servie par `enableStaticServing`. Vérifié sur l'image construite en local : `<title>` et `og:image` dans le HTML servi, `/app/static/og-default.jpg` en 200.
- Origine : carte admin « Remplacer l'aperçu Streamlit du post CaribScope du 20/11 ».
- Suite (même jour) : PR #19 fusionnée par Dim (`7f1beb3`), déployée par Coolify et vérifiée en ligne (titre, `og:image`, `lang="fr"` dans le HTML servi, image en 200). Reprise : Dim passe l'URL dans l'inspecteur de publication LinkedIn puis réédite le post du 20/11.

## 2026-10-19 · Volume de production constaté
- Agent : Claude Code · Branche : `master` · Commits : aucun (documentation locale)
- Travaux : capture Coolify de Dim : volume `caribscope-data` monté sur `/app/data`. Les leads (`/app/data/leads`) et les données sources y sont déjà persistants ; sections 2 et 3 de `deploy/COOLIFY.md` annotées comme réglées.
- Décisions : pas de montage supplémentaire sur `/app/data/leads`.
- Reprise : activer la sauvegarde du volume ; « Aucun lead capté » relève de l'acquisition, pas d'une perte de données.

## 2026-10-19 · Page KPIs : fermeture par défaut
- Agent : Claude Code · Branche : `master` · Commit : `ff83365`, poussé
- Travaux : vérification au navigateur de `caribscope.fwicss.fr/KPIs_Internes` après pose des variables : page ouverte sans code. Règle inversée : sans PIN, page fermée sauf développement déclaré ; README aligné.
- Composants impactés : page KPIs internes
- Tests : `pytest` 96/96 (6 nouveaux tests d'accès via `streamlit.testing`)
- Blocages : variables Coolify non transmises au conteneur, à vérifier (build seulement, ou redéploiement avant enregistrement)
- Reprise : TASK-002, revérifier la page après redéploiement.

## 2026-10-19 · Commit du diff local par lots et fusion avec origin/master
- Agent : Claude Code · Branche : `master` · Commits : `6d3dae8`, `fb8e908`, `3829a87`, `ad36b04` (fusion), poussés
- Travaux : diff local en attente depuis le 2026-09-02 commité en trois lots ; fusion des PR Renovate #9 et CI #10 venues d'une session cloud. Conflits résolus : versions figées de Renovate gardées, pytest déplacé dans `requirements-dev.txt` ; CI avec déclencheurs develop et master, actions figées par SHA, Python 3.14, fusion automatique limitée aux pushes sur develop.
- Fichiers : `requirements*.txt`, `.github/workflows/ci.yml`, `.gitignore`, `Dockerfile`, `app.py`, `pages/`, `src/`, `README.md`, `LICENSE`, `deploy/robots.txt`, `deploy/sitemap.xml`
- Composants impactés : cartes (plotly 7 compatible grâce à Scattermap et Densitymap), page KPIs (fail-closed), CI
- Décisions : aucune nouvelle ; `pilotage/` et `deploy/COOLIFY.md` restent hors du dépôt public en attendant DEC-001
- Tests : `pytest` 90/90, Python 3.14, venv isolé
- Blocages : le `master` distant installait plotly 7 avec des cartes encore en Scattermapbox (cassées) : corrigé par la fusion. Le KPI fail-closed exige `CARIBSCOPE_KPI_PIN` en production.
- Reprise : TASK-002 (poser `CARIBSCOPE_ENV` et `CARIBSCOPE_KPI_PIN` dans Coolify).

## 2026-10-18 · Mise en place du pilotage projet
- Agent : Claude Code · Branche : `master` · Commits : aucun (base `5fe2802`, pilotage non commité, voir Blocages)
- Travaux : création des 8 fichiers `pilotage/` ; reprise de `TODO.md`, `ROADMAP.md`, `AUDIT_2026-09-02.md` et `deploy/COOLIFY.md` ; confrontation à git (le partage étendu de `5fe2802` était encore listé à faire) ; hook graphify installé ; attribut de fusion placé dans `.git/info/attributes`, `.gitattributes` créé par l'installation retiré.
- Fichiers : `pilotage/*.md` uniquement. `TODO.md` et `ROADMAP.md` laissés intacts : ignorés par git (`/*.md`), sans historique, remplacer leur corps aurait perdu leur contenu. Les 34 entrées non commitées préexistantes ne sont pas touchées.
- Composants impactés : aucun (documentation). Graphe existant du 2026-09-02 ; god nodes : `inject_analytics()`, `inject_head()`, `get_max_category_per_hurricane()`, `get_hurricanes_near_island()`, `build_features()`, `share_buttons()`.
- Décisions : aucune tranchée ; DEC-001 à DEC-006 ouvertes ou à confirmer.
- Tests : non lancés (exécution refusée par l'environnement) ; 90/90 annoncés le 2026-09-02 dans `TODO.md` [à confirmer].
- Blocages : dépôt public dont le `.gitignore` déclare roadmap et contexte "non publics" : pilotage non commité en attendant DEC-001. `core.hooksPath` pointe vers un ancien chemin (`~/Desktop/Dev priority/Hurricane Project/HurricaneProject/.git/hooks`) : l'installation graphify y a créé ce dossier et ses deux hooks, laissés en place.
- Reprise : trancher DEC-001, puis TASK-001 (commiter le diff local par lots).
