# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "anthropic==0.72.0",
#     "anymap==0.7.0",
#     "bedrock-ge==0.3.2",
#     "bromodels==0.0.1",
#     "dask==2025.10.0",
#     "folium==0.20.0",
#     "geojson==3.2.0",
#     "geopandas==1.1.1",
#     "groundhog==0.15.0",
#     "mapclassify==2.8.1",
#     "mapwidget==0.2.0",
#     "marimo",
#     "matplotlib==3.10.7",
#     "numpy==2.3.4",
#     "pandas==2.3.3",
#     "plotly==6.3.1",
#     "polars==1.34.0",
#     "pyarrow==21.0.0",
#     "pygef==0.13.0",
#     "pyobsplot==0.5.4",
#     "pyproj==3.7.2",
#     "pyvista==0.46.3",
#     "shapely==2.1.2",
#     "xarray==2025.10.1",
# ]
# ///

import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(r"""
    locations_dfHow to access BRO data: [Handreiking Afname BRO Gegevens](https://www.bro-productomgeving.nl/bpo/latest/handreiking-afname-bro-gegevens)

    1. [BROloket](https://www.broloket.nl/ondergrondgegevens)
    2. BRO APIs
      1. SOAP - impractical, because requires a digital "PKI" certificate.
      2. [REST](https://www.bro-productomgeving.nl/bpo/latest/url-s-publieke-rest-services)
        1. CPT: <https://publiek.broservices.nl/sr/cpt/v1>
        2. Geotechnical boreholes: <https://publiek.broservices.nl/sr/bhrgt/v2>
    3. [PDOK](https://app.pdok.nl/viewer) - WMS
    """)
    return


@app.cell
def _():
    project_uid = "amsterdam_noord"
    project_uid
    return (project_uid,)


@app.cell
def _(mo):
    cwd = mo.notebook_location()
    return (cwd,)


@app.cell
def _(cwd, gpd):
    site_plot = gpd.read_file(cwd / "context.gpkg")
    return (site_plot,)


@app.cell
def _(mo):
    mo.md(r"""
    ## GeoTOP
    """)
    return


@app.cell
def _(site_plot):
    bbox = site_plot.total_bounds
    west, south, east, north = bbox
    buffer = 1000
    west = west - buffer
    south = south - buffer
    east = east + buffer
    north = north + buffer
    (west, south, east, north)
    return


@app.cell
def _():
    # ds = bromodels.GeoTopDomain(
    #     west=west, south=south, east=east, north=north, bottom=-60
    # )
    return


@app.cell
def _():
    # slider = mo.ui.slider(1, ds.dims["z"]-1)
    # slider
    return


@app.cell
def _():
    # ds["strat"].isel(z=slider.value).plot() #cmap=ListedColormap(colormap))
    return


@app.cell
def _():
    # ds["lithok"].isel(x=1).plot() #cmap=ListedColormap(colormap))
    return


@app.cell
def _():
    # _link = {
    #     "lithok": (bromodels.GeoTop.geotop_lithology_class(), "LITHO_CLASS_CD"),
    #     "strat": (bromodels.GeoTop.geotop_stratigraphic_unit(), "STR_UNIT_CD"),
    # }

    # mz, mx, my = np.meshgrid(ds.z.values, ds.x.values, ds.y.values, indexing="ij")
    # point_cloud = list(zip(mx.flatten(), my.flatten(), mz.flatten() + 0.25))

    # # create pyvista object
    # var = "lithok"  # lithok/ strat

    # # color
    # df_pv, CD = _link[var]
    # colormap = []
    # label = []
    # for i, row in df_pv.loc[df_pv["VOXEL_NR"].isin(ds[var].values.flatten())].iterrows():
    #     colormap.append(
    #         np.array([row.RED_DEC / 255, row.GREEN_DEC / 255, row.BLUE_DEC / 255])
    #     )
    #     label.append(row[CD])
    return


@app.cell
def _():
    # ListedColormap(colormap)
    return


