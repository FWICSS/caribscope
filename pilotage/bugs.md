# Bugs - CaribScope

> Rôle : anomalies et leur cycle de vie. Mis à jour : 2026-10-18. Prochain identifiant libre : BUG-002.
> Voir aussi : roadmap.md · todo.md · done.md · work-log.md · pending-decision.md · decisions.md · bugs.md · quality-checklist.md

Légende : `[vérifié]` constaté dans le code, git ou une sortie de commande ; `[à confirmer]` repris d'un document sans preuve ; `[hypothèse]` déduction de l'agent ; `[reco]` recommandation de l'agent.

## BUG-001 · La page KPIs internes est accessible sans code en production · Statut : `Corrigé`
- Gravité : bloquante · Priorité : P0
- Environnement : prod `caribscope.fwicss.fr/KPIs_Internes`
- Reproduction : 1. ouvrir la page sans PIN configuré côté Coolify
- Attendu : accès refusé sans code · Observé : page affichée avec bouton de téléchargement de `emails.csv`, selon l'audit du 2026-09-02 (vérifié par l'audit au navigateur) [à confirmer], non revérifié le 2026-10-18
- Cause : `_is_authorized()` de `pages/16_📈_KPIs_Internes.py` en fail-open quand `CARIBSCOPE_KPI_PIN` est absent, et PIN non défini en production (audit section 0.1)
- Correction : correctif fail-closed, limite de tentatives et `hmac.compare_digest` commités (`fb8e908`) et poussés le 2026-10-19 ; reste TASK-002 (PIN en production)
- Constat 2026-10-19 après déploiement : page encore ouverte, les variables posées dans Coolify n'arrivaient pas au conteneur et l'absence de `CARIBSCOPE_ENV` valait développement. Durci (`ff83365`) : fermée sans PIN hors `CARIBSCOPE_ENV=development|dev|local`. Non-régression : `tests/test_kpi_access.py` (6 cas). · Non-régression : aucun test identifié
- Historique : 2026-09-02 relevé et corrigé localement ; 2026-10-18 ouvert dans le pilotage
