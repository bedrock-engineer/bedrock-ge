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
def _():
    import datetime
    import json
    import xml.dom.minidom as minidom
    from io import BytesIO
    from urllib.request import Request, urlopen

    import folium
    import geopandas as gpd
    import marimo as mo
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
        etree,
        folium,
        gpd,
        json,
        minidom,
        mo,
        plot_cpt,
        read_cpt,
        urlopen,
        xmltodict,
    )


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
    3. [PDOK](https://app.pdok.nl/viewer)
      1. WMS - This is useful for quickly viewing the location of historic CPTs or geotechnical boreholes.
      2. ATOM feed - For downloading the whole dataset, i.e. to download all CPTs or all geotechnical boreholes in BRO.
    """
    )
    return


@app.cell(hide_code=True)
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
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
        style_kwds={"fillOpacity": 0.1},
        attr=("Esri.WorldStreetMap"),
    )
    site.explore(m=folium_map, color="red", style_kwds={"fill": False})
    folium.Rectangle(
        bounds=[[bounds[1], bounds[0]], [bounds[3], bounds[2]]],
        color="black",
        weight=0.5,
    ).add_to(folium_map)

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
    return (bounds,)


@app.cell
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


@app.cell
def _(buffer):
    # EPSG:4258 is the European Terrestrial Reference System 1989 (ETR)
    # ETR89 coordinates are in [Longitude (x), Latitude (y)]
    lonlat_bounds = buffer.to_crs(4258).bounds
    lonlat_bounds
    return


@app.cell
def _(Request, bounds, datetime, json, minidom, mo, urlopen, xmltodict):
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

    cpt_search = xmltodict.parse(
        xml,
        xml_attribs=False,
        process_namespaces=True,
        namespaces={
            "http://www.broservices.nl/xsd/dscpt/1.1": None,
            "http://www.broservices.nl/xsd/brocommon/3.0": None,
        },
    )

    tabs = mo.ui.tabs(
        {
            "XML": mo.md(
                f"```xml\n{minidom.parseString(xml).toprettyxml(indent='  ')}\n```"
            ),
            "JSON": xmltodict.parse(xml),
            "JSON, no XML attributes": cpt_search,
        }
    )

    tabs
    return


app._unparsable_cell(
    r"""
    for cpt in cpt_search
    """,
    name="_",
)


@app.cell
def _(Request, etree, urlopen):
    cpt_get_url = "https://publiek.broservices.nl/sr/cpt/v1/objects/CPT000000198164"
    cpt_get_req = Request(cpt_get_url, method="GET")
    with urlopen(cpt_get_req, timeout=30) as resp:
        cpt_str = resp.read()
        cpt_xml = etree.fromstring(cpt_str)

    print(etree.tostring(cpt_xml, pretty_print=True, encoding="unicode"))
    return (cpt_str,)


@app.cell
def _(cpt_str):
    cpt_str
    return


@app.cell
def _(BytesIO, cpt_str, read_cpt):
    cpt_data = read_cpt(BytesIO(cpt_str))
    cpt_data.__dict__
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