@app.cell
def _():
    # pdata = pyvista.PolyData(point_cloud)

    # create many cubes from the point cloud
    # cube = pyvista.Cube(x_length=100, y_length=100, z_length=0.5)

    # pdata[var] = ds[var].values.flatten()
    # pc = pdata.glyph(scale=False, geom=cube, orient=False)
    # p = pyvista.Plotter()
    # p.add_mesh(pc, scalars=var, cmap=ListedColormap(colormap), show_edges=False)
    # p.set_scale(zscale=20)
    # p.show_grid()
    # p.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## CPT
    """)
    return


@app.cell
def _(points):

    from anymap import MapLibreMap

    amsterdam_noord = [4.90367686119672, 52.38548804691893]

    def handle_click(event):
        lat, lng = event['lngLat']
        print(f"Clicked at: {lat:.4f}, {lng:.4f}")

    def handle_point_click(event):
        feature = event.get("features", [None])[0]
        if feature:
            props = feature["properties"]
            coords = feature["geometry"]["coordinates"]
            print(f"Clicked on: {props.get('name')} at {coords}")
        else:
            print("No feature clicked")


    m = MapLibreMap(
        center=amsterdam_noord,  
        zoom=14,
        height="400px",
    )

    m.add_geojson_layer(
        layer_id="cpt",
        geojson_data=points,
        layer_type="circle",
        paint={
            "circle-radius": 2,
            "circle-color": "#fff"
        }
    )

    m.enable_feature_popup("cpt", fields=["bro_id"], title_field="id")

    m
    return


@app.cell(hide_code=True)
def _():
    import geojson

    def make_cpt_point(cpt_hmm):
        coords = [cpt_hmm.standardized_location.y, cpt_hmm.standardized_location.x]

        props = {
            "bro_id": cpt_hmm.bro_id,
            "standard": cpt_hmm.cpt_standard,
            "description": cpt_hmm.cpt_description,
            "type": cpt_hmm.cpt_type
        }

        point_feature = geojson.Feature(
            geometry=geojson.Point(coords),
            properties=props
        )

        return point_feature
    return (make_cpt_point,)


@app.cell(hide_code=True)
def _(cpts, make_cpt_point):
    # TODO just use geopandas
    points =  {
        "type": "FeatureCollection",
        "features": [make_cpt_point(cpt) for cpt in cpts]
    }
    return (points,)


@app.cell
def _(cwd):
    cpt_folder = cwd / "data" 
    return (cpt_folder,)


@app.cell
def _(cpt_folder):
    xml_files = list(cpt_folder.rglob("*xml"))
    f"{len(xml_files)} XML files in {cpt_folder}"
    return (xml_files,)


@app.cell
def _(CRS, cpts):
    srs = { cpt.delivered_location.srs_name for cpt in cpts }.pop()
    projected_crs = CRS(srs)
    return (projected_crs,)


@app.cell
def _(projected_crs):
    projected_crs
    return


@app.cell
def _(cpts):
    cpts[0].delivered_vertical_position_datum
    return


@app.cell
def _(CRS):
    vertical_crs = CRS("EPSG:5709")
    return (vertical_crs,)


@app.cell
def _(
    CompoundCRS,
    Transformer,
    cesium_crs,
    network,
    projected_crs,
    vertical_crs,
):
    compound_crs = CompoundCRS(
        name=f"{projected_crs.name} + {vertical_crs.name}",
        components=[projected_crs, vertical_crs],
    )

    # Use always_xy=True to get (lon, lat) order instead of (lat, lon)
    # This matches GeoJSON standard and traditional GIS coordinate order
    transformer_compound = Transformer.from_crs(compound_crs, cesium_crs, always_xy=True)
    # This is crucial for proper height transformation! See https://proj.org/en/stable/usage/network.html
    network.set_network_enabled(active=True)
    return compound_crs, transformer_compound


@app.cell
def _(read_cpt, xml_files):
    cpts = [read_cpt(file) for file in xml_files]
    return (cpts,)


@app.cell
def _(pd, project_uid, projected_crs, vertical_crs):
    project = pd.DataFrame({
        "project_uid": [project_uid], # primary key
        "horizontal_crs_wkt": projected_crs.to_wkt(),
        "vertical_crs_wkt": vertical_crs.to_wkt(),
    })
    return (project,)


@app.cell
def _():
    standards_colors = {
        "ISO22476D1":"#DC143C",
        "NEN5140": "#0000CD" 
    }
    return


@app.cell
def _(errors):
    len(errors)
    return


@app.cell
def _(errors):
    import traceback
    if errors:
      for i, e in enumerate(errors[:5]):  # First 5 errors
          print(f"\n--- Error {i+1} ---")
          print(f"Type: {type(e).__name__}")
          print(f"Message: {str(e)}")
          print(f"Traceback:")
          traceback.print_exception(type(e), e, e.__traceback__)
    return


@app.cell
def _(errors):
    errors
    return


@app.cell
def _(add_interpretation, cpts, merge_layers, pl, project_uid, ç):
    layers = []
    errors = []
    soil_columns = []
    for cpt in cpts:
        # standardized_location
        try:
            # merge_layers expects and returns pandas DataFrame
            merged_pandas = merge_layers(add_interpretation(cpt.data, cpt.cpt_standard))
            # Convert to polars for column operations
            interpreted = pl.from_pandas(merged_pandas)
            df = interpreted.with_columns([
                pl.lit(f"{cpt.bro_id} {project_uid}").alias("location_uid"),
                pl.lit(project_uid).alias("project_uid")
            ])
            ç
            layers.append(df)
            soil_columns.append(interpreted)
        except Exception as e:
            errors.append(e)
            soil_columns.append(None)
            print(f"Error processing CPT: {e}")
            continue

    insitu = pl.concat(layers).to_pandas()
    return errors, insitu


@app.cell
def _(insitu):
    insitu
    return


@app.function
def rgb_to_hex(rgb):
    # multiply each component by 255 and convert to int
    r, g, b = (int(x * 255) for x in rgb)
    return f"#{r:02x}{g:02x}{b:02x}"


@app.cell
def _():
    geotop_rgb_colors = {
      "Anthropogenic": (0.784, 0.784, 0.784), # 0: antropogeen (anthropogenic) - light grey
      "Organic soils / Very soft clay": (0.616, 0.306, 0.251), # 1: veen (peat/organic) - brown
      "Clays: silty clay to clay": (0.0, 0.573, 0.0), # 2: klei (clay) - green
      "Silt mixtures: clayey silt to silty clay": (0.761, 0.812, 0.361), # 3: kleiig zand (sandy clay) - yellow-green
      "Sands: clean sand to silty sand": (1.0, 1.0, 0.0), # 5: zand fijn (fine sand) - bright yellow
      "Sand mixtures: silty sand to sandy silt": (0.953, 0.882, 0.024), # 6: zand midden (medium sand) - yellow-orange
      "Gravelly sand to dense sand": (0.906, 0.765, 0.086), # 7: zand grof (coarse sand) - orange-yellow
      "Unknown": (0.565, 0.565, 0.565), # 10: overig (other) - grey
    };

    soil_colors = {k: rgb_to_hex(v) for k, v in geotop_rgb_colors.items()}
    soil_colors
    return (soil_colors,)


@app.cell
def _(cpts):
    locations = [[cpt.delivered_location.x,cpt.delivered_location.y] for cpt in cpts]
    len(locations)
    return


@app.cell
def _(plt, soil_colors):
    # soil_colors = {
    #     'Unknown': '#FFFFFF',  # White
    #     'Gravelly sand to dense sand': '#FF8C00',  # Dark orange
    #     'Sands: clean sand to silty sand': '#FFD700',  # Gold
    #     'Sand mixtures: silty sand to sandy silt': '#F4E4A6',  # Pale yellow
    #     'Silt mixtures: clayey silt to silty clay': '#90EE90',  # Light green
    #     'Clays: silty clay to clay': '#8B4513',  # Saddle brown
    #     'Organic soils / Very soft clay': '#2F4F2F',  # Dark olive green

    #     # Legacy names
    #     'Clay': '#8B4513',
    #     'Silt': '#90EE90', 
    #     'Silty sand': '#F4E4A6',
    #     'Sand': '#FFD700',
    #     'Dense sand': '#FF8C00'
    # }

    def plot_column(df):
        fig, ax = plt.subplots(figsize=(2, 8))


        colors = [soil_colors.get(st, 'gray') for st in df['soil_type']]

        # Plot as horizontal bars
        ax.barh(
          df['depth_to_top'],
          1,
          height=df['Thickness [m]'],
          color=colors,
          edgecolor='black',
          linewidth=0.5
        )

        ax.set_ylabel('Depth [m]')
        ax.set_xlim(0, 1)
        ax.set_xticks([])
        ax.invert_yaxis()
        ax.set_ylim(df['depth_to_top'].max() + df['Thickness [m]'].iloc[-1], 0)
        ax.set_title('Soil Profile')

        return fig
    return


@app.cell
def _(cpts, mo):
    options = {d.bro_id: i for i, d in enumerate(cpts)}
    dropdown = mo.ui.dropdown(options, label="Select CPT")
    dropdown
    return (dropdown,)


@app.cell
def _(dropdown):
    cpt_index = dropdown.value or 0
    cpt_index
    return (cpt_index,)


@app.cell
def _():
    # plot_column(soil_columns[cpt_index])
    return


@app.cell
def _():
    return


@app.cell
def _(PCPTProcessing, classify_soil, np, pl, soil_colors):
    def add_interpretation(cpt_df, standard):
        # Check if required columns exist
        required_cols = ["frictionRatio", "depthOffset", "coneResistance", "localFriction"]
        missing_cols = [col for col in required_cols if col not in cpt_df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")

        u_2 = np.zeros_like(cpt_df["frictionRatio"])
        cpt_pd = cpt_df.with_columns(porePressure=u_2).with_columns((pl.col('frictionRatio')).alias('Rf [%]') ).to_pandas()

        cpt = PCPTProcessing("ams", waterunitweight=10)
        cpt.load_pandas(cpt_pd, z_key="depthOffset", qc_key="coneResistance", fs_key="localFriction", u2_key="porePressure", add_zero_row=False)

        # Filter out zero values
        cpt.data = cpt.data[cpt.data['qc [MPa]'] != 0]

        # Check if we have data left after filtering
        if len(cpt.data) == 0:
            raise ValueError("No data remaining after filtering zero values")

        cpt.apply_correlation(name="Isbt Robertson (2010)", outputs={'Isbt [-]': 'Ic [-]'})
        cpt.data['soil_type'] = cpt.data['Ic [-]'].apply(classify_soil)
        cpt.data['color'] = cpt.data['soil_type'].map(soil_colors)

        result = cpt.data.loc[:, ~cpt.data.columns.duplicated()]
    
        return result
    return (add_interpretation,)


@app.cell
def merge_layers(pd):
    def merge_layers(interpreted_df):
        # Ensure we're working with a pandas DataFrame
        if not isinstance(interpreted_df, pd.DataFrame):
            interpreted_df = interpreted_df.to_pandas()


        if 'soil_type' not in interpreted_df.columns:
            raise ValueError("Missing 'soil_type' column in interpreted DataFrame")

        print(f"DataFrame shape: {interpreted_df.shape}")
        print(f"Columns: {interpreted_df.columns.tolist()}")
        print(f"soil_type dtype: {interpreted_df['soil_type'].dtype}")
        print(f"Unique soil types: {interpreted_df['soil_type'].unique()}")
        
        # Identify consecutive groups of the same soil type
        interpreted_df['soil_group'] = (
            interpreted_df['soil_type'] != interpreted_df['soil_type'].shift()
        ).cumsum()

        # Define aggregations based on available columns
        agg_dict = {'z [m]': ['min', 'max']}

        # Add optional columns if they exist
        if 'qc [MPa]' in interpreted_df.columns:
            agg_dict['qc [MPa]'] = ['mean']
        if 'fs [kPa]' in interpreted_df.columns:
            agg_dict['fs [kPa]'] = ['mean']
        if 'Rf [%]' in interpreted_df.columns:
            agg_dict['Rf [%]'] = ['mean']
        if 'Ic [-]' in interpreted_df.columns:
            agg_dict['Ic [-]'] = ['mean']

        # Merge rows by soil group
        merged_layers = (
            interpreted_df.groupby(['soil_group', 'soil_type'])
            .agg(agg_dict)
            .reset_index()
        )

        # Flatten column names - handle both tuples and strings
        new_columns = []
        for col in merged_layers.columns:
            if isinstance(col, tuple):
                # Join tuple elements, e.g., ('qc [MPa]', 'mean') -> 'qc [MPa]_mean'
                new_columns.append('_'.join(str(c) for c in col).strip('_'))
            else:
                # Keep string columns as-is (e.g., 'soil_group', 'soil_type')
                new_columns.append(col)
        merged_layers.columns = new_columns

        # Rename depth columns
        # Note: if z [m] is elevation (negative = below ground), then:
        # - min = most negative = bottom (deepest)
        # - max = least negative = top (shallowest)
        merged_layers = merged_layers.rename(
            columns={
                'z [m]_min': "depth_to_top",
                'z [m]_max': "depth_to_bottom",
            }
        )

        # Calculate layer thickness (should be positive)
        # Since depth_to_top is less negative and depth_to_bottom is more negative:
        merged_layers['Thickness [m]'] = (
          merged_layers['depth_to_bottom'] - merged_layers['depth_to_top']
        )

        merged_layers = merged_layers[merged_layers['Thickness [m]'] > 0]

        return merged_layers
    return (merge_layers,)


@app.cell
def _(pd):
    def classify_soil(ic):
        if pd.isna(ic):
            return "Unknown"
        elif ic < 1.31:
            return "Gravelly sand to dense sand"
        elif ic < 2.05:
            return "Sands: clean sand to silty sand"
        elif ic < 2.60:
            return "Sand mixtures: silty sand to sandy silt"
        elif ic < 2.95:
            return "Silt mixtures: clayey silt to silty clay"
        elif ic < 3.60:
            return "Clays: silty clay to clay"
        else:
            return "Organic soils / Very soft clay"
    return (classify_soil,)


@app.cell
def _(mo):
    plot_options = {"coneResistance", "frictionRatio", "frictionRatioComputed", "porePressureU2"}
    prop = mo.ui.dropdown(plot_options, label="Select property to plot", value="coneResistance")
    prop
    return (prop,)


@app.cell(hide_code=True)
def _(Plot, cpt_index, cpts, prop):
    Plot.plot(
        {
            "height": 580,
            "width": 300,
            "x": {"label": "Conus [MPa]", "grid": True},
            "y": {"grid": True, "reverse": True, "label": "Depth [m]"},
            "marks": [
                Plot.frame(),
                Plot.lineX(
                    cpts[cpt_index].data,
                    {
                        "x": prop.value,
                        "y": "depth",
                        "style": {"stroke": "blue"},
                    },
                ),
                Plot.lineX(cpts[cpt_index].data, {"x": prop.value, "y": "depth"}),
                Plot.crosshair(
                    cpts[cpt_index].data, {"x": prop.value, "y": "depth"}
                ),
            ],
        }
    )
    return


@app.cell
def _(cpt_index, cpts, plot_cpt):
    plot_cpt(cpts[cpt_index])
    return


@app.cell
def _(cpts, pd, project_uid):
    locations_df = pd.DataFrame([
        {
            "location_uid": f"{cpt.bro_id} {project_uid}", # primary key
            "project_uid": project_uid, # foreign key
            "location_source_id": cpt.bro_id,
            "date": str(cpt.research_report_date),
            "location_type": "CPT",
            "easting": cpt.delivered_location.x,
            "northing": cpt.delivered_location.y,
            "depth_to_base": cpt.final_depth,
            "standard": cpt.cpt_standard,
            # "color": standards_colors[cpt.cpt_standard],
            "ground_level_elevation": cpt.delivered_vertical_position_offset,
            "elevation_at_base": cpt.final_depth,
        }
        for cpt in cpts
    ])
    locations_df
    return (locations_df,)


@app.cell
def _(BedrockGIDatabase, insitu, locations_df, project):
    brgi_db = BedrockGIDatabase(
            Project=project,
            Location=locations_df,
            InSituTests={"interpretation": insitu },
        )
    brgi_db
    return (brgi_db,)


@app.cell
def _(brgi_db, create_brgi_geodb):
    brgi_geodb = create_brgi_geodb(brgi_db)
    brgi_geodb.Location
    return (brgi_geodb,)


@app.cell
def _(brgi_db, check_brgi_geodb):
    check_brgi_geodb(brgi_db)
    return


@app.cell
def _(CRS):
    cesium_crs = CRS("EPSG:4979").to_3d()
    cesium_crs
    return (cesium_crs,)


@app.cell
def _(cesium_crs, gpd, transform_geometry):
    def to_epsg_4979_3d(gdf) -> gpd.GeoDataFrame: 
        result = gdf.copy()
        result.geometry = gdf.geometry.apply(transform_geometry)
        result.crs = cesium_crs
        return result
    return (to_epsg_4979_3d,)


@app.cell
def _(LineString, Point, transformer_compound):
    def transform_geometry(geom):
        if geom is None:
            return None

        if geom.geom_type == 'Point':
            if geom.has_z:
                # With always_xy=True, transformer returns (lon, lat, height)
                lon, lat, z = transformer_compound.transform(geom.x, geom.y, geom.z)
                return Point(lon, lat, z)
            else:
                lon, lat = transformer_compound.transform(geom.x, geom.y)
                return Point(lon, lat)

        elif geom.geom_type == 'LineString':
            coords = list(geom.coords)
            if len(coords[0]) == 3:  # Has Z
                x_list, y_list, z_list = zip(*coords)
                # With always_xy=True, transformer returns (lon, lat, height)
                lon_new, lat_new, z_new = transformer_compound.transform(x_list, y_list, z_list)
                return LineString(list(zip(lon_new, lat_new, z_new)))
            else:  # 2D
                x_list, y_list = zip(*coords)
                lon_new, lat_new = transformer_compound.transform(x_list, y_list)
                return LineString(list(zip(lon_new, lat_new)))
        else:
            raise ValueError(f"Unsupported geometry type: {geom.geom_type}")
    return (transform_geometry,)


@app.cell
def _():
    columns = ["date", "depth_to_base", "ground_level_elevation", "elevation_at_base", "geometry", "standard", "location_source_id", "color"]
    return (columns,)


@app.cell
def _(brgi_geodb, columns, to_epsg_4979_3d):
    locations_geojson = to_epsg_4979_3d(brgi_geodb.Location[columns]).to_json()

    with open("cpt.geojson", "w") as file:
        file.write(locations_geojson)
    return


@app.cell
def _(brgi_geodb, columns):
    locations_geojson_rd = brgi_geodb.Location[columns].to_json()

    with open("cpt_rd.geojson", "w") as file_rd:
        file_rd.write(locations_geojson_rd)
    return


@app.cell
def _(LineString, brgi_geodb, compound_crs, gpd, insitu, soil_colors):
    locations_with_coords = brgi_geodb.Location[['location_uid', 'geometry', 'ground_level_elevation']].copy()

    locations_with_coords['x'] = locations_with_coords.geometry.apply(lambda geom: geom.coords[0][0])
    locations_with_coords['y'] = locations_with_coords.geometry.apply(lambda geom: geom.coords[0][1])

    insitu_with_coords = insitu.merge(locations_with_coords, on='location_uid')

    def create_layer_geometry(row):
        x, y = row['x'], row['y']
        ground_elev = row['ground_level_elevation']
        top_elev = ground_elev - abs(row['depth_to_top'])
        bottom_elev = ground_elev - abs(row['depth_to_bottom'])
        return LineString([(x, y, top_elev), (x, y, bottom_elev)])

    insitu_with_coords['geometry'] = insitu_with_coords.apply(create_layer_geometry, axis=1)

    insitu_with_coords['color'] = insitu_with_coords['soil_type'].map(soil_colors)

    insitu_gdf = gpd.GeoDataFrame(insitu_with_coords, geometry='geometry', crs=compound_crs)
    return (insitu_gdf,)


@app.cell
def _(insitu_gdf, to_epsg_4979_3d):
    insitu_geojson = to_epsg_4979_3d(insitu_gdf).to_json()

    with open("cpt_interpreted.geojson", "w") as ins_file:
        ins_file.write(insitu_geojson)
    return


@app.cell
def _(insitu_gdf):
    insitu_geojson_rd = insitu_gdf.to_json()

    with open("cpt_interpreted_rd.geojson", "w") as ins_file_rd:
        ins_file_rd.write(insitu_geojson_rd)
    return


@app.cell
def _():
    import xarray as xr
    import dask
    from pyproj import CRS, Transformer, network
    from pyproj.crs.crs import CompoundCRS
    from shapely.geometry import Point, LineString
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
    import pyvista
    import mapwidget
    from groundhog.siteinvestigation.insitutests.pcpt_processing import PCPTProcessing 
    import pandas as pd
    from bedrock_ge.gi.schemas import BedrockGIDatabase
    from bedrock_ge.gi.db_operations import merge_dbs
    from bedrock_ge.gi.geospatial import create_brgi_geodb
    from bedrock_ge.gi.io_utils import geodf_to_df
    from bedrock_ge.gi.validate import check_brgi_geodb
    from bedrock_ge.gi.mapper import map_to_brgi_db
    from bedrock_ge.gi.write import write_brgi_db_to_file
    return (
        BedrockGIDatabase,
        CRS,
        CompoundCRS,
        LineString,
        PCPTProcessing,
        Plot,
        Point,
        Transformer,
        check_brgi_geodb,
        create_brgi_geodb,
        gpd,
        mo,
        network,
        np,
        pd,
        pl,
        plot_cpt,
        plt,
        read_cpt,
    )


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
