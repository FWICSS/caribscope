# Quality checklist - CaribScope

> Rôle : contrôles adaptés à la stack Python / Streamlit / pandas / scikit-learn / Docker Coolify. Mis à jour : 2026-10-18. Prochain identifiant libre : QC-015.
> Voir aussi : roadmap.md · todo.md · done.md · work-log.md · pending-decision.md · decisions.md · bugs.md · quality-checklist.md

## Contrôles permanents
| ID | Contrôle | Commande ou méthode | Statut | Dernier résultat |
|---|---|---|---|---|
| QC-001 | Tests unitaires | `pytest` (`pytest.ini`, `tests/`) | Non vérifié | - (non lancé le 2026-10-18 ; 90/90 annoncés le 2026-09-02 [à confirmer]) |
| QC-002 | Lint et format | - | Non applicable | aucun linter configuré dans le dépôt [hypothèse], à confirmer par `requirements-dev.txt` une fois commité |
| QC-003 | CI GitHub Actions | `.github/workflows/ci.yml` | Échec | au commit `5fe2802`, CI uniquement sur `push` vers `develop` (audit 4.3 c) [à confirmer] |
| QC-004 | Vulnérabilités des dépendances | `pip-audit -r requirements.txt` | Non vérifié | - |
| QC-005 | Secrets | skill `security-audit` ; dépôt public | Non vérifié | - |
| QC-006 | Accès à la page KPIs | navigateur, production | Échec | 2026-09-02, accessible sans code (BUG-001) [à confirmer] |
| QC-007 | En-têtes de sécurité | commande de `deploy/COOLIFY.md`, Vérification finale | Échec | 2026-09-02, tous absents [à confirmer] |
| QC-008 | Indexabilité | `curl` du HTML, `<title>` par page | Échec | 2026-09-02, document identique `<title>Streamlit</title>` [à confirmer] |
| QC-009 | Consentement cookies | navigateur : aucun `_ga` avant "Accepter" | Non vérifié | - |
| QC-010 | Persistance des leads | inscription test puis redéploiement | Non vérifié | - (TASK-003) |
| QC-011 | Build reproductible | build depuis un clone propre | Échec | `data/` non versionné (DEC-003) [à confirmer] |
| QC-012 | Accessibilité | Lighthouse mobile et desktop | Non vérifié | 2026-09-02, 88 à 92 [à confirmer] |
| QC-013 | Cohérence de version | skill `version-bump` | Échec | 2026-10-18, aucun tag ni CHANGELOG |
| QC-014 | Migrations BDD | - | Non applicable | pas de base de données, stockage CSV et parquet |

## Avant livraison
- Diff commité, `pytest` vert, CI déclenchée sur `master`.
- Variables `CARIBSCOPE_ENV`, `CARIBSCOPE_KPI_PIN`, `GA4_MEASUREMENT_ID` présentes dans Coolify, jamais dans git (dépôt public).
- Volumes `/app/data/leads` (et données si DEC-003 A) montés.
- Post-déploiement : les commandes "Vérification finale" de `deploy/COOLIFY.md`, page KPIs contrôlée au navigateur.
- Renvoi : skill `delivery-checklist`.
