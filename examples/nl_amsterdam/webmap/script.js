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

const soil_colors = {
  Unknown: "#FFFFFF",
  "Gravelly sand to dense sand": "#FF8C00",
  "Sands: clean sand to silty sand": "#FFD700",
  "Sand mixtures: silty sand to sandy silt": "#F4E4A6",
  "Silt mixtures: clayey silt to silty clay": "#90EE90",
  "Clays: silty clay to clay": "#8B4513",
  "Organic soils / Very soft clay": "#2F4F2F",
};

// const osmBuildings = await Cesium.createOsmBuildingsAsync();
// viewer.scene.primitives.add(osmBuildings);

// https://cesium.com/blog/2020/06/16/visualizing-underground/
const initAlpha = 0.7;

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

async function onLoadLocations(dataSource) {
  console.log("Loaded location data", dataSource.entities.values.length);

  // Clear existing entities to avoid conflicts
  dataSource.entities.removeAll();

  // Load GeoJSON directly to get proper coordinates
  console.log("Loading GeoJSON directly for cylinder rendering...");
  const response = await fetch("cpt.geojson");
  const geojson = await response.json();

  for (const feature of geojson.features) {
    const { properties, geometry } = feature;

    if (geometry.type !== "LineString" || geometry.coordinates.length < 2) {
      console.warn(`Invalid geometry for ${properties.location_source_id}`);
      continue;
    }

    const [topCoord, bottomCoord] = geometry.coordinates;
    const [lon, lat, topElev] = topCoord;
    const [, , bottomElev] = bottomCoord;

    const length = Math.abs(topElev - bottomElev);
    const centerElevation = (topElev + bottomElev) / 2;

    const color = Cesium.Color.fromCssColorString(
      cptStandardColorScale(properties.standard)
    );

    // Heights should already be ellipsoidal (transformed from NAP in Python)
    dataSource.entities.add({
      position: Cesium.Cartesian3.fromDegrees(lon, lat, centerElevation),
      cylinder: {
        topRadius: 1,
        bottomRadius: 1,
        length: length,
        material: color.withAlpha(0.8),
        fill: true,
        outline: true,
        outlineColor: color,
        outlineWidth: 2,
      },
      properties: properties,
      name: properties.location_source_id,
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
    enabled: true,
    dataSource: null,
    legendElement: createOrdinalLegend({
      scale: cptStandardColorScale,
      title: "CPT Standards",
      // config: agsHoleTypes,
    }),
    onLoad: onLoadLocations,
  },
  // {
  //   id: "cpt_interpretated",
  //   label: "CPT Interpreted",
  //   enabled: false,
  //   dataSource: null,
  //   // legendElement: createOrdinalLegend({
  //   //   scale: holeTypeColorScale,
  //   //   title: "Hole Types",
  //   //   config: agsHoleTypes,
  //   // }),
  //   onLoad: onLoadLocations,
  // },
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
document.querySelector("#alpha").addEventListener("input", (event) => {
  const alpha = event.target.valueAsNumber;

  // Update translucency using distance-based approach
  globe.translucency.frontFaceAlphaByDistance.nearValue = alpha;
  globe.translucency.frontFaceAlphaByDistance.farValue = alpha;
  // imageryLayer.alpha = alpha;
});

// 3D buildings toggle
document
  .querySelector("#buildings-toggle")
  .addEventListener("change", (event) => {
    osmBuildings.show = event.target.checked;
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
