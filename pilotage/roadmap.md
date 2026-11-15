# Roadmap - CaribScope

> Rôle : direction, jalons et risques de CaribScope. Mis à jour : 2026-10-18. Prochain identifiant libre : JAL-006.
> Voir aussi : roadmap.md · todo.md · done.md · work-log.md · pending-decision.md · decisions.md · bugs.md · quality-checklist.md

Légende : `[vérifié]` constaté dans le code, git ou une sortie de commande ; `[à confirmer]` repris d'un document sans preuve ; `[hypothèse]` déduction de l'agent ; `[reco]` recommandation de l'agent.

Attention, dépôt public (`github.com/FWICSS/caribscope`) : le `.gitignore` exclut volontairement `/*.md` et `docs/` comme "roadmap, specs, contexte non publics". Ce dossier `pilotage/` n'est pas commité tant que DEC-001 n'est pas tranchée.

## Vision
Observatoire open source caribéen : 170 ans de données NOAA HURDAT2, séismes USGS, tendances climatiques et SST, prédiction de catégorie par Random Forest, dans une application Streamlit de 17 pages. Niche de la phase 1 : médias et créateurs francophones Antilles-Caraïbes. Objectif à un an posé dans l'ancien `ROADMAP.md` `[à confirmer]` : première vente B2B (assureur, ONG ou collectivité), liste email de 10 000 inscrits et plus.

Règle posée dans l'ancien `ROADMAP.md` : tant que le MRR vaut zéro, aucune fonctionnalité produit sans lien direct avec l'acquisition ou la rétention (DEC-002).

## État actuel
Constat du 2026-10-18 :
- 10 commits sur `master`, le dernier le 2026-06-05 `[vérifié]`. Aucun tag, aucun CHANGELOG.
- 34 entrées non commitées dans l'arbre de travail (24 fichiers modifiés, 7 non suivis) : correctifs de l'audit du 2026-09-02 (page KPIs fail-closed, GA4 avec Consent Mode v2, mentions légales, accessibilité, précalcul de la home, CI, README, LICENSE, `deploy/`). Tests annoncés 90/90 le 2026-09-02 `[à confirmer]`.
- En production, d'après l'audit du 2026-09-02 : page KPIs internes accessible sans code, en-têtes de sécurité absents, site non indexable (Streamlit sert un document identique à tous les crawlers), domaine parent `fwicss.fr` en 503 `[à confirmer]`, non revérifié le 2026-10-18.
- Build Docker non reproductible depuis git : `data/` non versionné, `COPY . .` dans le Dockerfile `[à confirmer]` (`deploy/COOLIFY.md`, section 3).

## Jalons
| ID | Jalon | Statut | Critère de validation | Dépend de | Tâches |
|---|---|---|---|---|---|
| JAL-001 | Correctifs de l'audit 2026-09-02 commités et déployés | Bloqué | Diff commité par lots, PIN et `CARIBSCOPE_ENV` posés en production, page KPIs fermée vérifiée au navigateur | DEC-003 | TASK-001, TASK-002, TASK-003, TASK-004, TASK-005 |
| JAL-002 | Socle d'exposition publique : en-têtes, robots, sitemap, 301, Search Console | Planifié | Les commandes de la section "Vérification finale" de `deploy/COOLIFY.md` répondent comme attendu | JAL-001 | TASK-006, TASK-007, TASK-008, TASK-009 |
| JAL-003 | Pages de contenu indexables (ouragans, îles, saison) | Planifié | 150 pages indexées Google à 60 jours, OG valide sur LinkedIn et X `[à confirmer]` | DEC-004 | TASK-010 |
| JAL-004 | Phase 1 acquisition | En cours | 1 000 emails, 10 000 vues/mois sur 2 mois, 5 mentions presse, "Ouragan du jour" 60 jours d'affilée `[à confirmer]` | JAL-001 | TASK-011 à TASK-018, TASK-020 |
| JAL-005 | Phase 2 optimisation et premier MRR B2B | Planifié | Première vente B2B signée `[à confirmer]` | JAL-004 | TASK-022 |

Aucune date engagée : tous les jalons sont non datés. La saison cyclonique (juin à novembre) est la fenêtre d'attention visée par l'ancien ROADMAP.

## Fonctionnalités prévues
| Fonctionnalité | Priorité | Jalon | Statut |
|---|---|---|---|
| Pages statiques ou Next.js indexables par ouragan | P1 | JAL-003 | À faire, voie à arbitrer (DEC-004) |
| Newsletter quotidienne "Ouragan du jour" | P2 | JAL-004 | À faire |
| Image OG dynamique par ouragan | P2 | JAL-003 | À faire |
| Templates de visuels "post du jour" | P2 | JAL-004 | À faire |
| Lead magnet B2B "Risque ouragan et séisme 2026" | P2 | JAL-004 | À faire |
| Segments B2B, pricing, onboarding, API | P3 | JAL-005 | Gelé jusqu'à la phase 2 |

## Risques et blocages
- Page KPIs publique en production avec export des emails en clair : risque de violation de données personnelles dès le premier inscrit. Parade : TASK-001, TASK-002.
- Le prochain redéploiement peut casser la production (image sans données). Parade : DEC-003.
- Leads effacés à chaque déploiement si `/app/data/leads` n'est pas un volume. Parade : TASK-003.
- Nom "CaribScope" déjà porté par un magazine de la Caribbean Broadcasting Union, domaine parent en 503 : DEC-005.
- Travail non commité depuis plus de six semaines sur un dépôt public : risque de perte. Parade : TASK-001.

## Prochaines étapes stratégiques
1. Relire et commiter le diff local par lots (JAL-001, TASK-001).
2. Trancher DEC-003 puis poser les variables de production (TASK-002, TASK-003).
3. Trancher DEC-004 : générateur statique Jinja2 ou migration Next.js.
