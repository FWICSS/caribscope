# Todo - CaribScope

> Rôle : travail restant, une entrée TASK par tâche. Mis à jour : 2026-10-18. Prochain identifiant libre : TASK-036.
> Voir aussi : roadmap.md · todo.md · done.md · work-log.md · pending-decision.md · decisions.md · bugs.md · quality-checklist.md

Légende : `[vérifié]` constaté dans le code, git ou une sortie de commande ; `[à confirmer]` repris d'un document sans preuve ; `[hypothèse]` déduction de l'agent ; `[reco]` recommandation de l'agent.

Sources reprises : `TODO.md` racine (sections "au prochain lancement" du 2026-09-03 et historique du 2026-06-03), `ROADMAP.md` racine (2026-06-03), `AUDIT_2026-09-02.md`, `deploy/COOLIFY.md`. Ces fichiers sont ignorés par git (`/*.md`) : ils n'ont pas d'historique et restent intacts.

## Fonctionnalités

### TASK-010 · Produire des pages de contenu indexables
- Priorité : P1 · Statut : `À faire` · Jalon : JAL-003
- Description : une page par ouragan notable, par île, `/saison-2026`, home éditoriale, avec `<head>` complet, JSON-LD `Dataset` et `Article`, OG par ouragan, sitemap. Voie à arbitrer : générateur Jinja2 statique (audit 2026-09-02, section 7.1) ou migration hybride Next.js en 5 phases (plan `docs/superpowers/plans/2026-06-03-hybrid-nextjs-streamlit-migration.md`).
- Critères d'acceptation :
  - [ ] `curl` d'une page ouragan renvoie un `<title>` propre à l'ouragan
  - [ ] Inspecteur de partage LinkedIn affiche l'aperçu
- Dépendances : DEC-004 · Origine : TODO.md lignes 97 à 102 et 116 à 121 ; ROADMAP.md lignes 6 à 25 ; audit section 7

### TASK-011 · Créer les templates de visuels "post du jour"
- Priorité : P2 · Statut : `À faire` · Jalon : JAL-004
- Description : Plotly, filigrane et marque `caribscope.fwicss.fr`, réutilisables.
- Critères d'acceptation :
  - [ ] Un visuel généré en une commande pour un ouragan donné
- Dépendances : aucune · Origine : TODO.md ligne 156

### TASK-012 · Automatiser la newsletter quotidienne "Ouragan du jour"
- Priorité : P2 · Statut : `À faire` · Jalon : JAL-004
- Description : cron 7 h, contenu de la page du jour et visuel, envoi à la liste captée.
- Critères d'acceptation :
  - [ ] Un envoi test reçu, désinscription fonctionnelle
- Dépendances : TASK-003 · Origine : TODO.md ligne 166 ; ROADMAP.md ligne 59

### TASK-013 · Générer une image OG dynamique par ouragan
- Priorité : P2 · Statut : `À faire` · Jalon : JAL-003
- Description : PNG 1200x630 par ouragan. Recouvre en partie TASK-010.
- Critères d'acceptation :
  - [ ] Image servie et référencée dans le `<head>` de la page ouragan
- Dépendances : TASK-010 · Origine : TODO.md ligne 167 ; ROADMAP.md ligne 67

### TASK-014 · Publier le lead magnet B2B et sa page de capture
- Priorité : P2 · Statut : `À faire` · Jalon : JAL-004
- Description : PDF "Risque ouragan et séisme 2026, Martinique" contre email professionnel et fonction.
- Critères d'acceptation :
  - [ ] Téléchargement possible après saisie, lead enregistré avec sa source
- Dépendances : TASK-003 · Origine : TODO.md lignes 170 et 171 ; ROADMAP.md ligne 77

### TASK-015 · Lister et contacter 10 journalistes et créateurs caribéens
- Priorité : P1 · Statut : `À faire` · Jalon : JAL-004
- Description : 3 journalistes, 4 comptes météo Antilles, 3 créateurs YouTube ou podcast ; message personnalisé à chacun.
- Critères d'acceptation :
  - [ ] 10 contacts envoyés, consignés dans le work-log
