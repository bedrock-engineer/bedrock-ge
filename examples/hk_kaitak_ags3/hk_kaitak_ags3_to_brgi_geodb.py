# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "bedrock-ge==0.3.2",
#     "folium==0.20.0",
#     "geopandas==1.1.0",
#     "mapclassify==2.9.0",
#     "marimo",
#     "matplotlib==3.10.3",
#     "pyarrow==20.0.0",
#     "pyproj==3.7.1",
#     "requests==2.32.4",
#     "shapely==2.1.1",
# ]
# ///

import marimo

__generated_with = "0.14.7"
app = marimo.App(
    app_title="Kai Tak, HK AGS 3 data to a Bedrock GI Geospatial Database",
)


@app.cell(hide_code=True)
def _():
    # %pip install bedrock-ge geopandas folium mapclassify marimo --quiet

    import io
    import platform
    import sys
    import zipfile

    import folium
    import geopandas as gpd
    import mapclassify
    import marimo as mo
    import matplotlib
    from pyproj import CRS
    from shapely import Point

    from bedrock_ge.gi.ags import ags_to_brgi_db_mapping
    from bedrock_ge.gi.db_operations import merge_dbs
    from bedrock_ge.gi.geospatial import create_brgi_geodb
    from bedrock_ge.gi.io_utils import geodf_to_df
    from bedrock_ge.gi.mapper import map_to_brgi_db
    from bedrock_ge.gi.write import write_brgi_db_to_file

    platform_system = platform.system()
    print(platform_system)
    print(sys.version)
    # print(sys.executable)
    return (
        CRS,
        Point,
        ags_to_brgi_db_mapping,
        create_brgi_geodb,
        geodf_to_df,
        gpd,
        io,
        map_to_brgi_db,
        merge_dbs,
        mo,
        platform,
        platform_system,
        write_brgi_db_to_file,
        zipfile,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
    # AGS 3 Data in Kai Tak, Hong Kong

    This notebook demonstrates how to:

    1. Use `bedrock-ge` to load Ground Investigation (GI) data from AGS 3 files (a common GI data format in Hong Kong)
    2. Convert the AGS 3 data into a standardized GI database using `bedrock-ge`
    3. Transform the GI data into 3D GIS features with proper coordinates and geometry ([OGC Simple Feature Access](https://en.wikipedia.org/wiki/Simple_Features))
    4. Explore and analyze the GI data using:
       - Interactive filtering with Pandas dataframes
       - Visualization on interactive maps with GeoPandas
    5. Export the processed GI database to a GeoPackage file for use in GIS software

    We'll work with real GI data from the Kai Tak neighborhood in Hong Kong.

    ## Context

    Kai Tak is a neighborhood in Kowloon, Hong Kong. One of the highlights of Kai Tak used to be its airport. It holds a special place in aviation history due to its unique and challenging approach, which involved pilots making a steep descent over a densely populated area while making a sharp turn at the same time and then landing on a single runway that jutted out into Victoria Harbor. [Landing at Kai Tak Airport | YouTube](https://www.youtube.com/watch?v=OtnL4KYVtDE)

    In 1998, the new Hong Kong International Airport opened, and operations at Kai Tak Airport were ceased. After the closure, the former Kai Tak Airport and surrounding neighborhood underwent a massive redevelopment project to transform it into a new residential and commercial district, which is still continuing today.

    Have a look at the [Kai Tak Speckle Project](https://app.speckle.systems/projects/013aaf06e7/models/0e43d1f003,a739490298) to get an idea what Kai Tak looks like now. (Developments are going fast, so [Google Maps 3D](https://www.google.com/maps/@22.3065043,114.2020499,462a,35y,343.1h,75.5t/data=!3m1!1e3?entry=ttu) is a bit outdated.)

    ## The Kai Tak AGS 3 ground investigation data

    Ground Investigation Data for all of Hong Kong can be found here:  
    [GEO Data for Public Use](https://www.ginfo.cedd.gov.hk/GEOOpenData/eng/Default.aspx) → [Ground Investigation (GI) and Laboratory Test (LT) Records](https://www.ginfo.cedd.gov.hk/GEOOpenData/eng/GI.aspx)

    The Ground Investigation data specific to the Kai Tak neighborhood in Hong Kong can be found in the `bedrock-ge` GitHub repository:  
    [`github.com/bedrock-engineer/bedrock-ge/examples/hk_kaitak_ags3/kaitak_ags3.zip`](https://github.com/bedrock-engineer/bedrock-ge/blob/main/examples/hk_kaitak_ags3/kaitak_ags3.zip).  
    This archive contains GI data from 88 AGS 3 files, with a total of 834 locations (boreholes and Cone Penetration Tests).

    One of the AGS 3 files with GI data was left outside the ZIP archive, such that you can have a look at the structure of an AGS 3 file:  
    [`github.com/bedrock-engineer/bedrock-ge/examples/hk_kaitak_ags3/ASD012162 AGS.ags`](https://github.com/bedrock-engineer/bedrock-ge/blob/main/examples/hk_kaitak_ags3/64475_ASD012162%20AGS.ags)

    ### Getting the AGS 3 files

    To make it easy to run this notebook on your computer (locally) in the browser (remotely) in [marimo.app](https://marimo.app/) or [Google Colab](https://colab.research.google.com/), the code below requests the ZIP archive from GitHub and directly processes it. However, you can also download the ZIP from GitHub (link above) or directly from this notebook [by clicking this raw.githubusercontent.com raw url [ ↓ ]](http://raw.githubusercontent.com/bedrock-engineer/bedrock-ge/main/examples/hk_kaitak_ags3/kaitak_ags3.zip). 

    The cell below works as is, but has a commented line 2, to help you in case you have downloaded the ZIP, and want to use that downloaded ZIP in this notebook.
    """
    )
    return


@app.cell
async def _(io, platform_system):
    # Read ZIP from disk after downloading manually
    # zip = Path.home() / "Downloads" / "kaitak_ags3.zip"

    # Request ZIP from GitHub
    raw_githubusercontent_url = "https://raw.githubusercontent.com/bedrock-engineer/bedrock-ge/main/examples/hk_kaitak_ags3/kaitak_ags3.zip"
    # When running this marimo notebook in WebAssembly (WASM, a.k.a. Emscripten), use pyodide to request the data
    if platform_system == "Emscripten":
        from pyodide.http import pyfetch

        response = await pyfetch(raw_githubusercontent_url)
        zip = io.BytesIO(await response.bytes())
    else:
        import requests

        zip = io.BytesIO(requests.get(raw_githubusercontent_url).content)
    return (zip,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
    ## Converting the AGS 3 files to a relational database

    A relational database is a database with multiple tables that are linked to each other with relations. This type of database is ideal for storing  GI data, given its hierarchical structure:

    ```
    Project
     └───Location
          ├───InSitu_TEST
          └───Sample
              └───Lab_TEST
    ```

    Where `Project`, `Location`, `InSitu_TEST`, `Sample` and `Lab_TEST` are all tables that are linked to each other with the hierarchical structure shown above, meaning that all relations are many-to-one:

    - Each GI location (many) is related to one project.
    - Each sample or in-situ test (many) is related to one GI location.
    - Each lab test is related to one sample.

    In Python it's convenient to represent a relational database as a dictionary of dataframe's.

    ### Converting AGS 3 files to a dictionary of dataframes

    The AGS 3 files can be converted to a dictionary of dataframes using the function `list_of_ags3s_to_bedrock_gi_database(ags3_file_paths, CRS)`. The result is shown below. Have a look at the different tables and the data in those tables. Make sure to use the search and filter functionality to explore the data if you're using marimo to run this notebook!

    Notice the additional columns that were added to the tables by `bedrock-ge`:

    - To make sure that the primary keys of the GI data tables are unique when putting data from multiple AGS files together:  
        `project_uid`, `location_uid`, `sample_uid`
    - To make it possible to generate 3D GIS geometry for the `Location`, `Sample` and `InSitu_TEST` tables:  
        In the `Location` table: `easting`, `northing`, `ground_level_elevation`, `depth_to_base`  
      In the `Sample` and `InSitu_TEST` tables: `depth_to_top` and, in case the test or sample is taken over a depth interval, `depth_to_base`.
    """
    )
    return


@app.cell
def _(CRS, ags_to_brgi_db_mapping, map_to_brgi_db, merge_dbs, zip, zipfile):
    projected_crs = CRS("EPSG:2326")
    vertical_crs = CRS("EPSG:5738")

    ags3_file_brgi_dbs = []
    with zipfile.ZipFile(zip) as zip_ref:
        # Iterate over files and directories in the .zip archive
        for i, file_name in enumerate(zip_ref.namelist()):
            # Only process files that have an .ags or .AGS extension
            if file_name.lower().endswith(".ags"):
                print(f"\n🖥️ Processing {file_name} ...")
                with zip_ref.open(file_name) as ags3_file:
                    # 1. Convert content of a single AGS 3 file to a Bedrock GI Mapping.
                    # 2. Map the mapping object to a Bedrock GI Database.
                    # 3. Append the Bedrock GI Database to the list of Bedrock GI
                    #    Databases, that were created from single AGS 3 files.
                    ags3_file_brgi_dbs.append(
                        map_to_brgi_db(
                            ags_to_brgi_db_mapping(
                                ags3_file, projected_crs, vertical_crs
                            )
                        )
                    )

    brgi_db = merge_dbs(ags3_file_brgi_dbs)
    return (brgi_db,)


@app.cell
def _(brgi_db):
    brgi_db.Project
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Relational database to 3D geospatial database
    A  database is a relational database that has been enhanced to store  data. There are two broad categories of  data:

    1. [Raster data](https://en.wikipedia.org/wiki/GIS_file_format#Raster_formats): geographic information as a grid of pixels (cells), where each pixel stores a value corresponding to a specific location and attribute, such as elevation, temperature, or land cover. So, a Digital Elevation Model (DEM) is an example of GIS raster data.
    2. [Vector data](https://en.wikipedia.org/wiki/GIS_file_format#Vector_formats): tables in which each row contains:
        - [Simple feature GIS geometry](https://en.wikipedia.org/wiki/Simple_Features), represented as [Well-Known Text](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry). For example in the `InSitu_GEOL` and `InSitu_ISPT` tables:  
            `InSitu_GEOL`: a depth interval in a borehole where sand was found.  
            `InSitu_ISPT`: a point in a borehole where an SPT test was performed.
        - Attributes that describe the GIS geometry. For example in the `InSitu_GEOL` and `InSitu_ISPT` tables:  
            `InSitu_GEOL`: the geology code (`GEOL_GEOL`), general description of stratum (`GEOL_DESC`), etc.  
            `InSitu_ISPT`: the SPT N-value (`ISPT_NVAL`), energy ratio of the hammer (`ISPT_ERAT`), etc.

    So, when representing GI data as 3D GIS features, we are talking about GIS vector data.

    ### From GI dataframe to `geopandas.GeoDataFrame` 

    In order to construct the 3D simple feature GIS geometry of the `Location`s, `Sample`s and `InSitu_TEST`s, a few more columns have to be calculated for each of these tables: `elevation_at_top` and `elevation_at_base` if the in-situ test or sample was taken over a depth interval.

    The 3D simple feature GIS geometry as [WKT](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry) for point tests and samples:  
    `POINT (easting northing elevation_at_top)`

    The 3D simple feature GIS geometry as WKT for in-situ tests and samples taken over a depth interval:  
    `LINESTRING (easting northing elevation_at_top, easting northing elevation_at_base)`

    Additionally, a `LonLatHeight` table is created which contains the GI locations at ground level in WGS84 - World Geodetic System 1984 - EPSG:4326 coordinates (Longitude, Latitude, Ellipsoidal Height), which in WKT looks like:  
    `POINT (longitude latitude wgs84_ground_level_height)`

    The reason for creating the `LonLatHeight` table is that vertical lines in projected Coordinate Reference Systems (CRS) are often not rendered nicely by default in all web-mapping software. Vertical lines are often not visible when looking at a map from above, and not all web-mapping software is capable of handling geometry in non-WGS84, i.e. (Lon, Lat) coordinates.
    """
    )
    return


@app.cell
def _(brgi_db, create_brgi_geodb):
    brgi_geodb = create_brgi_geodb(brgi_db)
    return (brgi_geodb,)


@app.cell
def _(brgi_geodb):
    brgi_geodb.LonLatHeight.explore()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Ground Investigation data exploration

    After creating the Bedrock GI 3D  Database `brgi_geodb` - which is a dictionary of [`geopandas.GeoDataFrame`](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.html#geopandas.GeoDataFrame)s - you can explore the Kai Tak Ground Investigation data on an interactive map by applying the [`geopandas.GeoDataFrame.explore()`](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.explore.html#geopandas.GeoDataFrame.explore) method to the different tables in the `brgi_geodb`.

    Do note that this works best on the tables with `POINT` GIS geometry such as `LonLatHeight` or `ISPT` (SPT data). Tables with vertical `LINESTRING` GIS geometry, such as `Location`, `GEOL` (Stratum descriptions) or `WETH` (Weathering grades), display very small on the `leaflet`-based interactive map created with `geodf.explore()`, and don't show at all on the `matplotlib`-based map created with `geodf.plot()`.

    Therefore, a convenience function is defined below to just plot the first coordinate of a `LINESTRING`, which makes the data more visible. The data displayed below is the `GEOL` table (Stratum descriptions):
    """
    )
    return


@app.cell(hide_code=True)
def _(Point, brgi_geodb, gpd, mo):
    def gi_exploration_map(geodf):
        if "geometry" not in geodf.columns:
            output = mo.md(
                "No interactive map with the data selected in the table above can be shown, because the data you're exploring doesn't have a 'geometry' column."
            ).callout("warn")
        else:
            fltrd_geodf = gpd.GeoDataFrame(geodf.copy())
            fltrd_geodf["geometry"] = fltrd_geodf["geometry"].apply(
                lambda geom: Point(geom.coords[0])
            )
            output = fltrd_geodf.explore()
        return output

    geol_geodf = brgi_geodb.InSituTests["GEOL"]
    gi_exploration_map(geol_geodf)
    return geol_geodf, gi_exploration_map


@app.cell(hide_code=True)
def _(geodf_to_df, geol_geodf):
    geodf_to_df(geol_geodf)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    With marimo's built-in data exploration tables and dataframes, it's also really easy to filter and visualize the GI data.

    For example, in the `ISPT` table (SPT data) you could apply a filter to the `ISPT_NVAL` column (SPT N-value) of e.g. 1 - 10. When you then select those rows and then scroll to the map below, you'll see all the locations where soft soils were encountered.
    """
    )
    return


@app.cell(hide_code=True)
def _(brgi_geodb, mo):
    explore_brgi_table = mo.ui.dropdown(brgi_geodb.InSituTests, value="ISPT")
    mo.md(f"Select the In-Situ Test results you want to explore: {explore_brgi_table}")
    return (explore_brgi_table,)


@app.cell(hide_code=True)
def _(explore_brgi_table, geodf_to_df, mo):
    spt_1_10 = [
        1,
        2,
        13,
        28,
        29,
        30,
        47,
        48,
        50,
        52,
        68,
        69,
        96,
        101,
        116,
        117,
        118,
        119,
        120,
        123,
        139,
        140,
        141,
        142,
        162,
        163,
        164,
        166,
        168,
        173,
        184,
        185,
        189,
        191,
        198,
        199,
        213,
        214,
        215,
        244,
        245,
        251,
        259,
        261,
        275,
        277,
        279,
        281,
        295,
        299,
        331,
        333,
        334,
        335,
        350,
        375,
        393,
        396,
        407,
        409,
        411,
        413,
        414,
        415,
        416,
        419,
        420,
        421,
        444,
        446,
        454,
        455,
        456,
        458,
        459,
        461,
        479,
        481,
        495,
        496,
        499,
        515,
        517,
        519,
        530,
        531,
        534,
        546,
        547,
        548,
        578,
        610,
        725,
        726,
        814,
        832,
        833,
        834,
        835,
        849,
        850,
        851,
        881,
        895,
        896,
        947,
        957,
        990,
        993,
        1035,
        1052,
        1066,
        1067,
        1068,
        1069,
        1090,
        1091,
        1093,
        1131,
        1132,
        1163,
        1181,
        1182,
        1183,
        1184,
        1193,
        1194,
        1195,
        1197,
        1199,
        1222,
        1251,
        1267,
        1285,
        1286,
        1287,
        1302,
        1319,
        1491,
        1679,
        1727,
        1731,
        1782,
        1787,
        1811,
        1814,
        1870,
        1898,
        1899,
        1900,
        1919,
        1921,
        1923,
        1944,
        1948,
        1949,
        1950,
        1955,
        1957,
        1961,
        1962,
        1967,
        1973,
        1980,
        1988,
        1989,
        2014,
        2029,
        2030,
        2035,
        2036,
        2037,
        2046,
        2060,
        2066,
        2072,
        2078,
        2098,
        2115,
        2116,
        2125,
        2126,
        2127,
        2128,
        2145,
        2150,
        2152,
        2159,
        2160,
        2161,
        2164,
        2174,
        2175,
        2186,
        2188,
        2191,
        2194,
        2195,
        2196,
        2198,
        2204,
        2205,
        2206,
        2207,
        2208,
        2212,
        2233,
        2240,
        2241,
        2242,
        2244,
        2251,
        2252,
        2254,
        2255,
        2256,
        2258,
        2266,
        2267,
        2268,
        2269,
        2270,
        2286,
        2287,
        2288,
        2297,
        2299,
        2300,
        2302,
        2303,
        2307,
        2314,
        2315,
        2317,
        2336,
        2337,
        2338,
        2339,
        2340,
        2341,
        2343,
        2349,
        2350,
        2351,
        2352,
        2374,
        2375,
        2380,
        2394,
        2397,
        2404,
        2406,
        2417,
        2421,
        2422,
        2434,
        2457,
        2479,
        2480,
        2482,
        2493,
        2504,
        2505,
        2523,
        2525,
        2526,
        2535,
        2537,
        2548,
        2552,
        2565,
        2567,
        2582,
        2584,
        2601,
        2602,
        2622,
        2626,
        2636,
        2638,
        2639,
        2648,
        2649,
        2664,
        2666,
        2667,
        2677,
        2679,
        2701,
        2717,
        2718,
        2719,
        2720,
        2723,
        2742,
        2744,
        2745,
        2746,
        2747,
        2750,
        2754,
        2755,
        2761,
        2766,
        2769,
        2785,
        2786,
        2787,
        2802,
        2807,
        2825,
        2826,
        2844,
        2848,
        2874,
        2875,
        2909,
        2921,
        2935,
        2936,
        2937,
        2964,
        2965,
        2966,
        2967,
        2969,
        2977,
        2978,
        2996,
        3010,
        3011,
        3012,
        3016,
        3043,
        3045,
        3087,
        3088,
        3091,
        3094,
        3107,
        3108,
        3110,
        3112,
        3120,
        3121,
        3122,
        3136,
        3137,
        3138,
        3139,
        3140,
        3156,
        3157,
        3158,
        3161,
        3173,
        3175,
        3177,
        3178,
        3188,
        3192,
        3203,
        3204,
        3205,
        3206,
        3207,
        3221,
        3222,
        3245,
        3246,
        3247,
        3248,
        3249,
        3272,
        3286,
        3287,
        3288,
        3299,
        3300,
        3373,
        3374,
        3377,
        3378,
        3390,
        3391,
        3413,
        3414,
        3415,
        3416,
        3417,
        3418,
        3421,
        3422,
        3450,
        3451,
        3452,
        3464,
        3486,
        3487,
        3489,
        3490,
        3493,
        3494,
        3524,
        3533,
    ]
    filtered_table = mo.ui.table(
        geodf_to_df(explore_brgi_table.value), initial_selection=spt_1_10
    )
    filtered_table
    return (filtered_table,)


@app.cell(hide_code=True)
def _(explore_brgi_table, filtered_table, gi_exploration_map):
    gi_exploration_map(explore_brgi_table.value.loc[filtered_table.value.index])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Something else you might be interested in, is where the weathering grade of the soil or rock is low. Weathering grades range from `I` (Fresh Rock) to `VI` (Residual Soil). All rock with a weathering grade of `III` (Moderately Decomposed) or better is considered competent rock.

    The weathering grades can be found in the `WETH_GRAD` column in the `WETH` table (Weathering grades). Therefore, to find all competent rock, we need to filter out all the rows that contain a `V`, which you can do in the widget below.

    That widget also shows the Python code that creates the filter:

    ```python
    df_next = df
    df_next = df_next[~((df_next["WETH_GRAD"].str.contains("V")))]
    ```
    """
    )
    return


@app.cell(hide_code=True)
def _(brgi_geodb, mo):
    explore_brgi_df = mo.ui.dropdown(brgi_geodb.InSituTests, value="WETH")
    mo.md(f"Select the GI table you want to explore: {explore_brgi_df}")
    return (explore_brgi_df,)


@app.cell(hide_code=True)
def _(explore_brgi_df, geodf_to_df, mo):
    filtered_df = mo.ui.dataframe(geodf_to_df(explore_brgi_df.value))
    filtered_df
    return (filtered_df,)


@app.cell(hide_code=True)
def _(explore_brgi_df, filtered_df, gi_exploration_map):
    gi_exploration_map(explore_brgi_df.value.loc[filtered_df.value.index])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Saving the GI  database as a GeoPackage (.gpkg)

    Finally, lets write, i.e. persist `brgi_geodb` - a Python dictionary of `geopandas.GeoDataFrames` - to an actual  database file, so we can share our GI data with others.
    For example, to reuse it in other notebooks, create dashboards, access the GI data in QGIS or ArcGIS, and more...

    A GeoPackage is an OGC-standardized extension of SQLite (a relational database in a single file, .sqlite or .db) that allows you to store any type of GIS data (both raster as well as vector data) in a single file that has the .gpkg extension. Therefore, QGSI, ArcGIS and many other (open-source) GIS software packages support GeoPackage!

    > [What about Shapefile and GeoJSON?](#what-about-shapefile-and-geojson)
    """
    )
    return


@app.cell(hide_code=True)
def _(brgi_geodb, mo, platform, write_brgi_db_to_file):
    output = None
    if platform.system() != "Emscripten":
        write_brgi_db_to_file(
            brgi_geodb, mo.notebook_dir() / "kaitak_gi.gpkg", driver="GPKG"
        )
    else:
        output = mo.md(
            "Writing a GeoPackage from WebAssembly (marimo playground) causes geopandas to think that the GeoDataFrames in the `brgi_geodb` don't have a geometry column. You can [download the GeoPackage from GitHub](https://github.com/bedrock-engineer/bedrock-ge/blob/main/examples/hk_kaitak_ags3/kaitak_gi.gpkg)"
        ).callout("warn")
    output
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
    ## What's next?

    As mentioned above, the `kaitak_gi.gpkg` GeoPackage can be loaded into QGIS or ArcGIS. QGIS and ArcGIS have [connectors for the Speckle platform](https://www.speckle.systems/connectors), which allows you to publish GIS data to Speckle.

    With the Speckle viewer you can visualize the GI data in context with data from other AEC software such as Civil3D (Click the balloon!):

    <iframe title="Speckle" src="https://app.speckle.systems/projects/013aaf06e7/models/1cbe68ed69,44c8d1ecae,9535541c2b,a739490298,ff81bfa02b#embed=%7B%22isEnabled%22%3Atrue%7D" width="100%" height="400" frameborder="0"></iframe>

    Additionally, you can load the GI data in other software that Speckle has a connector for, such as Rhino / Grasshopper to enable parametric geotechnical engineering workflows.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## What about Shapefile and GeoJSON?

    ### Shapefile

    Bluntly put, Shapefile is a bad format.

    Among other problems, Shapefile isn't just a single file. One has to at least share three files [(\*.shp, \*.dbf, \*.shx)](https://en.wikipedia.org/wiki/Shapefile#Mandatory_files), which doesn't include the definition of a CRS. In case that doesn't sound terrible enough to you yet, please have a look at the fantastic website [switchfromshapefile.org](http://switchfromshapefile.org/).

    ### GeoJSON

    GeoJSON is a nice, human readable file format for GIS vector data, which is especially useful for web services, but has a few drawbacks:

    - Although it is technically possible to use GeoJSON with more CRSs, the [specification states clearly](https://tools.ietf.org/html/rfc7946#section-4) that WGS84, with EPSG:4326 and coordinates (Lon, Lat, Height), is the only CRS that should be used in GeoJSON (see [switchfromshapefile.org](http://switchfromshapefile.org/#geojson)).
    - GeoJSON support in ArcGIS isn't fantastic. You have to go through [Geoprocessing - JSON to Features conversion tool](https://pro.arcgis.com/en/pro-app/latest/tool-reference/conversion/json-to-features.htm) to add a GeoJSON to your ArcGIS project, which is a bit cumbersome.
    """
    )
    return


if __name__ == "__main__":
    app.run()
