import pandas as pd
import plotly.graph_objects as go
from src.data.loader import CATEGORY_COLORS


def plot_track_map(df: pd.DataFrame, title: str = "Trajectoires des ouragans — Caraïbes") -> go.Figure:
    """
    Carte Plotly des trajectoires. Chaque ouragan (SID) est une trace.
    La couleur représente la catégorie Saffir-Simpson.
    """
    fig = go.Figure()

    for sid, group in df.groupby("SID"):
        name = group["NAME"].iloc[0]
        year = int(group["year"].iloc[0])

        if group["USA_WIND"].notna().any():
            max_wind_idx = group["USA_WIND"].idxmax()
            dominant_cat = group.loc[max_wind_idx, "category"]
        else:
            dominant_cat = "Inconnu"

        color = CATEGORY_COLORS.get(dominant_cat, "#808080")

        fig.add_trace(go.Scattermapbox(
            lat=group["LAT"].tolist(),
            lon=group["LON"].tolist(),
            mode="lines+markers",
            line=dict(width=1.5, color=color),
            marker=dict(
                size=5,
                color=[CATEGORY_COLORS.get(c, "#808080") for c in group["category"].tolist()],
            ),
            name=f"{name} ({year})",
            hovertemplate=(
                f"<b>{name} {year}</b><br>"
                "Lat: %{lat:.1f}°<br>"
                "Lon: %{lon:.1f}°<br>"
                "<extra></extra>"
            ),
            showlegend=False,
        ))

    _add_legend_traces(fig)

    fig.update_layout(
        title=title,
        mapbox=dict(
            style="carto-darkmatter",
            center=dict(lat=18, lon=-65),
            zoom=3.5,
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        height=550,
    )
    return fig


def plot_heatmap(df: pd.DataFrame) -> go.Figure:
    """Heatmap de densité des passages d'ouragans."""
    fig = go.Figure(go.Densitymapbox(
        lat=df["LAT"],
        lon=df["LON"],
        z=[1] * len(df),
        radius=12,
        colorscale="YlOrRd",
        showscale=True,
        colorbar=dict(title="Densité"),
        hoverinfo="skip",
    ))

    fig.update_layout(
        mapbox=dict(
            style="carto-darkmatter",
            center=dict(lat=18, lon=-65),
            zoom=3.5,
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        height=550,
        title="Zones de passage les plus fréquentes",
    )
    return fig


def plot_single_track(df: pd.DataFrame, name: str, year: int) -> go.Figure:
    """Trajectoire détaillée d'un ouragan avec évolution de la catégorie."""
    track = df[(df["NAME"] == name) & (df["year"] == year)]

    fig = go.Figure()

    for _, row in track.iterrows():
        cat = row["category"]
        color = CATEGORY_COLORS.get(cat, "#808080")
        fig.add_trace(go.Scattermapbox(
            lat=[row["LAT"]],
            lon=[row["LON"]],
            mode="markers",
            marker=dict(size=10, color=color),
            hovertemplate=(
                f"<b>{name} {year}</b><br>"
                f"Catégorie: {cat}<br>"
                f"Vent: {row.get('USA_WIND', 'N/A')} kt<br>"
                f"Pression: {row.get('USA_PRES', 'N/A')} mb<br>"
                "<extra></extra>"
            ),
            showlegend=False,
        ))

    if len(track) > 1:
        fig.add_trace(go.Scattermapbox(
            lat=track["LAT"].tolist(),
            lon=track["LON"].tolist(),
            mode="lines",
            line=dict(width=2, color="white"),
            showlegend=False,
            hoverinfo="skip",
        ))

    _add_legend_traces(fig)

    min_lat, max_lat = track["LAT"].min(), track["LAT"].max()
    min_lon, max_lon = track["LON"].min(), track["LON"].max()
    center_lat = (min_lat + max_lat) / 2
    center_lon = (min_lon + max_lon) / 2

    fig.update_layout(
        mapbox=dict(
            style="carto-darkmatter",
            center=dict(lat=center_lat, lon=center_lon),
            zoom=4,
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        height=500,
        title=f"Trajectoire de {name} ({year})",
    )
    return fig


def _add_legend_traces(fig: go.Figure) -> None:
    for cat, color in CATEGORY_COLORS.items():
        fig.add_trace(go.Scattermapbox(
            lat=[None], lon=[None],
            mode="markers",
            marker=dict(size=10, color=color),
            name=cat,
            showlegend=True,
        ))
