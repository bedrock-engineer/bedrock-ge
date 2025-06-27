# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "geopandas==1.1.0",
#     "mapclassify==2.9.0",
#     "marimo",
#     "matplotlib==3.10.3",
#     "pyarrow==20.0.0",
#     "python-ags4==1.1.0",
#     "requests==2.32.4",
# ]
# ///

import marimo

__generated_with = "0.14.7"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import io
    import platform
    import sys

    import geopandas as gpd
    import marimo as mo
    from python_ags4 import AGS4

    platform_system = platform.system()
    print(platform_system)
    print(sys.version)
    # print(sys.executable)
    return AGS4, gpd, io, mo, platform_system


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # AGS 4 data for the Silvertown Tunnel, London, UK

    The Silvertown Tunnel is a road tunnel, opened on 7 April 2025, beneath the River Thames in east London, England. The 1.4 km (0.87-mile) twin-bore tunnel runs between west Silvertown, east of the River Lea estuary, on the north side of the Thames and a portal adjacent to the existing Blackwall Tunnel on the Greenwich Peninsula south of the river. ([Source](https://en.wikipedia.org/wiki/Silvertown_Tunnel))

    The Ground Investigation (GI) data and derived ground model that were used for the design of the Siltertown bored tunnels have been published online.

    The GI data for the Silvertown tunnel can be found on the British Geological Survey's ([BGS](https://www.bgs.ac.uk/)) [Deposited data search page](https://webapps.bgs.ac.uk/services/ngdc/accessions/index.html):  
    [**Title**: Preliminary GI for Silvertown Tunnel  
    **Description**: 	77 exploratory holes carried out for the design of the Silvertown Tunnel, London](https://webapps.bgs.ac.uk/services/ngdc/accessions/index.html?simpleText=silvertown#item162465)  
    For convenience, the AGS 4 file has also been uploaded to GitHub such that you can have a quick look what this AGS 4 data [looks like 🔎](https://raw.githubusercontent.com/bedrock-engineer/bedrock-ge/refs/heads/main/examples/uk_silvertown_tunnel_ags4/20110770-2021-02-16_1308-Final-6.ags). 

    The ground model has been published as an [AGSi Ground Model](https://www.ags.org.uk/data-format/agsi-ground-model/) by the Association of Geotechnical & Geoenvironmental Specialists ([AGS](https://www.ags.org.uk/)):  
    [AGSi Guidance / Example files](https://ags-data-format-wg.gitlab.io/agsi/AGSi_Documentation/Example_Silvertown)
    """
    )
    return


@app.cell
async def _(io, platform_system):
    bgs_url = "https://webservices.bgs.ac.uk/accessions/download/162465?fileName=20110770%20-%202021-02-16%201308%20-%20Final%20-%206.ags"
    # When running this marimo notebook in WebAssembly (WASM, a.k.a. Emscripten), use pyodide to request the data
    if platform_system == "Emscripten":
        from pyodide.http import pyfetch
        response = await pyfetch(bgs_url)
        ags = io.BytesIO(await response.bytes())
    else:
        import requests
        ags = io.BytesIO(requests.get(bgs_url).content)
    return (ags,)


@app.cell
def _(AGS4, ags):
    ags_tables, headings = AGS4.AGS4_to_dataframe(ags)
    for group, data in ags_tables.items():
        ags_tables[group] = (
            AGS4.convert_to_numeric(data).drop(columns=["HEADING"])
            # .convert_to_numeric already removes the UNIT and TYPE rows.
            # .loc[2:]
            # .reset_index(drop=True)
        )

    ags_tables
    return (ags_tables,)


@app.cell
def _(ags_tables, gpd):
    ags_tables["LOCA"] = gpd.GeoDataFrame(
        ags_tables["LOCA"],
        geometry=gpd.points_from_xy(
            ags_tables["LOCA"]["LOCA_NATE"], ags_tables["LOCA"]["LOCA_NATN"]
        ),
        crs="EPSG:27700",
    )
    return


@app.cell
def _(ags_tables):
    ags_tables["LOCA"].explore()
    return


if __name__ == "__main__":
    app.run()
