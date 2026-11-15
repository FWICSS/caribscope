# Décisions à arbitrer - CaribScope

> Rôle : arbitrages ouverts, l'agent recommande, Dimitri tranche. Mis à jour : 2026-10-18. Prochain identifiant libre : DEC-007.
> Voir aussi : roadmap.md · todo.md · done.md · work-log.md · pending-decision.md · decisions.md · bugs.md · quality-checklist.md

Légende : `[vérifié]` constaté dans le code, git ou une sortie de commande ; `[à confirmer]` repris d'un document sans preuve ; `[hypothèse]` déduction de l'agent ; `[reco]` recommandation de l'agent.

## DEC-001 · Le pilotage d'un dépôt public doit-il être versionné ? · Statut : `À arbitrer`
- Contexte : `github.com/FWICSS/caribscope` est public [vérifié]. Le `.gitignore` exclut `/*.md` et `docs/` comme "roadmap, specs, contexte non publics". `pilotage/` contient roadmap, décisions et constats de sécurité.
- Pourquoi décider : le pilotage n'est pas commité tant que ce n'est pas tranché ; il n'a donc aucune sauvegarde.
- Options :
  - A. Ajouter `pilotage/` au `.gitignore` et le sauvegarder ailleurs : + rien de privé publié / - pas de sauvegarde par git
  - B. Commiter `pilotage/` en assumant sa publication, après retrait des détails de sécurité : + versionné / - expose la roadmap
  - C. Passer le dépôt en privé et publier une vitrine séparée : + tout versionné / - perte de la visibilité open source
- [reco] A à court terme (le `.gitignore` est déjà modifié localement, à faire dans le même commit que TASK-001) ; C à étudier si la vitrine publique reste un objectif.
- Impacts : opérationnel, sécurité
- Sans décision : pilotage non sauvegardé.
- Arbitre : Dimitri Aigle
- Liens : TASK-001

## DEC-002 · Confirmer la règle acquisition-first · Statut : `En analyse`
- Contexte : l'ancien `ROADMAP.md` pose "tant que MRR = 0, zéro feature produit sans lien direct avec l'acquisition ou la rétention" et un backlog gelé jusqu'à la fin de la phase 1. Rien ne dit qui l'a validée.
- Pourquoi décider : elle filtre toutes les tâches de todo.md.
- Options : A. confirmer et la consigner dans decisions.md ; B. la revoir.
- [reco] A, elle est cohérente avec le reste du portefeuille.
- Impacts : fonctionnel
- Sans décision : la règle reste appliquée comme hypothèse de travail.
- Arbitre : Dimitri Aigle
- Liens : JAL-004

## DEC-003 · Comment rendre le build Docker reproductible ? · Statut : `À arbitrer`
- Contexte : `data/` non versionné, Dockerfile en `COPY . .`. Trois sorties dans `deploy/COOLIFY.md`, section 3.
- Pourquoi décider : le prochain redéploiement peut casser la production.
- Options :
  - A. Volume `/app/data` alimenté une fois : + image légère / - étape manuelle à documenter
  - B. Téléchargement NOAA et USGS au démarrage si `data/` est vide : + autonome / - démarrage plus lent, dépendance réseau
  - C. Versionner les données : + simple / - alourdit le dépôt, contraire à la règle "pas de média ou donnée lourde dans git"
- [reco] A, ordre de préférence déjà posé dans `deploy/COOLIFY.md`.
- Impacts : technique, opérationnel
- Sans décision : aucun redéploiement sûr.
- Arbitre : Dimitri Aigle
- Liens : TASK-028, TASK-003

## DEC-004 · Pages indexables : générateur statique Jinja2 ou migration Next.js ? · Statut : `À arbitrer`
- Contexte : `TODO.md` (2026-09-03) dit "Migration Next.js. Décidée." ; l'audit du 2026-09-02 recommande un générateur Jinja2 statique devant Streamlit, 2 à 3 jours, avant toute migration. Les deux documents se contredisent sur l'ordre.
- Pourquoi décider : TASK-010 en dépend, la saison cyclonique se termine fin novembre.
- Options :
  - A. Jinja2 statique d'abord : + premières pages en quelques jours, pipeline réutilisé / - deux surfaces à maintenir
  - B. Migration Next.js en 5 phases : + cible finale / - 3 à 5 jours avant la première page indexable
- [reco] A puis B page par page, comme le propose l'audit ; à confirmer si la décision "Next.js" visait la cible finale et non l'ordre.
- Impacts : technique, SEO, temps
- Sans décision : site toujours non indexable.
- Arbitre : Dimitri Aigle
- Liens : TASK-010, TASK-013

## DEC-005 · Domaine et nom : réparer `fwicss.fr` ou prendre un domaine dédié ? · Statut : `À arbitrer`
- Contexte : `fwicss.fr` en 503, nom "CaribScope" déjà porté par un magazine de la Caribbean Broadcasting Union (audit section 1.5) [à confirmer].
- Pourquoi décider : crédibilité auprès des médias ciblés, redirections et Search Console en dépendent.
- Options : A. réparer `fwicss.fr` ; B. domaine dédié ; C. renommer le produit.
- [reco] pas de recommandation tant que whois AFNIC et INPI (classes 9, 41, 42) ne sont pas consultés : un agent ne peut pas vérifier une disponibilité.
- Impacts : marque, SEO
- Sans décision : TASK-008 et TASK-009 restent sur un domaine fragile.
- Arbitre : Dimitri Aigle
- Liens : TASK-008, TASK-009

## DEC-006 · Confirmer le remplacement de Plausible par GA4 · Statut : `En analyse`
- Contexte : `TODO.md` marque Plausible "OBSOLÈTE au 2026-09-02, remplacé par Google Analytics 4" ; le code commité utilise encore Plausible, le diff local passe en GA4 avec Consent Mode v2.
- Pourquoi décider : GA4 impose un bandeau de consentement et un transfert hors UE ; Plausible ou Umami auto-hébergé l'évitent.
- Options : A. GA4 ; B. Umami auto-hébergé.
- [reco] confirmer A puisque le code est écrit ; noter B comme option si le bandeau pèse sur la conversion.
- Impacts : RGPD, mesure
- Sans décision : TASK-004 reste ouverte.
- Arbitre : Dimitri Aigle
- Liens : TASK-004, TASK-018, TASK-020

## Décisions closes
Aucune au 2026-10-18.
