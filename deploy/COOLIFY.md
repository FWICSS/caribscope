# Ce qu'il reste à faire sur Coolify

État vérifié en production le 2026-09-02. Rien de ce qui suit ne demande de
changement de code : tout se règle dans l'interface Coolify ou devant elle.
Ces réglages restent valables après la migration Next.js, puisqu'ils vivent au
niveau du reverse proxy et du DNS.

Ordre volontaire : du plus urgent au plus confortable.

---

## 1. Variables d'environnement (5 min) — BLOQUANT

Application → Environment Variables. Sans la première, le tableau de bord
interne refusera désormais de s'afficher, et sans la deuxième vous n'aurez
aucune mesure d'audience.

| Variable | Valeur | Pourquoi |
|---|---|---|
| `CARIBSCOPE_ENV` | `production` | Active le refus d'accès au tableau de bord interne quand le PIN manque |
| `CARIBSCOPE_KPI_PIN` | une chaîne longue et aléatoire | Protège l'export des emails. **Obligatoire** dès que `CARIBSCOPE_ENV=production` |
| `GA4_MEASUREMENT_ID` | `G-XXXXXXXXXX` | Identifiant Google Analytics 4. Laisser vide désactive proprement toute mesure |
| `CARIBSCOPE_BASE_URL` | `https://caribscope.fwicss.fr` | URL canonique et liens de partage |

Générer le PIN :

```bash
openssl rand -base64 24
```

Le comportement est *fail-closed* (renforcé le 2026-10-19 : la page est fermée sans PIN dès que `CARIBSCOPE_ENV` ne vaut pas `development`) : si `CARIBSCOPE_ENV=production` et
que le PIN est absent, la page affiche « Page indisponible » au lieu de s'ouvrir
en grand comme aujourd'hui.

**Créer le flux GA4 avant** : Google Analytics → Admin → Flux de données → Web →
`caribscope.fwicss.fr`. L'identifiant `G-…` est affiché à la création.

---

## 2. Volume persistant pour les leads (10 min) — BLOQUANT

> **Réglé, constaté le 2026-10-19** : un volume `caribscope-data` est monté sur
> `/app/data` dans Coolify. `data/leads/` en fait partie, les inscriptions
> survivent donc aux redéploiements. Ne pas ajouter de montage sur
> `/app/data/leads` (doublon) et ne jamais supprimer ce volume.

Aujourd'hui `data/leads/emails.csv` vit dans le système de fichiers du
conteneur : **chaque redéploiement efface les inscriptions**. C'est la première
explication du « Aucun lead capté » affiché en production.

Application → Storages → Add → Volume Mount :

| Champ | Valeur |
|---|---|
| Name | `caribscope-leads` |
| Source (host) | `/data/coolify/caribscope/leads` |
| Destination (container) | `/app/data/leads` |

Redéployer, puis vérifier depuis le serveur :

```bash
ls -la /data/coolify/caribscope/leads/
```

---

## 3. Le point à clarifier avant tout redéploiement (30 min) — RISQUE

> **Tranché, constaté le 2026-10-19** : l'option 1 est en place, les données
> sources vivent dans le volume `caribscope-data` monté sur `/app/data`, pas dans
> l'image. Deux redéploiements du 2026-10-19 depuis GitHub ont fonctionné.
> Reste à faire : sauvegarder ce volume (bouton Backup de Coolify).

`data/` n'est pas versionné (`git ls-files data/` renvoie 0 fichier) et le
Dockerfile fait `COPY . .`. Si Coolify construit l'image depuis le dépôt GitHub,
l'image n'aura **aucune donnée** : `start.sh` sautera le précalcul et
l'application plantera au premier chargement.

Que la production fonctionne aujourd'hui signifie que l'image tourne sur un
contexte de build qui contenait les données. Autrement dit : **le build n'est
pas reproductible, et le prochain redéploiement peut casser le site.**

Trois sorties possibles, par ordre de préférence :

1. **Volume de données** : monter `/app/data` comme les leads, et y déposer les
   CSV sources une fois. Le conteneur devient sans état, l'image légère.
2. **Téléchargement au démarrage** : `start.sh` récupère HURDAT2 depuis la NOAA
   et le catalogue USGS si `data/` est vide. Plus propre, plus lent au boot.
3. **Versionner les données** : simple, mais alourdit le dépôt et contredit la
   raison pour laquelle elles ont été retirées de git.

À trancher **avant** le prochain déploiement, pas pendant.

---

## 4. Headers de sécurité (20 min)

Toujours tous absents en production, signalés dès l'audit de juin. Ce sont des
en-têtes statiques, aucun impact applicatif.

### Option A, recommandée : Cloudflare devant (règle aussi les points 5 et 6)

Passer le DNS de `caribscope.fwicss.fr` en proxy Cloudflare (nuage orange), puis
Rules → Transform Rules → Modify Response Header, avec ces six entrées :

```
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=(), interest-cohort=()
Cross-Origin-Opener-Policy: same-origin
```

### Option B : labels Traefik dans Coolify

Application → Advanced → Custom Labels :

```
traefik.http.middlewares.caribscope-sec.headers.stsSeconds=31536000
traefik.http.middlewares.caribscope-sec.headers.stsIncludeSubdomains=true
traefik.http.middlewares.caribscope-sec.headers.contentTypeNosniff=true
traefik.http.middlewares.caribscope-sec.headers.frameDeny=false
traefik.http.middlewares.caribscope-sec.headers.customFrameOptionsValue=SAMEORIGIN
traefik.http.middlewares.caribscope-sec.headers.referrerPolicy=strict-origin-when-cross-origin
traefik.http.middlewares.caribscope-sec.headers.customResponseHeaders.Permissions-Policy=geolocation=(), microphone=(), camera=()
traefik.http.routers.caribscope.middlewares=caribscope-sec@docker
```

