import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pyproj
    from pyproj import CRS, Transformer
    from pyproj.crs.crs import CompoundCRS

    print(f"pyproj version: {pyproj.__version__}")
    print(f"PROJ version:   {pyproj.proj_version_str}")
    pyproj.network.set_network_enabled(active=True)
    print(f"PROJ network enabled for geoid grid streaming? {pyproj.network.is_network_enabled()}")
    return CRS, CompoundCRS, Transformer, mo


@app.cell
def _(CRS, CompoundCRS):
    wgs84 = CRS(4326)
    wgs84_3d = wgs84.to_3d() # = CRS(4979)

    egm2008_3855 = CRS(3855)
    wgs84_egm2008_9518 = CRS(9518)

    world_mercator_3395 = CRS(3395)
    world_mercator_3d = world_mercator_3395.to_3d()
    world_mercator_egm2008_6893 = CRS(6893)

    web_mercator_3857 = CRS(3857)
    web_mercator_3d = web_mercator_3857.to_3d()

    nl_rdnew_28992 = CRS(28992)
    nl_3d = nl_rdnew_28992.to_3d()
    nl_rdnew_nap_7415 = CRS(7415)

    uk_grid_27700 = CRS(27700)
    uk_3d = uk_grid_27700.to_3d()
    uk_grid_odn_7405 = CRS(7405)

    swiss_2056 = CRS(2056)
    swiss_3d = swiss_2056.to_3d()
    # https://pyproj4.github.io/pyproj/stable/build_crs.html#compound-crs
    swiss_lhn95_height = CRS("EPSG:5729")
    swiss_compound = CompoundCRS(
        name="CH1903+ / LV95 + LHN95 height",
        components=[swiss_2056, swiss_lhn95_height]
    )
    return (
        swiss_2056,
        swiss_3d,
        swiss_compound,
        swiss_lhn95_height,
        wgs84,
        wgs84_3d,
        wgs84_egm2008_9518,
        world_mercator_3395,
        world_mercator_3d,
        world_mercator_egm2008_6893,
    )


@app.cell
def _(world_mercator_3d):
    world_mercator_3d
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ## WGS 84 to WGS84 + EGM 2008 orthometric height

    - WGS 84 (EPSG:4979)
    - WGS 84 (EPSG:4326) + EGM2008 orthometric height (EPSG:3855) => (EPSG:9518)
    """
    )
    return


@app.cell
def _(
    CRS,
    Transformer,
    print_srs,
    wgs84,
    wgs84_3d,
    wgs84_egm2008_9518,
    world_mercator_3d,
):
    # 2D Transformation
    null_transform_2d = Transformer.from_crs(
        wgs84, wgs84, always_xy=True
    )
    print(
        f"2D transform of point {(8.37909, 47.01987, 1000)} from {print_srs(wgs84)} to {print_srs(wgs84)} gives:"
    )
    print(null_transform_2d.transform(8.37909, 47.01987, 1000))

    # 3D Transformations
    null_transform_3d = Transformer.from_crs(
        CRS(4979), wgs84_3d, always_xy=True
    )
    print(
        f"3D transform of point {(8.37909, 47.01987, 1000)} from {print_srs(wgs84_3d)} to {print_srs(world_mercator_3d)} gives:"
    )
    print(
        null_transform_3d.transform(
            8.37909, 47.01987, 1000
        )
    )

    transformer_ellips_to_egm2008_ortho = Transformer.from_crs(
        wgs84_3d, wgs84_egm2008_9518, always_xy=True
    )
    print(
        f"3D transform of point {(8.37909, 47.01987, 1000)} from {print_srs(wgs84_3d)} to {print_srs(wgs84_egm2008_9518)} gives:"
    )
    print(
        transformer_ellips_to_egm2008_ortho.transform(
            8.37909, 47.01987, 1000
        )
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## WGS 84 to World Mercator + EGM 2008 orthometric height

    - WGS 84 (EPSG:4979)
    - World Mercator (EPSG:3395) + EGM2008 orthometric height (EPSG:3855) => (EPSG:6893)
    """
    )
    return


