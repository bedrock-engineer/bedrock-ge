# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "folium==0.19.5",
#     "mapclassify==2.8.1",
#     "matplotlib==3.9.4",
#     "pandas==2.2.3",
#     "shapely==2.0.7",
# ]
# ///

import marimo

__generated_with = "0.13.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    from pathlib import Path

    import geopandas as gpd
    import marimo as mo
    import pandas as pd
    import pyogrio
    from shapely import Point

    return Path, Point, gpd, mo, pd, pyogrio


@app.cell
def _(Path):
    gpkg_path = Path(
        r"S:\Shared drives\Bedrock\Case Studies\A2TunnelMaastricht\data\A2_Maastricht.gpkg"
    )
    return (gpkg_path,)


@app.cell(hide_code=True)
def _(gpd, gpkg_path, pyogrio):
    gpkg_layers = gpd.list_layers(gpkg_path)

    brgi_geodb = {}
    for layer in gpkg_layers["name"]:
        brgi_geodb[layer] = pyogrio.read_dataframe(gpkg_path, layer=layer)

    gpkg_layers
    return (brgi_geodb,)


@app.cell(hide_code=True)
def _(brgi_geodb, mo):
    sel_brgi_table = mo.ui.dropdown(brgi_geodb, value="Project")
    mo.md(f"Select the Bedrock GI table you want to explore: {sel_brgi_table}")
    return (sel_brgi_table,)


@app.cell(hide_code=True)
def _(pd, sel_brgi_table):
    df = pd.DataFrame(sel_brgi_table.value.copy())
    if "geometry" in df.columns:
        df = df.assign(geometry=df.geometry.astype(str))

    df
    return


@app.cell(hide_code=True)
def _(Point, sel_brgi_table):
    if "geometry" in sel_brgi_table.value.columns:
        gdf = sel_brgi_table.value.copy()
        gdf = gdf["geometry"].apply(lambda geom: Point(geom.coords[0]))
        map = gdf.explore()
    else:
        map = f"The {sel_brgi_table.selected_key} table doesn't contain GIS geometry."

    map
    return


if __name__ == "__main__":
    app.run()
