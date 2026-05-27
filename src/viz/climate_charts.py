import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

MONTHS_FR = {
    1: "Jan", 2: "Fév", 3: "Mar", 4: "Avr", 5: "Mai", 6: "Juin",
    7: "Juil", 8: "Août", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Déc",
}


def plot_major_hurricane_pct(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["decade"].astype(str) + "s",
        y=df["major_pct"],
        name="% Cat 4-5",
        marker_color="#DC143C",
        opacity=0.85,
    ))
    rolling = df.set_index("decade")["major_pct"].rolling(2, center=True).mean().reset_index()
    fig.add_trace(go.Scatter(
        x=rolling["decade"].astype(str) + "s",
        y=rolling["major_pct"],
        mode="lines+markers",
        name="Tendance",
        line=dict(color="#FFD700", width=2),
    ))
    fig.update_layout(
        title="% d'ouragans majeurs (Cat 4-5) par décennie",
        xaxis_title="Décennie",
        yaxis_title="% des ouragans",
        template="plotly_dark",
        height=400,
        legend=dict(orientation="h", y=1.05),
    )
    return fig


def plot_season_length(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["year"],
        y=df["first_month"].map(MONTHS_FR),
        mode="lines",
        name="Début de saison",
        line=dict(color="#4FC3F7", width=1.5),
    ))
    fig.add_trace(go.Scatter(
        x=df["year"],
        y=df["last_month"].map(MONTHS_FR),
        mode="lines",
        name="Fin de saison",
        line=dict(color="#FF6347", width=1.5),
    ))
    fig.update_layout(
        title="Durée de la saison des ouragans par année",
        xaxis_title="Année",
        yaxis_title="Mois",
        template="plotly_dark",
        height=400,
        legend=dict(orientation="h", y=1.05),
    )
    return fig


def plot_sst_trend(df_sst: pd.DataFrame) -> go.Figure:
    yearly = df_sst.groupby("year")["sst_c"].mean().reset_index()
    rolling = yearly.set_index("year")["sst_c"].rolling(5, center=True).mean().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=yearly["year"],
        y=yearly["sst_c"],
        mode="lines",
        name="SST annuelle",
        line=dict(color="#4FC3F7", width=1),
        opacity=0.5,
    ))
    fig.add_trace(go.Scatter(
        x=rolling["year"],
        y=rolling["sst_c"],
        mode="lines",
        name="Moyenne mobile (5 ans)",
        line=dict(color="#FFD700", width=2.5),
    ))
    fig.update_layout(
        title="Température de surface (SST) — Caraïbes 1980–2025",
        xaxis_title="Année",
        yaxis_title="SST (°C)",
        template="plotly_dark",
        height=400,
        legend=dict(orientation="h", y=1.05),
    )
    return fig


def plot_sst_correlation(df_corr: pd.DataFrame) -> go.Figure:
    import numpy as np
    if df_corr.empty:
        return go.Figure()
    corr = df_corr[["sst_peak", "max_wind"]].corr().iloc[0, 1]
    m, b = np.polyfit(df_corr["sst_peak"], df_corr["max_wind"], 1)
    x_line = [df_corr["sst_peak"].min(), df_corr["sst_peak"].max()]
    y_line = [m * x + b for x in x_line]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_corr["sst_peak"],
        y=df_corr["max_wind"],
        mode="markers+text",
        text=df_corr["year"].astype(str),
        textposition="top center",
        marker=dict(color="#FF6347", size=8),
        name="Données annuelles",
    ))
    fig.add_trace(go.Scatter(
        x=x_line,
        y=y_line,
        mode="lines",
        line=dict(color="#FFD700", dash="dash", width=2),
        name=f"Tendance (r={corr:.2f})",
    ))
    fig.update_layout(
        title="Corrélation SST pic-saison ↔ vitesse max ouragan",
        xaxis_title="SST juillet–octobre (°C)",
        yaxis_title="Vent max ouragan (kt)",
        template="plotly_dark",
        height=400,
        legend=dict(orientation="h", y=1.05),
    )
    return fig