@app.cell
def _(
    Transformer,
    print_srs,
    wgs84,
    wgs84_3d,
    world_mercator_3395,
    world_mercator_3d,
    world_mercator_egm2008_6893,
):
    # 2D Transformation
    transformer2d_wgs84_to_world_mercator = Transformer.from_crs(
        wgs84, world_mercator_3395, always_xy=True
    )
    print(
        f"2D transform of point {(8.37909, 47.01987, 1000)} from {print_srs(wgs84)} to {print_srs(world_mercator_3395)} gives:"
    )
    print(transformer2d_wgs84_to_world_mercator.transform(8.37909, 47.01987, 1000))

    # 3D Transformations
    transformer3d_wgs84_to_world_mercator_ellips = Transformer.from_crs(
        wgs84_3d, world_mercator_3d, always_xy=True
    )
    print(
        f"3D transform of point {(8.37909, 47.01987, 1000)} from {print_srs(wgs84_3d)} to {print_srs(world_mercator_3d)} gives:"
    )
    print(
        transformer3d_wgs84_to_world_mercator_ellips.transform(
            8.37909, 47.01987, 1000
        )
    )

    transformer3d_wgs84_to_world_mercator_egm2008 = Transformer.from_crs(
        wgs84_3d, world_mercator_egm2008_6893, always_xy=True
    )
    print(
        f"3D transform of point {(8.37909, 47.01987, 1000)} from {print_srs(wgs84_3d)} to {print_srs(world_mercator_egm2008_6893)} gives:"
    )
    print(
        transformer3d_wgs84_to_world_mercator_egm2008.transform(
            8.37909, 47.01987, 1000
        )
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## WGS 84 to Swiss national grid

    - WGS 84 (EPSG:4979)
    - Swiss national grid projected SRS: CH1903+ / LV95 (EPSG:2056) + LHN95 height (EPSG:5729)

    """
    )
    return


@app.cell
def _(
    Transformer,
    print_srs,
    swiss_2056,
    swiss_3d,
    swiss_compound,
    swiss_lhn95_height,
    wgs84,
    wgs84_3d,
):
    # https://pyproj4.github.io/pyproj/stable/advanced_examples.html#promote-crs-to-3d
    # 2D Transformation
    transformer2d_wgs84_to_swiss = Transformer.from_crs(wgs84, swiss_2056, always_xy=True)
    print(
        f"2D transform of point {(8.37909, 47.01987, 1000)} from {print_srs(wgs84)} to {print_srs(swiss_2056)} gives:"
    )
    print(transformer2d_wgs84_to_swiss.transform(8.37909, 47.01987, 1000))

    # 3D Transformation
    transformer3d_wgs84_to_swiss_ellips = Transformer.from_crs(
        wgs84_3d,
        swiss_3d,
        always_xy=True,
    )
    print(
        f"3D transform of point {(8.37909, 47.01987, 1000)} from {print_srs(wgs84_3d)} to {print_srs(swiss_3d)} gives:"
    )
    print(transformer3d_wgs84_to_swiss_ellips.transform(8.37909, 47.01987, 1000))
    transformer3d_wgs84_to_swiss_ortho = Transformer.from_crs(
        wgs84_3d,
        swiss_compound,
        always_xy=True,
    )
    print(
        f"3D transform of point {(8.37909, 47.01987, 1000)} from {print_srs(wgs84_3d)} to {print_srs(swiss_compound)} gives:"
    )
    print(transformer3d_wgs84_to_swiss_ortho.transform(8.37909, 47.01987, 1000))

    # wgs84_3d
    # swiss_2056
    swiss_lhn95_height
    # swiss_3d
    # swiss_compound
    return


@app.cell
def _(CRS):
    def print_srs(srs: CRS) -> str:
        axes = [axis.name for axis in srs.axis_info]
        return f"{srs.name} {axes}"
    return (print_srs,)


@app.cell
def _(mo):
    mo.md(
        r"""
    from https://bertt.wordpress.com/2023/08/24/vertical-coordinate-reprojection-from-geoid-to-ellipsoid/

    When doing surveys in the field, it’s critical to know the correct vertical elevation. But the earth has the shape of a lumpy potato, so it’s not easy to calculate the vertical elevation.

    Traditionally the vertical elevation is calculated relative to a local system: the geoid. For the Netherlands the geoid ‘NAP height’ (https://www.rijkswaterstaat.nl/zakelijk/open-data/normaal-amsterdams-peil) is used – https://spatialreference.org/ref/epsg/5709/. The elevation is between minus 6.78 meter (Nieuwerkerk aan den IJssel) and 322.38 meter (Vaals).

    For example the Dam square in Amsterdam has about 2.6 meter elevation:
    """
    )
    return


if __name__ == "__main__":
    app.run()
