// import {
//   interpolateYlGnBu,
//   interpolateCividis,
// } from "https://cdn.jsdelivr.net/npm/d3-scale-chromatic@3/+esm";
import {
  scaleOrdinal,
  scaleSequential,
} from "https://cdn.jsdelivr.net/npm/d3-scale/+esm";

// Your access token can be found at: https://ion.cesium.com/tokens.
// Replace `your_access_token` with your Cesium ion access token.
Cesium.Ion.defaultAccessToken =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI2ZTc4NGUwYi1hMGQ1LTQ0YmEtYThhMi03ZDFkYjhhYzY0ZGEiLCJpZCI6Mjc0NDQ3LCJpYXQiOjE3NjIyNTAwMDJ9._znSCj5J_BQcLnzZL1DGHw7E1cOqzZYENzl437ZY_5A";

// Initialize the Cesium Viewer in the HTML element with the `map` ID.
const mapElementId = "map";
const viewer = new Cesium.Viewer(mapElementId, {
  terrain: Cesium.Terrain.fromWorldTerrain(), // https://cesium.com/platform/cesium-ion/content/#cesium-world-terrain
  animation: false,
  timeline: false,
  fullscreenButton: false,
  vrButton: false,
  sceneModePicker: false,
  baseLayerPicker: false,
  navigationHelpButton: false,
  geocoder: false,
  homeButton: false,
});

const terrainProvider = await Cesium.CesiumTerrainProvider.fromUrl(
  "https://api.pdok.nl/kadaster/3d-basisvoorziening/ogc/v1_0/collections/digitaalterreinmodel/quantized-mesh"
);
viewer.scene.terrainProvider = terrainProvider;

const soilColors = {
  Anthropogenic: "#c7c7c7",
  "Organic soils / Very soft clay": "#9d4e40",
  "Clays: silty clay to clay": "#009200",
  "Silt mixtures: clayey silt to silty clay": "#c2cf5c",
  "Sands: clean sand to silty sand": "#ffff00",
  "Sand mixtures: silty sand to sandy silt": "#f3e006",
  "Gravelly sand to dense sand": "#e7c315",
  Unknown: "#909090",
};

const soilTypeColorScale = scaleOrdinal()
  .domain(Object.keys(soilColors))
  .range(Object.values(soilColors))
  .unknown("#999999");

// https://cesium.com/blog/2020/06/16/visualizing-underground/
const initAlpha = 0.8;

const { globe } = viewer.scene;

// Configure globe for underground visualization
globe.translucency.enabled = true;
globe.translucency.frontFaceAlphaByDistance = new Cesium.NearFarScalar(
  200, // The lower bound of the camera range.
  0.1, // Minimum alpha at close distance
  800, // The upper bound of the camera range.
  initAlpha //  Maximum alpha at far distance
);
globe.translucency.backFaceAlpha = 1.0; // Keep back face opaque
globe.undergroundColor = Cesium.Color.GREY;
// Set the camera to look at out data in Amsterdam Noord
viewer.camera.setView({
  destination: Cesium.Cartesian3.fromDegrees(
    4.90367686119672,
    52.38548804691893,
    1325
  ),
  orientation: {
    heading: 0.0319,
    // pitch: -0.05,
    roll: 6.28318,
  },
});
// So we can move the camera below the surface
viewer.scene.screenSpaceCameraController.enableCollisionDetection = false;

const imageryProvider = new Cesium.UrlTemplateImageryProvider({
  url: "https://tiles.stadiamaps.com/tiles/stamen_terrain/{z}/{x}/{y}.png",
  // url: "https://tiles.stadiamaps.com/tiles/stamen_toner_lite/{z}/{x}/{y}.png",
  maximumLevel: 18,
  credit:
    '&copy; <a href="https://stadiamaps.com/" target="_blank">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a>',
});
const imageryLayer = viewer.imageryLayers.addImageryProvider(imageryProvider);

function onLoadLocations(dataSource) {
  console.log("Loaded location data", dataSource.entities.values.length);

  for (const entity of dataSource.entities.values) {
    const standardType = entity.properties.standard.getValue();
    const cptId = entity.properties.location_source_id.getValue();

    const coordinates =
      entity.polyline && entity.polyline.positions
        ? entity.polyline.positions.getValue()
        : null;

    // Remove the default polyline rendering
    if (entity.polyline) {
      entity.polyline = undefined;
    }

    // Remove the default point rendering
    if (entity.marker) {
      entity.marker = undefined;
    }

    if (!coordinates || coordinates.length < 2) {
      console.warn(`No valid coordinates for CPT ${cptId}`);
      continue;
    }

    const { length, position } = linestringToCylinder(coordinates);

    const color = Cesium.Color.fromCssColorString(
      cptStandardColorScale(standardType)
    );

    dataSource.entities.add({
      position,
      cylinder: {
        topRadius: 2.5,
        bottomRadius: 2.5,
        length: length,
        material: color.withAlpha(0.8),
        fill: true,
        outline: true,
        outlineColor: color,
        outlineWidth: 2,
      },
      properties: entity.properties,
      name: cptId,
    });
  }
}

