import streamlit as st
import plotly.express as px
import pandas as pd
from src.data.loader import load_caribbean_tracks, CATEGORY_COLORS
from src.ml.predict import load_model, predict_category, get_feature_importance, CATEGORY_LABELS

st.set_page_config(page_title="Prédiction ML", page_icon="🤖", layout="wide")
st.title("🤖 Prédiction d'Intensité — Machine Learning")
st.caption("Modèle Random Forest entraîné sur 170 ans de données HURDAT2 · Prédit la catégorie Saffir-Simpson.")

try:
    model = load_model()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

tab1, tab2 = st.tabs(["🔮 Prédire", "📊 Comprendre le modèle"])

# ── Tab 1: Prédire ────────────────────────────────────────────────────────────
with tab1:
    st.subheader("Entrez les conditions météo actuelles")
    col_in1, col_in2 = st.columns(2)

    with col_in1:
        pressure = st.slider("Pression atmosphérique (mb)", 870, 1020, 980)
        lat = st.slider("Latitude (°N)", 8.0, 28.0, 18.0, 0.5)

    with col_in2:
        lon = st.slider("Longitude (°E)", -90.0, -55.0, -65.0, 0.5)
        month = st.selectbox(
            "Mois",
            options=list(range(1, 13)),
            index=8,
            format_func=lambda m: {
                1:"Janvier",2:"Février",3:"Mars",4:"Avril",5:"Mai",6:"Juin",
                7:"Juillet",8:"Août",9:"Septembre",10:"Octobre",11:"Novembre",12:"Décembre"
            }[m],
        )

    result = predict_category(model, pressure=pressure, lat=lat, lon=lon, month=month)

    st.divider()
    cat_num = result["category_num"]
    cat_label = result["category_label"]
    cat_color = list(CATEGORY_COLORS.values())[min(cat_num + 1, len(CATEGORY_COLORS) - 1)]

    st.markdown(f"""
    <div style="background:{cat_color}22;border:2px solid {cat_color};border-radius:12px;padding:20px;text-align:center;">
        <h2 style="color:{cat_color};margin:0;">🌀 {cat_label}</h2>
        <p style="color:#ccc;margin:4px 0 0 0;">Catégorie prédite</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Probabilités par catégorie")
    proba_df = pd.DataFrame([
        {"Catégorie": CATEGORY_LABELS.get(k, str(k)), "Probabilité": round(v * 100, 1)}
        for k, v in sorted(result["probabilities"].items())
    ])
    fig_proba = px.bar(
        proba_df, x="Probabilité", y="Catégorie", orientation="h",
        color="Probabilité", color_continuous_scale="Reds",
        template="plotly_dark", height=320,
    )
    fig_proba.update_coloraxes(showscale=False)
    st.plotly_chart(fig_proba, width="stretch")

# ── Tab 2: Comprendre ─────────────────────────────────────────────────────────
with tab2:
    st.subheader("Importance des variables")
    imp_df = get_feature_importance(model)
    imp_df["feature_fr"] = imp_df["feature"].map({
        "USA_PRES": "Pression (mb)",
        "LAT": "Latitude",
        "LON": "Longitude",
        "month": "Mois",
        "decade": "Décennie",
    })
    fig_imp = px.bar(
        imp_df, x="importance", y="feature_fr", orientation="h",
        title="Importance des features dans le modèle",
        labels={"importance": "Importance relative", "feature_fr": "Variable"},
        color="importance", color_continuous_scale="Oranges",
        template="plotly_dark", height=350,
    )
    fig_imp.update_coloraxes(showscale=False)
    st.plotly_chart(fig_imp, width="stretch")

    top_feature = imp_df["feature_fr"].iloc[0]
    top_pct = round(imp_df["importance"].iloc[0] * 100, 1)
    st.info(
        f"💡 **{top_feature}** est la variable la plus prédictive du modèle ({top_pct}% d'importance)."
    )

    st.subheader("Test sur un ouragan historique")
    with st.spinner("Chargement des ouragans…"):
        df_hurr = load_caribbean_tracks()

    storm_options = (
        df_hurr.groupby(["NAME", "year"])["SID"]
        .first().reset_index()
        .assign(label=lambda d: d["NAME"] + " (" + d["year"].astype(str) + ")")
        .sort_values(["year", "NAME"], ascending=False)
    )
    selected = st.selectbox("Sélectionner un ouragan", storm_options["label"].tolist())
    row = storm_options[storm_options["label"] == selected].iloc[0]
    track = df_hurr[(df_hurr["NAME"] == row["NAME"]) & (df_hurr["year"] == row["year"])]
    track = track[track["USA_PRES"] > 0].copy()

    if not track.empty:
        preds = [
            predict_category(model, r["USA_PRES"], r["LAT"], r["LON"], r["month"])["category_num"]
            for _, r in track.iterrows()
        ]
        track["predicted_cat"] = preds
        correct = (track["predicted_cat"] == track["category_num"]).mean()
        st.metric("Précision sur cet ouragan", f"{correct * 100:.1f}%")
        st.dataframe(
            track[["Hurricane_Date", "USA_WIND", "USA_PRES", "category_num", "predicted_cat"]]
            .rename(columns={
                "Hurricane_Date": "Date",
                "USA_WIND": "Vent (kt)",
                "USA_PRES": "Pression (mb)",
                "category_num": "Cat réelle",
                "predicted_cat": "Cat prédite",
            }),
            width="stretch",
            hide_index=True,
        )
