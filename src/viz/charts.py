import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

MONTHS_FR = {
    1: "Jan", 2: "Fév", 3: "Mar", 4: "Avr", 5: "Mai", 6: "Juin",
    7: "Juil", 8: "Août", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Déc",
}


def plot_hurricanes_per_year(df_by_year: pd.DataFrame) -> go.Figure:
    """Histogramme du nombre d'ouragans par an + tendance mobile."""
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_by_year["year"],
        y=df_by_year["count"],
        name="Par année",
        marker_color="#DC143C",
        opacity=0.6,
    ))

    rolling = df_by_year.set_index("year")["count"].rolling(10, center=True).mean().reset_index()
    fig.add_trace(go.Scatter(
        x=rolling["year"],
        y=rolling["count"],
        mode="lines",
        name="Moyenne mobile (10 ans)",
        line=dict(color="#FFD700", width=2),
    ))

    fig.update_layout(
        title="Nombre d'ouragans par année (Caraïbes)",
        xaxis_title="Année",
        yaxis_title="Nombre d'ouragans",
        legend=dict(orientation="h", y=1.05),
        template="plotly_dark",
        height=400,
    )
    return fig


def plot_intensity_trend(df_decade: pd.DataFrame) -> go.Figure:
    """Évolution de l'intensité moyenne par décennie."""
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_decade["decade"].astype(str) + "s",
        y=df_decade["mean_max_wind"],
        name="Vitesse max moyenne (kt)",
        marker_color="#FF6347",
    ))

    fig.update_layout(
        title="Intensité maximale moyenne des ouragans par décennie",
        xaxis_title="Décennie",
        yaxis_title="Vitesse max moyenne (kt)",
        template="plotly_dark",
        height=400,
    )
    return fig


def plot_monthly_distribution(df_monthly: pd.DataFrame) -> go.Figure:
    """Distribution mensuelle des ouragans."""
    df_monthly = df_monthly.copy()
    df_monthly["month_name"] = df_monthly["month"].map(MONTHS_FR)

    fig = px.bar(
        df_monthly,
        x="month_name",
        y="count",
        title="Distribution mensuelle des ouragans (Caraïbes)",
        labels={"month_name": "Mois", "count": "Nombre d'ouragans"},
        color="count",
        color_continuous_scale="OrRd",
        template="plotly_dark",
    )
    fig.update_coloraxes(showscale=False)
    fig.update_layout(height=400)
    return fig


def plot_wind_pressure_scatter(df: pd.DataFrame) -> go.Figure:
    """Scatter plot pression vs vitesse du vent."""
    valid = df[(df["USA_WIND"] > 0) & (df["USA_PRES"] > 0)].copy()

    fig = px.scatter(
        valid.sample(min(5000, len(valid))),
        x="USA_WIND",
        y="USA_PRES",
        color="category",
        title="Relation pression / vitesse du vent",
        labels={
            "USA_WIND": "Vitesse du vent (kt)",
            "USA_PRES": "Pression (mb)",
            "category": "Catégorie",
        },
        template="plotly_dark",
        opacity=0.5,
    )
    fig.update_layout(height=400)
    return fig


def plot_hurricane_timeline(df: pd.DataFrame, name: str, year: int) -> go.Figure:
    """Évolution vitesse et pression au fil du temps pour un ouragan."""
    track = df[(df["NAME"] == name) & (df["year"] == year)].copy()
    track = track.sort_values("Hurricane_Date")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=track["Hurricane_Date"],
        y=track["USA_WIND"],
        name="Vitesse (kt)",
        line=dict(color="#FF6347", width=2),
        yaxis="y1",
    ))

    fig.add_trace(go.Scatter(
        x=track["Hurricane_Date"],
        y=track["USA_PRES"],
        name="Pression (mb)",
        line=dict(color="#00BFFF", width=2),
        yaxis="y2",
    ))

    fig.update_layout(
        title=f"Évolution de {name} ({year})",
        xaxis_title="Date",
        yaxis=dict(title="Vitesse (kt)", side="left"),
        yaxis2=dict(title="Pression (mb)", side="right", overlaying="y"),
        legend=dict(orientation="h"),
        template="plotly_dark",
        height=350,
    )
    return fig


def plot_basin_distribution(df: pd.DataFrame) -> go.Figure:
    """Camembert de la répartition par bassin."""
    basin_counts = df.groupby("BASIN")["SID"].nunique().reset_index()
    basin_counts.columns = ["basin", "count"]

    fig = px.pie(
        basin_counts,
        names="basin",
        values="count",
        title="Répartition des ouragans par bassin",
        template="plotly_dark",
    )
    fig.update_layout(height=400)
    return fig
