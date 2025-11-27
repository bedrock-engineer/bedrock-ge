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
app = marimo.App(width="columns")


@app.cell(column=0, hide_code=True)
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
    3. [PDOK](https://app.pdok.nl/viewer)
      1. WMS - This is useful for quickly viewing the location of historic CPTs or geotechnical boreholes.
      2. ATOM feed - For downloading the whole dataset, i.e. to download all CPTs or all geotechnical boreholes in BRO.
    """
    )
    return


@app.cell(hide_code=True)
def _(Request, bounds, datetime, json, minidom, mo, pl, urlopen, xmltodict):
    cpt_search_url = "https://publiek.broservices.nl/sr/cpt/v1/characteristics/searches"
    api_request_data = json.dumps(
        {
            "registrationPeriod": {
                "beginDate": "2017-01-01",
                "endDate": datetime.date.today().isoformat(),
            },
            "area": {
                "boundingBox": {
                    "lowerCorner": {
                        "lon": bounds[0],
                        "lat": bounds[1],
                    },
                    "upperCorner": {
                        "lon": bounds[2],
                        "lat": bounds[3],
                    },
                }
            },
        }
    ).encode("utf-8")

    cpt_search_req = Request(
        cpt_search_url,
        data=api_request_data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(cpt_search_req, timeout=30) as cpt_search_resp:
        xml = cpt_search_resp.read()

    cpt_search_dict = xmltodict.parse(
        xml,
        xml_attribs=False,
        process_namespaces=True,
        namespaces={
            "http://www.opengis.net/gml/3.2": None,
            "http://www.broservices.nl/xsd/dscpt/1.1": None,
            "http://www.broservices.nl/xsd/brocommon/3.0": None,
        },
    )

    def to_bool(col: str) -> pl.Expr:
        truthy = ["ja", "yes", "true", "1"]
        return pl.col(col).str.to_lowercase().is_in(truthy)

    def parse_pos(col: str) -> pl.Expr:
        return (
            pl.col(col)
            .struct.field("pos")
            .str.split(" ")
            .cast(pl.Array(float, 2))
            .alias(col)
        )

    cpt_search_df = (
        pl.DataFrame(
            cpt_search_dict["dispatchCharacteristicsResponse"]["dispatchDocument"]
        )
        .unnest("CPT_C")
        .with_columns(
            # Casts
            pl.col("deliveryAccountableParty").cast(int),
            pl.col("objectRegistrationTime").cast(pl.Datetime),
            pl.col("offset").cast(float),
            pl.col("startTime").cast(pl.Date),
            pl.col("predrilledDepth").cast(float),
            pl.col("finalDepth").cast(float),
            # "ja" / "nee" -> boolean
            to_bool("deregistered"),
            to_bool("underReview"),
            to_bool("dissipationTestPerformed"),
            # {"pos":"lon lat"} -> pl.Array[float,2 ] (keeps [lon, lat])
            parse_pos("standardizedLocation"),
            parse_pos("deliveredLocation"),
            # {"date":"YYYY-MM-DD"} -> pl.Date
            pl.col("researchReportDate")
            .struct.field("date")
            .cast(pl.Date)
            .alias("researchReportDate"),
        )
    )
    cpt_search_table = mo.ui.table(cpt_search_df)

    tabs = mo.ui.tabs(
        {
            "DataFrame": cpt_search_table,
            "XML": mo.md(
                f"```xml\n{minidom.parseString(xml).toprettyxml(indent='  ')}\n```"
            ),
            "JSON": xmltodict.parse(xml),
            "JSON, no XML attributes": cpt_search_dict,
        }
    )

    tabs
    return (cpt_search_df,)


@app.cell
def _(BytesIO, Request, cpt_search_df, pl, read_cpt, urlopen):
    cpts = []
    cpt_data = []
    for bro_id in cpt_search_df["broId"]:
        cpt_get_url = f"https://publiek.broservices.nl/sr/cpt/v1/objects/{bro_id}"
        cpt_get_req = Request(cpt_get_url, method="GET")
        with urlopen(cpt_get_req, timeout=30) as resp:
            cpt_xml = resp.read()
            cpt_obj = read_cpt(BytesIO(cpt_xml))
        cpt_data.append(
            cpt_obj.data.with_columns(pl.lit(cpt_obj.bro_id).alias("broId"))
        )
        cpt_dict = cpt_obj.__dict__.copy()
        del cpt_dict["data"]
        cpt_dict["delivered_location"] = [
            cpt_dict["delivered_location"].x,
            cpt_dict["delivered_location"].y,
        ]
        cpt_dict["standardized_location"] = [
            cpt_dict["standardized_location"].x,
            cpt_dict["standardized_location"].y,
        ]
        cpt_dict["delivered_vertical_position_datum"] = cpt_dict["delivered_vertical_position_datum"]._name_
        cpts.append(cpt_dict)

    cpts_df = pl.DataFrame(cpts).cast(
        {
            "delivered_location": pl.Array(float, 2),
            "standardized_location": pl.Array(float, 2),
        }
    )
    cpt_data_df = pl.concat(cpt_data, how="diagonal_relaxed")
    return (cpt_data_df,)


@app.cell(hide_code=True)
def _():
    import datetime
    import json
    import xml.dom.minidom as minidom
    from io import BytesIO
    from urllib.request import Request, urlopen

    import folium
    import geopandas as gpd
    import marimo as mo
    import polars as pl
    import xmltodict

    from folium.plugins import Draw
    from lxml import etree
    from pygef import read_cpt
    from pygef.plotting import plot_cpt

    cwd = mo.notebook_location()
    return (
        BytesIO,
        Draw,
        Request,
        datetime,
        folium,
        gpd,
        json,
        minidom,
        mo,
        pl,
        read_cpt,
        urlopen,
        xmltodict,
    )


@app.cell(column=1, hide_code=True)
def _(Draw, buffer, folium, geojson_text_area, gpd, json, site_geojson):
    geojson = geojson_text_area.value if geojson_text_area.value else site_geojson
    # Create a folium interactive map (leaflet.js maps)
    site = gpd.GeoDataFrame.from_features(
        {
            "type": "FeatureCollection",
            "name": "site",
            "features": [json.loads(geojson)],
        },
        crs=4326,
    ).to_crs(28992)
    buffered_site = site.geometry.buffer(buffer.value)
    bounds = buffered_site.to_crs(4326).bounds.to_numpy()[0]
    folium_map = buffered_site.explore(
        # tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
        tiles="CartoDB positron",
        style_kwds={"fillOpacity": 0.1},
        attr=("Esri.WorldStreetMap"),
    )
    site.explore(m=folium_map, color="red", style_kwds={"fill": False})
    bounds_rectangle = folium.Rectangle(
        bounds=[[bounds[1], bounds[0]], [bounds[3], bounds[2]]],
        color="black",
        weight=0.5,
    )
    bounds_rectangle.add_to(folium_map)

    # Add PDOK's CPT WMS layer
    folium.WmsTileLayer(
        url="https://service.pdok.nl/bzk/geologie/bro-geotechnisch-sondeeronderzoek/wms/v1_0?request=GetCapabilities&service=WMS",
        name="BRO CPT",
        fmt="image/png",
        layers="GE.conePenetrationTest",
        transparent=True,
    ).add_to(folium_map)

    # Add PDOK's geotechnical borehole WMS layer
    folium.WmsTileLayer(
        url="https://service.pdok.nl/bzk/geologie/bro-geotechnisch-booronderzoek/wms/v1_0?request=getcapabilities&service=wms",
        name="BRO BHR-GT",
        fmt="image/png",
        layers="GE.Borehole",
        transparent=True,
    ).add_to(folium_map)

    # Add drawing widget
    draw = Draw(
        export=True,
        filename="site.geojson",
        position="topleft",
        draw_options={
            "polyline": True,
            "polygon": True,
            "circle": False,
            "rectangle": False,
            "marker": True,
            "circlemarker": False,
        },
    ).add_to(folium_map)

    folium_map
    return bounds, bounds_rectangle, site


@app.cell(hide_code=True)
def _(mo):
    site_geojson = '{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[4.902889698063478,52.385435257999404],[4.902923632305726,52.385509906165986],[4.902901716440955,52.385619936470341],[4.903006347021203,52.38569026942325],[4.90389499998988,52.385854235381281],[4.904091535809526,52.385902562073795],[4.904285950739031,52.385988859607401],[4.904484607448818,52.38602683046868],[4.904532680958658,52.386042363993511],[4.904790722592364,52.386094573856099],[4.904799206152918,52.386073862513044],[4.904974533071164,52.386108812898868],[4.904999276789463,52.386100183176488],[4.905287541107636,52.385853480276289],[4.903576336246269,52.385074312916224],[4.903554420381488,52.385093082996256],[4.903498923756159,52.38509416173622],[4.903484784488561,52.385100202679702],[4.903473119592793,52.385110990076754],[4.903287895187223,52.385027927051986],[4.903256788798504,52.38504302943177],[4.903150390809821,52.38513472234078],[4.903119637902792,52.385127171167227],[4.903098782483085,52.38514421524286],[4.903084996697174,52.385139037296511],[4.90302349088312,52.385198152147602],[4.902889698063478,52.385435257999404]]]}}'
    geojson_text_area = mo.ui.text_area(
        placeholder="1. Draw a shape on the map.\n2. Click it.\n3. Copy the GeoJSON from the pop-up.\n4. Paste GeoJSON here.",
        debounce=5,
        full_width=True,
    )
    buffer = mo.ui.slider(start=0, stop=200, label="Buffer", value=100, step=10)
    mo.hstack(
        [geojson_text_area, buffer],
        widths=[1, 0],
    )
    return buffer, geojson_text_area, site_geojson


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""The bouding box around the site + buffer that we created above is now used to make a call to the BRO API to retrieve all the CPT characteristics of the CPTs in that bounding box.""")
    return


@app.cell(hide_code=True)
def _(bounds_rectangle, cpt_search_df, gpd, site):
    cpt_search_gdf = gpd.GeoDataFrame(cpt_search_df.to_pandas(), geometry=gpd.points_from_xy(cpt_search_df["deliveredLocation"].arr.get(0), cpt_search_df["deliveredLocation"].arr.get(1)), crs=28992)
    cpt_map = cpt_search_gdf.explore(tiles="CartoDB positron")
    bounds_rectangle.add_to(cpt_map)
    site.explore(m=cpt_map, color="red", style_kwds={"fill": False})
    cpt_map
    return


@app.cell
def _(cpt_data_df):
    cpt_data_df
    return


@app.cell
def _(cpt_data_df, mo):
    mo.ui.dataframe(cpt_data_df)
    return


@app.cell
def _(cpt_data_df):
    cpt_data_df.filter(cpt_data_df["broId"].contains("CPT000000198163"))
    return


if __name__ == "__main__":
    app.run()
