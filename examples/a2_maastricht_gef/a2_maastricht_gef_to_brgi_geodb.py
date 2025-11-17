# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "bedrock-ge==0.3.2",
#     "folium==0.20.0",
#     "geopandas==1.1.1",
#     "mapclassify==2.8.1",
#     "marimo[mcp]",
#     "matplotlib==3.10.7",
#     "pyproj==3.7.1",
#     "requests==2.32.3",
#     "shapely==2.1.2",
#     "pygef==0.13.0",
#     "pandas==2.3.3",
#     "pyarrow==21.0.0",
#     "anthropic==0.73.0",
#     "numpy==2.3.5",
# ]
# ///

import marimo

__generated_with = "0.17.8"
app = marimo.App(
    width="medium",
    app_title="Maastricht A2 Tunnel GEF-BORE data to a Bedrock GI Geospatial Database",
)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # GEF Data for A2 Tunnel Maastricht

    <a href="https://bedrock.engineer"><img src="https://bedrock.engineer/Bedrock_TextRight.png" alt="Bedrock logo" width="180" /></a>

    This notebook demonstrates how to

    1. Read in Ground Investigation (GI) data from [GEF files](https://bedrock.engineer/reference/formats/gef/gef/) using the [pygef](https://cemsbv.github.io/pygef/) library.
    1. Use [`bedrock-ge`](https://github.com/bedrock-engineer/bedrock-ge) to convert that data into a standardized GI database.
    1. Transform the GI data into 3D spatial features with proper coordinates and geometry ([OGC Simple Feature](https://en.wikipedia.org/wiki/Simple_Features))
    1. Explore and analyze the GI data using interactive filtering with Pandas DataFrames and interactive visualization on a map using GeoPandas.
    1. Export the processed GI database to a GeoPackage file for use in GIS software, like QGIS or ArcGIS.

    <details>
        <summary>What are GEF files?</summary>
        <p>
            <abbr>[Geotechnical Exchange Format](http://localhost:4321/reference/formats/gef/gef/) (GEF)</abbr> is a standardized,
            text-based format designed to facilitate the reliable exchange and archiving
            of geotechnical investigation data, particularly CPT results, across
            different organizations and software platforms. GEF can also be used for
            other types of soil tests, like <a href="https://bedrock.engineer/reference/formats/gef/gef-cpt/">CPTs</a>. It is widely used in the
            Netherlands and Belgium in ground investigation.
        </p>
    </details>

    <details>
        <summary>What is a DataFrame?</summary>
        <p>
          A DataFrame is like a spreadsheet, it is a two-dimensional data structure that holds data like a table with rows and columns.
        </p>
    </details>

    ## Ground Investigation Data

    The GI data was downloaded from [Dinoloket](https://www.dinoloket.nl/ondergrondgegevens), a platform for viewing and request data from the Dutch Geological Survey and Basisregistratie Ondergrond about the subsurface of the Netherlands.
    We are using [GEF files](https://bedrock.engineer/reference/formats/gef/gef/) that contain borehole data, [GEF-BORE](https://bedrock.engineer/reference/formats/gef/gef-bore/).

    ## Context

    The [Koning Willem-Alexander Tunnel](https://www.rijkswaterstaat.nl/wegen/wegenoverzicht/a2/koning-willem-alexandertunnel-a2-n2) is a double-deck tunnel for motorized traffic in the city Maastricht, the Netherlands. The tunnel has a length of 2.5 kilometers (lower tunnel tubes) and 2.3 kilometers (upper tunnel tubes).

    The tunnel has moved the old A2 highway underground. This highway previously formed a barrier for the city and slowed traffic.

    ### Geology

    The uppermost layer consists of topsoil, clay, and loam, with a thickness of about 2 to 4 meters. These soft Holocene deposits are attributed to the Boxtel Formation, laid down by the Meuse River. The tunnel is situated in a former river arm.

    Beneath the surface layer lies an approximately 8-m thick gravel deposit. This gravel acts as a significant aquifer and was a key factor in the groundwater management strategies required for the tunnel construction.

    Below the gravel lies a fissured limestone layer belonging to the Maastricht Formation (mergel). This layer is a very weak, porous, sandy, shallow marine limestone, often weathered, and includes chalk and calcarenite components.

    The limestone is relatively young and shallow, resulting in low compaction and cementation. Its mechanical strength is highly variable and generally low, especially when saturated with groundwater.

    ## Ground Investigation & Operations

    Extensive geophysical surveys and borehole investigations were conducted to map the subsurface, identify faults, flint layers, and assess the risk of cavities within the limestone. While faults were detected, no significant cavities were found.

    The stability of the excavation pit was monitored in real-time, with groundwater levels and pressures carefully controlled to prevent collapse or excessive deformation of the pit walls.

    Due to the high permeability of the gravel and fissured limestone, groundwater management was a major challenge. Over 500 wells were drilled to depths of up to 32 m for dewatering, and a reinfiltration system was implemented to return nearly all pumped water to the ground, protecting local buildings and ecosystems.

    <details>
    <summary>
        Sources
    </summary>
    <ul>
        <li><a href="https://www.tunnel-online.info/en/artikel/tunnel-a2-maastricht-groundwater-management-with-dsi-system-1564115.html">Tunnel A2 Maastricht: Groundwater Management with DSI System]</li>
        <li><a href="https://www.cob.nl/magazines-brochures-en-nieuws/verdieping/verdieping-sept2012/geotechniek-en-risicos-bij-a2-maastricht">Geotechniek-en-Risicos bij A2 Maastricht]</li>
        <li><a href="https://onepetro.org/ISRMEUROCK/proceedings-abstract/EUROCK15/All-EUROCK15/ISRM-EUROCK-2015-072/43534">Laboratory Tests on Dutch Limestone (Mergel)</li>
        <li><a href="https://a2maastricht.nl/application/files/3315/2060/1222/Interview_Eduard_van_Herk_en_Bjorn_Vink.pdf">Interview Eduard van Herk en Bjorn Vink</li>
    </ul>
    </details>
    """)
    return


@app.cell
def _(Path, pygef):
    folder_path = Path("./gefs")
    gef_files = list(folder_path.glob("*.gef"))
    boreholes = [pygef.read_bore(gef_file) for gef_file in gef_files]
    return (boreholes,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("pygef uses [polars](https://pola.rs/) for DataFrames, for consistency, we convert them to [Pandas](http://pandas.pydata.org/) DataFrames in this notebook.").callout("warn")
    return


@app.cell(hide_code=True)
def _(boreholes, mo):
    options = {d.alias: i for i, d in enumerate(boreholes)}
    multiselect = mo.ui.dropdown(options, label="Select borehole")
    multiselect
    return (multiselect,)


@app.cell(hide_code=True)
def _(multiselect):
    index = multiselect.value or 0
    index
    return (index,)


@app.cell(hide_code=True)
def _(boreholes, index):
    boreholes[index].data.to_pandas().dropna(axis=1, how='all') # drop empty columns for display
    return


@app.cell
def _(boreholes, index, plot_bore):
    plot_bore(boreholes[index])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Converting multiple GEF files to a relational database

    Rather than dealing with a folder of files in a format that not much software can handle, we would like to combine all of these files into a single database with spatial information. This is where `bedrock-ge` comes in.

    ### Relational Databases

    A [relational database](https://observablehq.com/blog/databases-101-basics-data-analysts#what-are-relational-databases) is a database with multiple tables that are linked to each other with relations. This type of database is ideal for storing GI data, given its [hierarchical structure](https://bedrock.engineer/explanation/hierarchical-structure/).

    In Python it's convenient to represent a relational database as a dictionary of DataFrames.

    ### Coordinated Reference System (CRS)

    First, let's check in which projected coordinate system the provided data was recorded.
    """)
    return


@app.cell
def _(CRS, boreholes):
    code = {bore.delivered_location.srs_name for bore in boreholes}.pop()
    projected_crs = CRS(code)
    projected_crs
    return (projected_crs,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The data is in EPSG:28992, which is the [Rijksdriehoekscoördinaten (NL)](https://nl.wikipedia.org/wiki/Rijksdriehoeksco%C3%B6rdinaten) system, also called "Amersfoort / RD New". This reference system does not include elevation.

    To represent GI data spatially in 3D geometry we need a CRS **with elevation**. That's why we will use
    [EPSG:5709](https://epsg.org/crs_5709/NAP-height.html) "Normaal Amsterdams Peil (NAP) height" as the vertical reference system.
    """)
    return


@app.cell
def _(CRS):
    vertical_crs = CRS("EPSG:5709")
    return (vertical_crs,)


@app.cell
def _(CRS):
    wgs = CRS("EPSG:4326")
    return


@app.cell
def _():
    project_uid = "Maastricht A2 tunnel"
    return (project_uid,)


@app.cell
def _(pd, project_uid, projected_crs, vertical_crs):
    project = pd.DataFrame({
        "project_uid": [project_uid], # primary key
        "horizontal_crs_wkt": projected_crs.to_wkt(),
        "vertical_crs_wkt": vertical_crs.to_wkt(),
    })
    return (project,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here, we create a new DataFrame for locations and remap the GEF keys to follow Bedrock's conventions.
    We need to map `alias` to `location_source_id` and `delivered_vertical_position_offset` to `ground_level_elevation` for example.
    We also need to create a **unique identifier** and add `project_uid` as a key to relate it the project.
    """)
    return


@app.cell
def _(boreholes, pd, project_uid):
    locations_df = pd.DataFrame([
        {
            "location_uid": f"{borehole.alias} {project_uid}", # primary key
            "project_uid": project_uid, # foreign key
            "data": process_data(borehole),
            "location_source_id": borehole.alias,
            "date": borehole.research_report_date,
            "location_type": "Hole",
            "easting": borehole.delivered_location.x,
            "northing": borehole.delivered_location.y,
            "depth_to_base": min(borehole.data["lowerBoundaryOffset"]),
            "ground_level_elevation": borehole.delivered_vertical_position_offset,
            "elevation_at_base": borehole.delivered_vertical_position_offset - min(borehole.data["lowerBoundaryOffset"]),
        }
        for borehole in boreholes
    ])
    return (locations_df,)


@app.cell
def _(locations_df):
    locations_df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here we create a DataFrame for the In-Situ data of all GI locations. To relate the in-situ data to locations and the project, we add foreign keys to each row.
    """)
    return


@app.cell
def _(locations_df, pd):
    insitu = pd.DataFrame([
        {
            **layer,
            "location_uid": location["location_uid"], # foreignkey
            "project_uid": location["project_uid"], # foreignkey
        }
        # Outer loop: iterate through each location
        for location in locations_df.to_dict('records')
        # Inner loop: iterate through each layer in the location's data dataframe
        for layer in location["data"].to_dict('records')
    ])
    insitu
    return (insitu,)


@app.cell
def _(BedrockGIDatabase, insitu, locations_df, project):
    brgi_db = BedrockGIDatabase(
            Project=project,
            Location=locations_df.drop(columns=["data"]),
            InSituTests={"interpretation": insitu},
        )
    brgi_db
    return (brgi_db,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now let's convert the various tables (`Location`, `LonLatHeight`, `In-SituTests` ) into geospatial DataFrames with interpolated geometry data using `bedrock-ge`'s `create_brgi_geodb`.
    """)
    return


@app.cell
def _(brgi_db, create_brgi_geodb):
    brgi_geodb = create_brgi_geodb(brgi_db)
    return (brgi_geodb,)


@app.cell
def _(brgi_geodb):
    brgi_geodb.InSituTests["interpretation"]
    return


@app.function
def process_data(bore):
    df = bore.data.to_pandas().dropna(axis=1, how='all').rename(columns=
    {
        'upperBoundary': 'depth_to_top',
        'lowerBoundary': 'depth_to_base',
        'upperBoundaryOffset': 'elevation_at_top',
        'lowerBoundaryOffset': 'elevation_at_base'
    })

    return df


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Displaying the GI locations on a map

    Rather than multiple tables (DataFrames) and soil profiles, we would like see an overview of what this ground investigation covers. It's **spatial** data after all, let's view it in a spatial context.

    `create_brgi_geodb` creates a `LonLatHeight` table which contains the GI locations at ground level as points in WGS84 - World Geodetic System 1984 - EPSG:4326 coordinates (Longitude, Latitude, Ellipsoidal Height).


    The reason for creating the `LonLatHeight` table is that vertical lines in projected Coordinate Reference Systems (CRS) are often not rendered nicely by default in all web-mapping software. Vertical lines are often not visible when looking at a map from above, and not all web-mapping software is capable of handling geometry in non-WGS84, i.e. (Lon, Lat) coordinates.

    `brgi_geodb.LonLatHeight` is a GeoPandas GeoDataFrame, which has an `.explore()` utility method to view the data on a webmap.
    """)
    return


@app.cell
def _(brgi_geodb):
    map = brgi_geodb.LonLatHeight.explore(marker_kwds={"radius":5})
    map
    return


@app.cell
def _(brgi_geodb):
    brgi_geodb.LonLatHeight
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Saving the GI geospatial database as a GeoPackage (.gpkg)

    Finally, we'll write it to an actual geospatial database file, a [GeoPackage](https://www.geopackage.org/), so we can share our GI data with others, for example, to reuse it in other computational notebooks, create dashboard apps, access the GI data in QGIS or ArcGIS, and more...

    A GeoPackage is an <abbr title="Open Geospatial Consortium">OGC-standardized</abbr> extension of SQLite, a relational database in a single file. SQLite is the most deployed database in the world, it's probably on every device you own.

    GeoPackage allows you to store any type of GIS data (both raster as well as vector data) in a single file that has the `.gpkg` extension. Therefore, many (open-source) GIS software packages support GeoPackage!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `check_brgi_geodb` checks that all tables in the BedrockGI geospatial database conform to their respective schemas and that all foreign key relationships are properly maintained.
    """)
    return


@app.cell
def _(brgi_geodb, check_brgi_geodb):
    check_brgi_geodb(brgi_geodb)
    return


@app.cell
def _(brgi_geodb, os, write_brgi_db_to_file):
    os.makedirs('./output', exist_ok=True)

    write_brgi_db_to_file(brgi_geodb, path="./output/A2_Maastricht.gpkg", driver="GPKG")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Visualising the Data

    As standardized geospatial data, we can visualize our GI in a wealth of ways.

    View one of the Bedrock guides to see what you can do with your data.

    * [Viewing Geotechnical Data in QGIS](https://bedrock.engineer/guides/viewing-qgis/)
    * [Viewing Geotechnical Data on a Web Map](https://bedrock.engineer/guides/viewing-webmap/)

    ### 3D Webmap with Cesium.js

    View the data from this example interactively in a [3D webmap using CesiumJS](https://www.bedrock.engineer/maastricht-a2).
    """)
    return


@app.cell
def _():
    import marimo as mo
    import pygef
    from pygef.plotting import plot_bore
    import os
    from pathlib import Path
    import pandas as pd
    import geopandas as gpd
    import matplotlib
    import pyarrow
    import folium
    import mapclassify
    import numpy as np
    from shapely.geometry import Point, LineString

    from bedrock_ge.gi.schemas import BedrockGIDatabase
    from bedrock_ge.gi.db_operations import merge_dbs
    from bedrock_ge.gi.geospatial import create_brgi_geodb
    from bedrock_ge.gi.io_utils import geodf_to_df
    from bedrock_ge.gi.validate import check_brgi_geodb
    from bedrock_ge.gi.mapper import map_to_brgi_db
    from bedrock_ge.gi.write import write_brgi_db_to_file
    from pyproj import CRS
    from typing import Dict, Tuple, Union
    return (
        BedrockGIDatabase,
        CRS,
        Path,
        check_brgi_geodb,
        create_brgi_geodb,
        mo,
        os,
        pd,
        plot_bore,
        pygef,
        write_brgi_db_to_file,
    )


if __name__ == "__main__":
    app.run()
