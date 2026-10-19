"""Mentions légales, politique de confidentialité et gestion du consentement.

Fichier volontairement nommé sans accent : Streamlit dérive l'URL du nom de
fichier, et /Mentions_Legales évite un chemin percent-encodé dans les liens du
bandeau de consentement et du formulaire de capture email.

⚠️ HEBERGEUR : à compléter avec le fournisseur réel du VPS qui exécute Coolify
(dénomination, adresse, téléphone). C'est une mention obligatoire au titre de
l'article 6 III de la LCEN.
"""
import streamlit as st

from src.components.analytics import consent_reset_button, inject_analytics, measurement_id

st.set_page_config(
    page_title="Mentions légales — CaribScope",
    page_icon="⚖️",
    layout="centered",
)

inject_analytics("Mentions Legales")
inject_head(
    title="Mentions légales et confidentialité — CaribScope",
    description=(
        "Mentions légales, politique de confidentialité et gestion du consentement aux cookies de CaribScope."
    ),
    path="Mentions_Legales",
)

EDITEUR = {
    "denomination": "Dim's Info Services",
    "statut": "Micro-entreprise (entrepreneur individuel)",
    "siret": "92070724700010",
    "adresse": "Sainte-Rose, 97115 Guadeloupe",
    "responsable": "Dimitri Aigle",
    "email": "contact@dimsinfoservices.dev",
    "tva": "TVA non applicable, article 293 B du CGI",
}

# À compléter : nom, raison sociale, adresse et téléphone du fournisseur du VPS.
HEBERGEUR = {
    "denomination": "À compléter",
    "adresse": "À compléter",
    "telephone": "À compléter",
}

st.title("⚖️ Mentions légales et politique de confidentialité")
st.caption("Dernière mise à jour : 2 septembre 2026")

st.divider()

# ── Mentions légales ─────────────────────────────────────────────────────────
st.header("1. Mentions légales")

st.subheader("Éditeur du site")
st.markdown(
    f"""
- **Dénomination** : {EDITEUR['denomination']}
- **Statut** : {EDITEUR['statut']}
- **SIRET** : {EDITEUR['siret']}
- **Siège** : {EDITEUR['adresse']}
- **Directeur de la publication** : {EDITEUR['responsable']}
- **Contact** : [{EDITEUR['email']}](mailto:{EDITEUR['email']})
- **TVA** : {EDITEUR['tva']}
"""
)

st.subheader("Hébergement")
if HEBERGEUR["denomination"] == "À compléter":
    st.warning(
        "Mention d'hébergeur non renseignée. Elle est obligatoire (LCEN, art. 6 III) : "
        "compléter le dictionnaire HEBERGEUR dans ce fichier avec le fournisseur du "
        "serveur qui exécute Coolify."
    )
else:
    st.markdown(
        f"""
- **Hébergeur** : {HEBERGEUR['denomination']}
- **Adresse** : {HEBERGEUR['adresse']}
- **Téléphone** : {HEBERGEUR['telephone']}
"""
    )

st.subheader("Propriété intellectuelle et données sources")
st.markdown(
    """
Le code de CaribScope est publié sous licence MIT sur
[github.com/FWICSS/caribscope](https://github.com/FWICSS/caribscope).

Les données affichées proviennent de sources publiques et restent la propriété
de leurs producteurs :

- **NOAA HURDAT2** (National Hurricane Center) pour les trajectoires cycloniques ;
- **USGS Earthquake Catalog** pour le catalogue sismique ;
- données de température de surface océanique pour la zone caribéenne.

CaribScope est un projet indépendant, sans lien officiel avec la NOAA, l'USGS,
Météo-France ou toute autorité de sécurité civile. **Les informations diffusées
sont fournies à titre informatif et documentaire. Elles ne constituent en aucun
cas une alerte officielle et ne doivent pas servir de fondement à une décision
de mise en sécurité.** En cas d'événement, se référer exclusivement aux
consignes de la préfecture et de Météo-France.
"""
)

st.divider()

# ── Politique de confidentialité ──────────────────────────────────────────────
st.header("2. Politique de confidentialité")

st.markdown(
    f"""
Le responsable de traitement est **{EDITEUR['denomination']}**, joignable à
l'adresse [{EDITEUR['email']}](mailto:{EDITEUR['email']}).

CaribScope met en œuvre deux traitements de données à caractère personnel.
"""
)

st.subheader("2.1 Newsletter « Ouragan du jour »")
st.markdown(
    """
| | |
|---|---|
| **Données collectées** | Adresse email, date d'inscription, page d'origine, navigateur utilisé |
| **Finalité** | Envoi de la newsletter et des alertes de saison cyclonique |
| **Base légale** | Consentement (RGPD, art. 6.1.a), donné par la soumission volontaire du formulaire |
| **Durée de conservation** | 3 ans à compter du dernier contact, ou jusqu'à demande de suppression |
| **Destinataires** | L'éditeur seul. Aucune cession, aucune revente, aucun partage commercial |
| **Transfert hors UE** | Aucun |
"""
)

st.subheader("2.2 Mesure d'audience (Google Analytics 4)")
if measurement_id():
    st.markdown(
        """
| | |
|---|---|
| **Données collectées** | Pages consultées, durée de visite, type d'appareil, pays, source d'arrivée, identifiant de mesure déposé par cookie |
| **Finalité** | Comprendre l'usage du site et orienter son développement |
| **Base légale** | Consentement (RGPD, art. 6.1.a) |
| **Sous-traitant** | Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irlande |
| **Transfert hors UE** | Oui, vers les États-Unis, encadré par le Data Privacy Framework et les clauses contractuelles types |
| **Durée de conservation** | 14 mois maximum |

**Aucun cookie de mesure n'est déposé avant votre accord.** Le refus est sans
conséquence : toutes les fonctionnalités du site restent accessibles. Le
consentement est recueilli via le bandeau affiché à la première visite, et vous
pouvez revenir sur votre choix à tout moment ci-dessous.
"""
    )
    st.markdown("**Modifier mon consentement**")
    consent_reset_button()
else:
    st.info(
        "La mesure d'audience est actuellement désactivée sur cette instance : "
        "aucun cookie analytique n'est déposé."
    )

st.subheader("2.3 Vos droits")
st.markdown(
    f"""
Vous disposez d'un droit d'accès, de rectification, d'effacement, de limitation,
d'opposition et de portabilité sur vos données, ainsi que du droit de retirer
votre consentement à tout moment.

Pour l'exercer, écrivez à [{EDITEUR['email']}](mailto:{EDITEUR['email']}).
Une réponse vous sera apportée sous un mois.

Si vous estimez que vos droits ne sont pas respectés, vous pouvez introduire une
réclamation auprès de la **CNIL** : [www.cnil.fr/fr/plaintes](https://www.cnil.fr/fr/plaintes),
3 place de Fontenoy, TSA 80715, 75334 Paris Cedex 07.
"""
)

st.subheader("2.4 Sécurité et sous-traitance")
st.markdown(
    """
Les adresses collectées sont stockées sur le serveur qui héberge l'application,
dans un fichier accessible au seul éditeur. Les échanges avec le site sont
chiffrés en HTTPS. Aucun prestataire d'emailing n'est utilisé à ce jour ; si un
tel prestataire est introduit, cette page sera mise à jour avant tout transfert.
"""
)

st.divider()
st.caption(
    "CaribScope — Observatoire open source des risques naturels caribéens · "
    "Données NOAA & USGS · Code sous licence MIT"
)
