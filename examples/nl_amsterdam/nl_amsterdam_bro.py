# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "bromodels",
#     "folium==0.20.0",
#     "geopandas==1.1.1",
#     "mapclassify==2.8.1",
#     "marimo",
#     "matplotlib==3.10.7",
#     "pyarrow==21.0.0",
#     "pygef==0.13.0",
#     "pyobsplot",
#     "xarray",
# ]
# ///

import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(
        r"""
    How to access BRO data: [Handreiking Afname BRO Gegevens](https://www.bro-productomgeving.nl/bpo/latest/handreiking-afname-bro-gegevens)

    1. [BROloket](https://www.broloket.nl/ondergrondgegevens)
    2. BRO APIs
      1. SOAP - impractical, because requires a digital "PKI" certificate.
      2. [REST](https://www.bro-productomgeving.nl/bpo/latest/url-s-publieke-rest-services)
        1. CPT: <https://publiek.broservices.nl/sr/cpt/v1>
        2. Goetechnical boreholes: <https://publiek.broservices.nl/sr/bhrgt/v2>
    3. [PDOK](https://app.pdok.nl/viewer) - WMS
    """
    )
    return


@app.cell
def _(mo):
    cwd = mo.notebook_location()
    return (cwd,)


@app.cell
def _(cwd, gpd):
    site_plot = gpd.read_file(cwd / "context.gpkg")
    site_plot.explore()
    return


@app.cell
def _(cwd, read_cpt):
    cpt_data = read_cpt(cwd / "data" / "CPT000000061548.xml")
    cpt_data.data
    return (cpt_data,)


@app.cell
def _(cpt_data):
    cpt_data.data
    return


@app.cell
def _(cpt_data):
    type(cpt_data.data)
    return


@app.cell
def _(pl):
    data = pl.DataFrame(
        {
            "x": [1, 5, 2, 4, 6, 2, 4],
            "y": [2, 1, 3, 4, 5, 1, 2],
            "type": ["T1", "T2", "T1", "T2", "T1", "T1", "T2"],
        }
    )
    return (data,)


@app.cell
def _(data):
    type(data)
    return


@app.cell
def _(Plot, data):
    Plot.plot(
        {
            "grid": True,
            "marks": [Plot.dot(data, {"x": "x", "y": "y", "fill": "type", "r": 5})],
        }
    )
    return


@app.cell
def _(cpt_data):
    cpt_data.data
    return


@app.cell
def _(Plot, cpt_data):
    Plot.plot({
        "height": 580, "width": 300, 
        "x": {
          "label": "Conus [MPa]",
          "grid": True
        },
        "y":{
          "grid": True,
          "reverse": True,
          "label": "Depth [m]"
        },
        "marks": [
          Plot.frame(),
          Plot.lineX(cpt_data.data, {
            "x": "coneResistance",
            "y": "depth"
          }),
          Plot.crosshair(cpt_data.data, {
            "x": "coneResistance",
            "y": "depth"
          })
        ]
    })
    return


@app.cell
def _(cpt_data, plot_cpt):
    plot_cpt(cpt_data)
    return


@app.cell
def _():
    import geopandas as gpd
    import marimo as mo
    from pygef import read_cpt
    from pygef.plotting import plot_cpt
    from pyobsplot import Plot
    import matplotlib.pyplot as plt
    import numpy as np
    import xarray
    from matplotlib.colors import ListedColormap
    import bromodels
    import polars as pl
    return Plot, gpd, mo, pl, plot_cpt, read_cpt


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