function linestringToCylinder(coordinates) {
  const [top, bottom] = coordinates;
  const topCartographic = Cesium.Cartographic.fromCartesian(top);
  const bottomCartographic = Cesium.Cartographic.fromCartesian(bottom);

  const lon = topCartographic.longitude * Cesium.Math.DEGREES_PER_RADIAN;
  const lat = topCartographic.latitude * Cesium.Math.DEGREES_PER_RADIAN;
  const topElevation = topCartographic.height;
  const bottomElevation = bottomCartographic.height;

  const length = Math.abs(topElevation - bottomElevation);
  const centerElevation = (topElevation + bottomElevation) / 2;

  const position = Cesium.Cartesian3.fromDegrees(lon, lat, centerElevation);

  return { length, position };
}

function onLoadInterpretedCPT(dataSource) {
  console.log("Loaded interpreted CPT data", dataSource.entities.values.length);

  for (const entity of dataSource.entities.values) {
    const soilType = entity.properties.soil_type.getValue();
    const locationUid = entity.properties.location_uid.getValue();

    const coordinates =
      entity.polyline && entity.polyline.positions
        ? entity.polyline.positions.getValue()
        : null;

    // Remove the default polyline rendering
    if (entity.polyline) {
      entity.polyline = undefined;
    }

    // Remove the default point rendering
    if (entity.marker) {
      entity.marker = undefined;
    }

    if (!coordinates || coordinates.length < 2) {
      console.warn(`No valid coordinates for layer ${locationUid}`);
      continue;
    }

    const { length, position } = linestringToCylinder(coordinates);

    const color = Cesium.Color.fromCssColorString(soilTypeColorScale(soilType));

    dataSource.entities.add({
      position,
      cylinder: {
        topRadius: 2,
        bottomRadius: 2,
        length,
        material: color.withAlpha(0.9),
        fill: true,
        outline: false,
      },
      properties: entity.properties,
      name: `${locationUid} - ${soilType}`,
    });
  }
}

// https://observablehq.com/@d3/d3-scaleordinal
const cptStandardColorScale = scaleOrdinal()
  .domain(["ISO22476D1", "NEN5140"])
  .range(["#DC143C", "#0000CD"])
  .unknown("#999999");

const datasets = [
  {
    id: "cpt",
    label: "CPT Locations",
    enabled: false,
    dataSource: null,
    legendElement: createOrdinalLegend({
      scale: cptStandardColorScale,
      title: "CPT Standards",
    }),
    onLoad: onLoadLocations,
  },
  {
    id: "cpt_interpreted",
    label: "CPT Interpreted",
    enabled: true,
    dataSource: null,
    legendElement: createOrdinalLegend({
      scale: soilTypeColorScale,
      title: "Soil Types",
    }),
    onLoad: onLoadInterpretedCPT,
  },
];

function loadDataset(dataset) {
  return Cesium.GeoJsonDataSource.load(`${dataset.id}.geojson`, {
    clampToGround: false,
    stroke: Cesium.Color.YELLOW,
    strokeWidth: 3,
  })
    .then((dataSource) => {
      // Store reference to the loaded data source for later access (visibility toggling, styling)
      dataset.dataSource = dataSource;

      dataset.onLoad(dataSource);

      dataSource.show = dataset.enabled;

      viewer.dataSources.add(dataSource);

      return dataSource;
    })
    .catch((error) => {
      console.error(`Error loading ${dataset.id}.geojson:`, error);
    });
}

function updateLegendDisplay() {
  for (const dataset of datasets) {
    if (dataset.legendElement) {
      dataset.legendElement.style.display = dataset.enabled ? "block" : "none";
    }
  }
}

function generateDatasetControls() {
  const controlsSection = document.getElementById("datasets");

  const controlsHTML = datasets
    .map(
      (dataset) => `
  <div class="checkbox-item">
    <input type="checkbox" id="${dataset.id}-toggle" ${
        dataset.enabled ? "checked" : ""
      }>
    <label for="${dataset.id}-toggle">${dataset.label}</label>
  </div>
`
    )
    .join("");

  controlsSection.innerHTML = controlsSection.innerHTML + controlsHTML;

  // Add event listeners to checkboxes
  for (const dataset of datasets) {
    const checkbox = document.getElementById(`${dataset.id}-toggle`);
    checkbox.addEventListener("change", (event) => {
      dataset.enabled = event.target.checked;
      if (dataset.dataSource) {
        dataset.dataSource.show = dataset.enabled;
      }
      updateLegendDisplay();
    });
  }
}

generateDatasetControls();

// Add legend elements to DOM and set initial visibility
const legendEl = document.querySelector("#legend");
for (const dataset of datasets) {
  if (dataset.legendElement) {
    dataset.legendElement.style.display = dataset.enabled ? "block" : "none";
    legendEl.appendChild(dataset.legendElement);
  }
}

// Load all datasets
Promise.allSettled(datasets.map((dataset) => loadDataset(dataset))).then(
  (results) => {
    for (const result of results) {
      if (result.status === "rejected") {
        console.warn("Failed to load dataset:", result.reason);
      }
    }
  }
);

