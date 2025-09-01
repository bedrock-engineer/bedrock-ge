import marimo

__generated_with = "0.14.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import geopandas as gpd
    from bedrock_ge.gi.geospatial import create_brgi_geodb
    from bedrock_ge.gi.mapper import map_to_brgi_db
    from bedrock_ge.gi.mapping_models import (
        BedrockGIMapping,
        ProjectTableMapping,
        LocationTableMapping,
        InSituTestTableMapping,
    )
    from bedrock_ge.gi.write import write_brgi_db_to_file
    from bedrock_ge.gi.io_utils import geodf_to_df
    from pyproj import CRS
    from pathlib import Path
    return (
        BedrockGIMapping,
        CRS,
        InSituTestTableMapping,
        LocationTableMapping,
        Path,
        ProjectTableMapping,
        create_brgi_geodb,
        map_to_brgi_db,
        mo,
        pd,
        write_brgi_db_to_file,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # New Zealand Weka Hills Leapfrog Demo Project

    Weka Hills is a ficticious location in New Zealand that is used in Leapfrog Works training. The data relevant to this ficticious project can be downloaded from here:  
    https://files.seequent.com/training/Data/Works/Weka_Hills.zip

    The Ground Investigation (GI) data as CSV's can be found here:  
    https://github.com/bedrock-engineer/bedrock-ge/tree/main/examples/nz_weka_hills_leapfrog
    """
    )
    return


@app.cell
def _(mo):
    nb_dir = mo.notebook_location()
    gi_csvs = [
        file.name
        for file in nb_dir.iterdir()
        if (file.is_file() and file.suffix.lower() == ".csv")
    ]
    gi_csvs
    return (nb_dir,)


@app.cell
def _(Path):
    csv_files = {
        "cpt_collar": Path("WH_cpt_collar.csv"),
        "spt_all": Path("WH_SPT_all.csv"),
        "collar_all": Path("WH_collar_all.csv"),
        "geol_all": Path("WH_Geol_all.csv"),
        "cpt_alluvial": Path("WH_cpt_Alluvial.csv"),
        "survey_all": Path("WH_survey_all.csv")
    }
    return (csv_files,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""All borehole inclinations are 90°, so vertical, so there's no need to bother with the borehole inclination, i.e. survey data:""")
    return


@app.cell
def _(csv_files, nb_dir, pd):
    bh_inclination_df = pd.read_csv(nb_dir / csv_files["survey_all"])
    bh_inclination_df["Inclination"].unique()
    return


@app.cell
def _(csv_files, nb_dir, pd):
    bh_location_df = pd.read_csv(nb_dir / csv_files["collar_all"])
    cpt_data_df = pd.read_csv(nb_dir / csv_files["cpt_alluvial"])
    cpt_location_df = pd.read_csv(nb_dir / csv_files["cpt_collar"] )
    geol_df = pd.read_csv(nb_dir / csv_files["geol_all"])
    spt_df = pd.read_csv(nb_dir / csv_files["spt_all"])
    spt_df
    return bh_location_df, geol_df, spt_df


@app.cell
def _(bh_location_df):
    bh_location_df.columns
    return


@app.cell
def _(
    BedrockGIMapping,
    CRS,
    InSituTestTableMapping,
    LocationTableMapping,
    ProjectTableMapping,
    bh_location_df,
    create_brgi_geodb,
    geol_df,
    map_to_brgi_db,
    mo,
    spt_df,
):
    brgi_geodb = create_brgi_geodb(
        map_to_brgi_db(
            BedrockGIMapping(
                Project=ProjectTableMapping(
                    data={
                        "name": "Weka Hills Leapfrog demo project",
                        "description": "Weka Hills is a ficticious location in New Zealand that is used in Leapfrog Works training.",
                    },
                    project_id="WekaHills",
                    horizontal_crs=CRS("EPSG:2193"),
                    vertical_crs=CRS("EPSG:7839"),
                ),
                Location=LocationTableMapping(
                    data=bh_location_df,
                    location_id_column="LocationID",
                    easting_column="Easting",
                    northing_column="Northing",
                    ground_level_elevation_column="GroundLevel",
                    depth_to_base_column="FinalDepth",
                ),
                InSitu=[
                    InSituTestTableMapping(
                        table_name="Geology",
                        data=geol_df,
                        location_id_column="HoleID",
                        depth_to_top_column="from",
                        depth_to_base_column="to",
                    ),
                    InSituTestTableMapping(
                        table_name="SPT",
                        data=spt_df,
                        location_id_column="holeid",
                        depth_to_top_column="from",
                        depth_to_base_column="to",
                    ),
                ],
            )
        )
    )

    cols = brgi_geodb.Location.columns
    brgi_geodb.Location = brgi_geodb.Location.drop(columns=["Easting", "Northing"])
    print(cols)
    mo.callout('When the column name in the data is the same (case insensitive) as one of the Bedrock GI standard column names, writing to a database such as GeoPackage becomes impossible. For the Weka Hills GI data this means that "Easting" & "easting" and "Northing" & "northing" cause a conflict.', kind="danger")
    return (brgi_geodb,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""The Weka Hills is a fictional location in New Zealand, therefore it looks like some of the boreholes are in the water 🙄""")
    return


@app.cell
def _(brgi_geodb):
    brgi_geodb.LonLatHeight.explore()
    return


@app.cell
def _(brgi_geodb, mo, write_brgi_db_to_file):
    write_brgi_db_to_file(
        brgi_geodb, mo.notebook_dir() / "wekahills_gi.gpkg", driver="GPKG"
    )
    return


if __name__ == "__main__":
    app.run()