- Dépendances : aucune · Origine : TODO.md lignes 142 et 143 ; ROADMAP.md ligne 46

### TASK-016 · Lancer le format "Ouragan du jour" sur les réseaux
- Priorité : P1 · Statut : `À faire` · Jalon : JAL-004
- Description : premier post LinkedIn, X, Instagram ; comptes `@caribscope` à créer (disponibilité du handle à vérifier) ; objectif 60 posts en 60 jours.
- Critères d'acceptation :
  - [ ] Premier post publié, lien vers l'application
- Dépendances : TASK-011 · Origine : TODO.md lignes 146 et 147 ; ROADMAP.md ligne 62

### TASK-017 · Faire les spikes de visibilité gratuits
- Priorité : P2 · Statut : `À faire` · Jalon : JAL-004
- Description : Awesome Streamlit, Show HN, r/dataisbeautiful, dataset HURDAT2 enrichi sur Kaggle.
- Critères d'acceptation :
  - [ ] Chaque soumission consignée avec son lien
- Dépendances : aucune · Origine : TODO.md lignes 150, 157, 158, 174 ; ROADMAP.md lignes 70 et 71

### TASK-018 · Tenir le tableau quotidien des KPIs
- Priorité : P2 · Statut : `À faire` · Jalon : JAL-004
- Description : feuille quotidienne (date, revenu, nouveaux emails, vues, coût d'acquisition, clients payants). Les vues viendront de GA4, plus de Plausible (DEC-006). Taux dérivés : RPM, CAC, conversion vues vers emails, emails vers démo.
- Critères d'acceptation :
  - [ ] Une ligne par jour sur 7 jours
- Dépendances : TASK-004 · Origine : TODO.md lignes 135 et 188 à 202 ; ROADMAP.md ligne 52

### TASK-022 · Préparer la phase 2 B2B
- Priorité : P3 · Statut : `À faire` · Jalon : JAL-005
- Description : segments assurances, ONG, collectivités, tourisme ; page pricing ; onboarding et dashboard utilisateur ; funnel avancé ; étude de cas média ; événements Caraïbes. Puis phase 3 : duplication géographique, ads, API à pricing tier, recrutement, communauté, structuration. Gelé tant que la phase 1 n'est pas atteinte.
- Critères d'acceptation :
  - [ ] Signal de passage en phase 2 atteint (voir roadmap.md, JAL-004)
- Dépendances : JAL-004 · Origine : TODO.md lignes 178 à 184 ; ROADMAP.md lignes 91 à 119 et 128

## Bugs
- TASK-001 · Corriger BUG-001 (page KPIs publique) par le commit du correctif local puis la configuration de production · P0 · `Fait` (commit `fb8e908`), reste TASK-002

## Sécurité

### TASK-002 · Poser `CARIBSCOPE_ENV` et `CARIBSCOPE_KPI_PIN` en production
- Priorité : P0 · Statut : `Fait` · Jalon : JAL-001
- Description : sans PIN, la nouvelle version refuse d'afficher la page KPIs (fail-closed). PIN aléatoire long, stocké dans Coolify uniquement.
- Critères d'acceptation :
  - [x] Page KPIs inaccessible sans code, vérifié au navigateur en production (2026-10-19 : écran « Code d'accès »)
- Dépendances : TASK-001 · Origine : TODO.md ligne 66 ; audit section 0.1 ; `deploy/COOLIFY.md` section 1

### TASK-006 · Poser les en-têtes de sécurité
- Priorité : P1 · Statut : `À faire` · Jalon : JAL-002
- Description : tous absents depuis l'audit de juin. Option A recommandée par `deploy/COOLIFY.md` : Cloudflare devant ; option B : labels Traefik.
- Critères d'acceptation :
  - [ ] Commande "En-têtes de sécurité présents" de `deploy/COOLIFY.md` renvoie 5
- Dépendances : TASK-001 · Origine : TODO.md ligne 79 ; audit section 4.1

### TASK-019 · Limiter le débit du formulaire email
- Priorité : P2 · Statut : `À faire` · Jalon : JAL-001
- Description : plafond par session et honeypot ; aujourd'hui seule la session Streamlit freine le spam.
- Critères d'acceptation :
  - [ ] Au-delà du plafond, l'inscription est refusée (test)
- Dépendances : aucune · Origine : audit section 4.3 a

## Dette technique

### TASK-005 · Initialiser le versionnage
- Priorité : P2 · Statut : `À faire` · Jalon : JAL-001
- Description : ni CHANGELOG ni tag. Skill `version-bump` après TASK-001. Pas de manifeste de version Python dans le dépôt (pas de `pyproject.toml`) `[vérifié]` : tag git et CHANGELOG seuls.
- Critères d'acceptation :
  - [ ] Tag `v` posé et entrée de CHANGELOG concordante
- Dépendances : TASK-001 · Origine : TODO.md ligne 59

### TASK-020 · Compter la navigation interne dans la mesure d'audience
- Priorité : P2 · Statut : `À vérifier` · Jalon : JAL-004
- Description : l'audit signale que les changements de page internes de Streamlit ne sont pas comptés. Le diff local annonce "tracking des 17 pages" : à vérifier une fois commité.
- Critères d'acceptation :
  - [ ] Navigation entre deux pages visible comme deux pages vues dans GA4
- Dépendances : TASK-001, TASK-004 · Origine : audit section 5.2 ; TODO.md ligne 52

### TASK-021 · Écrire le CHANGELOG des fonctionnalités antérieures, si utile
- Priorité : P3 · Statut : `À faire` · Jalon : -
- Description : facultatif, l'historique git suffit pour les 10 commits existants.
- Critères d'acceptation :
  - [ ] Décision consignée
- Dépendances : TASK-005 · Origine : constat de mise en place 2026-10-18

## Tests

### TASK-023 · Faire tourner la CI sur `master` et sur les pull requests
- Priorité : P1 · Statut : `À vérifier` · Jalon : JAL-001
- Description : au commit `5fe2802`, `ci.yml` ne se déclenche que sur `push` vers `develop` ; Renovate automerge des patches non testés. Le fichier est modifié localement (correctif probable `[hypothèse]`).
- Critères d'acceptation :
  - [ ] Un run CI visible sur une PR Renovate
- Dépendances : TASK-001 · Origine : audit section 4.3 c ; TODO.md ligne 58

## Documentation

### TASK-024 · Remplir l'hébergeur dans les mentions légales
- Priorité : P1 · Statut : `À faire` · Jalon : JAL-001
- Description : dictionnaire `HEBERGEUR` de `pages/17_⚖️_Mentions_Legales.py` (fichier non suivi) avec le fournisseur réel du VPS. Mention obligatoire LCEN art. 6 III.
- Critères d'acceptation :
  - [ ] Plus d'avertissement affiché sur la page
- Dépendances : TASK-001 · Origine : TODO.md lignes 88 à 91

### TASK-025 · Relocaliser la consigne de fusion Karu'lis vers son projet
- Priorité : P2 · Statut : `À faire` · Jalon : -
- Description : consigne notée dans `TODO.md` le 2026-09-03 ("s'il y a deux fois le même point, garder celui de Karulis"), qui ne concerne pas CaribScope. Retrouver le projet, puis préciser les deux sources, la définition du "même point" et le périmètre (arrêts seuls ou aussi horaires et lignes).
- Critères d'acceptation :
  - [ ] Consigne présente dans le pilotage du bon projet, retirée d'ici
- Dépendances : réponse de Dimitri · Origine : TODO.md lignes 8 à 31

## Accessibilité

### TASK-026 · Vérifier les corrections d'accessibilité en production
- Priorité : P2 · Statut : `À vérifier` · Jalon : JAL-001
- Description : `lang="fr"`, contrastes, hiérarchie de titres sont corrigés localement selon `TODO.md` (non commité). Score audit : 88 à 92.
- Critères d'acceptation :
  - [ ] Lighthouse accessibilité 95 ou plus en production
- Dépendances : TASK-001 · Origine : TODO.md ligne 56 ; audit section 3

## Infrastructure et déploiement

### TASK-003 · Monter `/app/data/leads` en volume persistant
- Priorité : P0 · Statut : `À faire` · Jalon : JAL-001
- Description : sinon les inscriptions disparaissent à chaque déploiement. L'audit note "aucun lead capté" trois mois après la mise en ligne : zéro inscription réelle ou volume absent, à trancher.
- Critères d'acceptation :
  - [ ] Une inscription test survit à un redéploiement
- Dépendances : aucune · Origine : TODO.md lignes 71, 72 et 138 ; ROADMAP.md lignes 58 et 126 ; audit section 0.2

### TASK-004 · Créer le flux GA4 et renseigner `GA4_MEASUREMENT_ID`
- Priorité : P1 · Statut : `À faire` · Jalon : JAL-001
- Description : tant qu'il est vide, aucune mesure et aucun cookie. Vérifier ensuite au navigateur qu'aucun cookie `_ga` n'apparaît avant "Accepter".
- Critères d'acceptation :
  - [ ] Événement visible en temps réel dans GA4 après acceptation
  - [ ] Aucun `_ga` avant le choix
- Dépendances : TASK-001, DEC-006 · Origine : TODO.md lignes 69, 70, 92, 93

### TASK-007 · Servir robots.txt et sitemap.xml
- Priorité : P1 · Statut : `À faire` · Jalon : JAL-002
- Description : fichiers générés dans `deploy/` (non suivi), à servir par le proxy.
- Critères d'acceptation :
  - [ ] `robots.txt` en 200 `text/plain`
- Dépendances : TASK-001 · Origine : TODO.md ligne 80 ; `deploy/COOLIFY.md` section 5

### TASK-008 · Passer la redirection http en 301 et ajouter www
- Priorité : P2 · Statut : `À faire` · Jalon : JAL-002
- Description : `http://` redirige en 302, `www.caribscope.fwicss.fr` ne résout pas.
- Critères d'acceptation :
  - [ ] `curl -sI http://...` renvoie 301
- Dépendances : DEC-005 · Origine : TODO.md ligne 81 ; audit section 1.5

### TASK-009 · Inscrire le site dans Google Search Console et Bing Webmaster Tools
- Priorité : P1 · Statut : `À faire` · Jalon : JAL-002
- Description : puis soumettre le sitemap.
- Critères d'acceptation :
  - [ ] Sitemap accepté dans les deux consoles
- Dépendances : TASK-007 · Origine : TODO.md ligne 82 ; `deploy/COOLIFY.md` section 7

### TASK-027 · Sauvegarder les leads chaque jour vers un bucket
- Priorité : P2 · Statut : `À faire` · Jalon : JAL-002
- Description : cron Coolify vers un stockage S3 compatible (Backblaze B2 ou Cloudflare R2 proposés).
- Critères d'acceptation :
  - [ ] Une sauvegarde datée présente et restaurable
- Dépendances : TASK-003 · Origine : TODO.md lignes 84 et 124 ; `deploy/COOLIFY.md` section 8

### TASK-028 · Rendre le build Docker reproductible
- Priorité : P0 · Statut : `Bloquée` · Jalon : JAL-001
- Description : `data/` non versionné, Dockerfile en `COPY . .` : un rebuild depuis GitHub produit une image sans données. À faire avant tout redéploiement.
- Critères d'acceptation :
  - [ ] Une image construite depuis un clone propre démarre et affiche la home
- Dépendances : DEC-003 · Origine : TODO.md lignes 73 à 75 ; audit section 4.3 b ; `deploy/COOLIFY.md` section 3

Numéros TASK-029 à TASK-035 : réalisations archivées dans done.md.