Le nom du routeur (`caribscope`) doit correspondre à celui que Coolify génère :
le relever dans les labels existants avant d'ajouter la dernière ligne.

**Pas de Content-Security-Policy pour l'instant.** Streamlit utilise des scripts
inline, un WebSocket et des iframes de composants : une CSP écrite trop vite
casserait l'application. À poser au moment de la migration Next.js, où le
périmètre est maîtrisé.

Vérification :

```bash
curl -sSI https://caribscope.fwicss.fr/ | grep -iE "strict-transport|x-content-type|x-frame|referrer|permissions"
```

---

## 5. robots.txt et sitemap.xml (20 min)

Aujourd'hui les deux URLs renvoient le shell HTML de Streamlit en HTTP 200.
Lighthouse le signale : « robots.txt is not valid ».

Streamlit ne sait pas servir de fichier statique à la racine, donc cela se règle
devant. Les deux fichiers sont prêts dans ce dossier : `deploy/robots.txt` et
`deploy/sitemap.xml`.

**Avec Cloudflare** (le plus simple) : Workers & Pages → créer un Worker
rattaché aux routes `caribscope.fwicss.fr/robots.txt` et
`caribscope.fwicss.fr/sitemap.xml`, qui renvoie le contenu de ces fichiers avec
le bon `Content-Type` (`text/plain` et `application/xml`).

**Sans Cloudflare** : ajouter à côté de l'application un petit service nginx
servant ces deux fichiers, et router les deux chemins vers lui dans Traefik. Le
service tient en une image `nginx:alpine` et deux fichiers montés.

Vérification, une fois en place :

```bash
curl -sS https://caribscope.fwicss.fr/robots.txt   | head -3
curl -sSI https://caribscope.fwicss.fr/sitemap.xml | grep -i content-type
```

---

## 6. Redirections et DNS (15 min)

Trois corrections indépendantes :

- **`http://` répond en 302**, une redirection temporaire. Google ne transmet
  pas pleinement l'autorité sur une 302 : la passer en **301**. Cloudflare :
  Rules → Redirect Rules, ou SSL/TLS → Edge Certificates → Always Use HTTPS.
- **`www.caribscope.fwicss.fr` ne résout pas du tout.** Ajouter un CNAME `www`
  vers `caribscope.fwicss.fr` et le rediriger en 301 vers la version sans `www`.
- **`https://fwicss.fr/` renvoie 503.** Le domaine parent est en panne, ce qui
  donne un sous-domaine orphelin sur un domaine mort. Soit y remettre une page,
  soit décider de basculer CaribScope sur un domaine dédié. À arbitrer avant de
  démarcher les journalistes de la roadmap.

---

## 7. Search Console et Bing (20 min)

Sans elle, l'état d'indexation reste une hypothèse.

1. [search.google.com/search-console](https://search.google.com/search-console) →
   ajouter une propriété **Préfixe d'URL** `https://caribscope.fwicss.fr/`.
2. Valider par balise HTML impossible ici (Streamlit ne contrôle pas le `<head>`
   servi) : utiliser la **vérification par enregistrement DNS TXT** sur
   `fwicss.fr`, ou le fichier HTML servi par le même mécanisme qu'au point 5.
3. Soumettre `https://caribscope.fwicss.fr/sitemap.xml`.
4. Répéter sur [Bing Webmaster Tools](https://www.bing.com/webmasters), qui
   alimente aussi les réponses de ChatGPT Search.

Attendre les données : comptez de quelques jours à deux semaines avant que la
couverture d'indexation soit exploitable.

---

## 8. Sauvegarde des leads (30 min)

Une fois le volume monté, les emails deviennent la seule donnée non
reconstructible du projet. Tout le reste se retélécharge depuis la NOAA et
l'USGS.

Coolify → Scheduled Tasks, une fois par jour :

```bash
rclone copy /data/coolify/caribscope/leads remote:caribscope-backups/leads
```

Backblaze B2 et Cloudflare R2 conviennent tous les deux et coûtent quelques
centimes par mois à ce volume.

---

## Vérification finale

Après application des points 1 à 6 :

```bash
# En-têtes de sécurité présents
curl -sSI https://caribscope.fwicss.fr/ | grep -icE "strict-transport|x-content-type|x-frame|referrer|permissions"
# doit renvoyer 5

# robots.txt réellement servi
curl -sS -o /dev/null -w "%{http_code} %{content_type}\n" https://caribscope.fwicss.fr/robots.txt
# doit renvoyer : 200 text/plain

# Redirection permanente
curl -sS -o /dev/null -w "%{http_code}\n" http://caribscope.fwicss.fr/
# doit renvoyer : 301

# Tableau de bord interne fermé
curl -sS https://caribscope.fwicss.fr/KPIs_Internes | grep -c "Streamlit"
# le contenu réel n'est visible qu'après saisie du code, à vérifier dans un navigateur
```

Et dans un navigateur, sur la page d'accueil : le bandeau de consentement doit
apparaître, et aucun cookie `_ga` ne doit exister tant que vous n'avez pas
cliqué « Accepter ».
