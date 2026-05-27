import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


_MAG_COLOR_SCALE = [
    [0.0, "#FFD700"],
    [0.3, "#FFA500"],
    [0.6, "#FF4500"],
    [1.0, "#8B0000"],
]


def plot_earthquake_map(df: pd.DataFrame, mode: str = "points") -> go.Figure:
    """mode: 'points' or 'heatmap'"""
    if mode == "heatmap":
        fig = go.Figure(go.Densitymapbox(
            lat=df["latitude"],
            lon=df["longitude"],
            z=df["magnitude"],
            radius=20,
            colorscale="YlOrRd",
            showscale=True,
            colorbar=dict(title="Magnitude"),
            hoverinfo="skip",
        ))
    else:
        fig = go.Figure(go.Scattermapbox(
            lat=df["latitude"],
            lon=df["longitude"],
            mode="markers",
            marker=dict(
                size=df["magnitude"] * 2,
                color=df["magnitude"],
                colorscale=_MAG_COLOR_SCALE,
                showscale=True,
                colorbar=dict(title="Magnitude"),
                sizemin=4,
            ),
            text=df["place"],
            customdata=df[["magnitude", "depth_km", "year"]].values,
            hovertemplate=(
                "<b>%{text}</b><br>"
                "Magnitude: %{customdata[0]}<br>"
                "Profondeur: %{customdata[1]:.1f} km<br>"
                "Année: %{customdata[2]}<br>"
                "<extra></extra>"
            ),
        ))

    fig.update_layout(
        mapbox=dict(
            style="carto-darkmatter",
            center=dict(lat=18, lon=-65),
            zoom=3.5,
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        height=550,
        title="Séismes Caraïbes (M ≥ 4.0)",
        template="plotly_dark",
    )
    return fig


def plot_earthquakes_by_decade(df_decade: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df_decade,
        x=df_decade["decade"].astype(str) + "s",
        y="count",
        title="Nombre de séismes (M ≥ 4.0) par décennie",
        labels={"x": "Décennie", "count": "Nombre de séismes"},
        color="count",
        color_continuous_scale="OrRd",
        template="plotly_dark",
    )
    fig.update_coloraxes(showscale=False)
    fig.update_layout(height=400)
    return fig


def plot_magnitude_histogram(df_dist: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df_dist,
        x="range",
        y="count",
        title="Distribution par magnitude",
        labels={"range": "Magnitude", "count": "Nombre"},
        color="count",
        color_continuous_scale="Reds",
        template="plotly_dark",
    )
    fig.update_coloraxes(showscale=False)
    fig.update_layout(height=380)
    return fig