// Globe opacity slider
document.querySelector("#alpha")?.addEventListener("input", (event) => {
  const alpha = event.target.valueAsNumber;

  // Update translucency using distance-based approach
  globe.translucency.frontFaceAlphaByDistance.nearValue = alpha;
  globe.translucency.frontFaceAlphaByDistance.farValue = alpha;
  // imageryLayer.alpha = alpha;
});

export function createOrdinalLegend({ scale, title, config = null }) {
  const container = document.createElement("section");
  container.classList.add("legend-section");

  const titleEl = document.createElement("h4");
  titleEl.textContent = title;
  container.appendChild(titleEl);

  const itemsDiv = document.createElement("div");
  scale.domain().forEach((value) => {
    const item = document.createElement("div");
    item.className = "legend-item";

    // Use full name from config if available, otherwise use the value
    const displayName = config?.[value] ? config[value] : value;

    item.innerHTML = `
      <div class="legend-circle" style="background-color: ${scale(
        value
      )}"></div>
      <span>${displayName}</span>
    `;
    itemsDiv.appendChild(item);
  });

  container.appendChild(itemsDiv);
  return container;
}

const lithoColorShader = new Cesium.CustomShader({
  fragmentShaderText: `
      void fragmentMain(FragmentInput fsInput, inout czm_modelMaterial material) {
        float litho = fsInput.metadata.lithok;

        vec3 color;
        float alpha;

        // Render nodata voxels as fully transparent
        // IMPORTANT: Must set diffuse to black to prevent gray artifacts
        if (litho < -1000.0) {
          material.diffuse = vec3(0.0, 0.0, 0.0);  // Black (prevents gray showing through)
          material.alpha = 0.0;  // Fully transparent - ray continues through
          return;
        }

        // Official GeoTOP color scheme (RGB values converted to 0-1 range)
        if (litho < 0.5) {
          color = vec3(0.784, 0.784, 0.784);  // 0: antropogeen (anthropogenic) - light grey
        } else if (litho < 1.5) {
          color = vec3(0.616, 0.306, 0.251);  // 1: veen (peat/organic) - brown
        } else if (litho < 2.5) {
          color = vec3(0.0, 0.573, 0.0);      // 2: klei (clay) - green
        } else if (litho < 3.5) {
          color = vec3(0.761, 0.812, 0.361);  // 3: kleiig zand (sandy clay) - yellow-green
        } else if (litho < 5.5) {
          color = vec3(1.0, 1.0, 0.0);        // 5: zand fijn (fine sand) - bright yellow
        } else if (litho < 6.5) {
          color = vec3(0.953, 0.882, 0.024);  // 6: zand midden (medium sand) - yellow-orange
        } else if (litho < 7.5) {
          color = vec3(0.906, 0.765, 0.086);  // 7: zand grof (coarse sand) - orange-yellow
        } else {
          color = vec3(0.565, 0.565, 0.565);  // 10: overig (other) - grey
        }

        material.diffuse = color;
        // CRITICAL: Alpha must be < 1.0 for volumetric rendering
        // Lower alpha = more transparent = can see through sparse layers
        material.alpha = 0.8;
      }
    `,
});

viewer.extend(Cesium.viewerVoxelInspectorMixin);

const voxelProvider = await Cesium.Cesium3DTilesVoxelProvider.fromUrl(
  `geotop_amsterdam/tileset.json`
);

const voxelPrimitive = viewer.scene.primitives.add(
  new Cesium.VoxelPrimitive({
    provider: voxelProvider,
    customShader: lithoColorShader,
  })
);

voxelPrimitive.nearestSampling = true;
voxelPrimitive.jitter = false;

// // Force proper depth testing and disable face culling
// voxelPrimitive.depthTest = true;
// voxelPrimitive.blendOption = Cesium.BlendOption.TRANSLUCENT;

viewer.voxelInspector.viewModel.voxelPrimitive = voxelPrimitive;

document.querySelector("#geotop-toggle").addEventListener("change", (event) => {
  voxelPrimitive.show = event.target.checked;
});

try {
  const tileset_3dbag = await Cesium.Cesium3DTileset.fromUrl(
    "https://data.3dbag.nl/v20250903/cesium3dtiles/lod22/tileset.json"
  );
  viewer.scene.primitives.add(tileset_3dbag);

  // 3D buildings toggle
  document
    .querySelector("#buildings-toggle")
    .addEventListener("change", (event) => {
      tileset_3dbag.show = event.target.checked;
    });

  // 3D basisvoorziening terreinen
  // const tileset_3dbgt = await Cesium.Cesium3DTileset.fromUrl(
  //   "https://api.pdok.nl/kadaster/3d-basisvoorziening/ogc/v1_0/collections/terreinen/3dtiles"
  // );
  // viewer.scene.primitives.add(tileset_3dbgt);
} catch (error) {
  // Handle errors
  console.log(`There was an error while creating the 3D tileset. ${error}`);
}
