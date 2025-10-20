# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "folium==0.20.0",
#     "geopandas==1.1.1",
#     "mapclassify==2.8.1",
#     "marimo",
#     "matplotlib==3.10.7",
#     "pygef==0.13.0",
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
def _(cpt_data, plot_cpt):
    plot_cpt(cpt_data)
    return


@app.cell
def _():
    import geopandas as gpd
    import marimo as mo
    from pygef import read_cpt
    from pygef.plotting import plot_cpt

    return gpd, mo, plot_cpt, read_cpt


if __name__ == "__main__":
    app.run()
