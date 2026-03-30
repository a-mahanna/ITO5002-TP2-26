<template>
  <div class="container mt-2">
  <div class="map-wrapper" ref="mapEl">
    <div id="map" class="map-canvas"></div>
  </div>
  </div>

</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import geojsonData from '../data/melbournesuburbetymologywithgeometry.geojson?url'

const props = withDefaults(
  defineProps<{
    selectedSuburb?: string | null
    metric?: 'safety_score' | 'transport_score' | 'rent_score'
  }>(),
  {
    selectedSuburb: null,
    metric: 'safety_score',
  }
)

const emit = defineEmits<{
  (e: 'suburb-selected', payload: { suburbName: string }): void
}>()

const mapEl = ref<HTMLElement | null>(null)

let map: L.Map | null = null
let suburbLayer: L.GeoJSON | null = null
let selectedLayer: L.Path | null = null

type MetricKey = 'safety_score' | 'transport_score' | 'rent_score'

type SuburbLookupValue = {
  name: string
  safety_score: number | null
  transport_score: number | null
  rent_score: number | null
}

const suburbLookup = new Map<string, SuburbLookupValue>()

function normaliseKey(input: string) {
  return input
    .trim()
    .toLowerCase()
    .replace(/\s+/g, ' ')
    .replace(/\s*\(.*?\)\s*/g, '')
}

function formatSuburbName(input: string) {
  return input
    .trim()
    .replace(/\s+/g, ' ')
    .toLowerCase()
    .split(' ')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

function getSuburbName(feature: any) {
  const rawName =
    feature?.properties?.LOCALITY ||
    feature?.properties?.GAZLOC ||
    'Unknown suburb'

  return formatSuburbName(String(rawName))
}

function getMetricLabel(metric: MetricKey) {
  if (metric === 'safety_score') return 'Safety Score'
  if (metric === 'transport_score') return 'Transport Score'
  return 'Affordability Score'
}

function getMetricValue(suburbName: string, metric: MetricKey): number | null {
  const match = suburbLookup.get(normaliseKey(suburbName))
  if (!match) return null
  return match[metric]
}

function getChoroplethColor(value: number | null | undefined) {
  /*if (value === null || value === undefined)*/ return '#dee2e6'
  //if (value >= 85) return '#2b8a3e'
  //if (value >= 70) return '#66a80f'
  //if (value >= 55) return '#fab005'
  //if (value >= 40) return '#fd7e14'
  //return '#e03131'
}

function getSuburbStyle(feature?: any) {
  const suburbName = feature ? getSuburbName(feature) : ''
  const value = suburbName ? getMetricValue(suburbName, props.metric) : null

  return {
    color: '#495057',
    weight: 1,
    fillColor: getChoroplethColor(value),
    fillOpacity: 0.72,
  }
}

function getHoverStyle(feature?: any) {
  const suburbName = feature ? getSuburbName(feature) : ''
  const value = suburbName ? getMetricValue(suburbName, props.metric) : null

  return {
    color: '#212529',
    weight: 2,
    fillColor: getChoroplethColor(value),
    fillOpacity: 0.9,
  }
}

function getSelectedStyle() {
  return {
    color: '#0d6efd',
    weight: 3,
    fillColor: '#74c0fc',
    fillOpacity: 0.9,
  }
}

function resetAllStyles() {
  if (!suburbLayer) return

  suburbLayer.eachLayer((layer: any) => {
    suburbLayer?.resetStyle(layer)
  })
}

function refreshLayerStyles() {
  if (!suburbLayer) return

  suburbLayer.setStyle((feature) => getSuburbStyle(feature as any))

  if (props.selectedSuburb) {
    highlightSelectedSuburb(props.selectedSuburb, false)
  }
}

function highlightSelectedSuburb(
  name: string | null | undefined,
  shouldFitBounds = true
) {
  if (!suburbLayer) return

  selectedLayer = null
  resetAllStyles()

  suburbLayer.eachLayer((layer: any) => {
    const suburbName = getSuburbName(layer.feature)

    if (name && normaliseKey(suburbName) === normaliseKey(name)) {
      layer.setStyle(getSelectedStyle())
      selectedLayer = layer

      if (shouldFitBounds && layer.getBounds && map) {
        map.fitBounds(layer.getBounds(), { padding: [20, 20] })
      }
    }
  })
}

async function loadSuburbScores() {
  const response = await fetch('https://ito5002-tp2-26.onrender.com/api/v1/suburbs/all')
  if (!response.ok) {
    throw new Error('Failed to fetch suburb map data')
  }

  const raw = await response.json()
  const suburbs = Array.isArray(raw?.suburbs) ? raw.suburbs : []

  suburbLookup.clear()

  suburbs.forEach((suburb: any) => {
    const displayName = String(suburb?.name ?? '').trim()
    if (!displayName) return

    const value: SuburbLookupValue = {
      name: displayName,
      safety_score: suburb?.scores?.safety_score ?? null,
      transport_score: suburb?.scores?.transport_score ?? null,
      rent_score: suburb?.scores?.rent_score ?? null,
    }

    suburbLookup.set(normaliseKey(displayName), value)

    const originalName = String(suburb?.original_name ?? '').trim()
    if (originalName) {
      suburbLookup.set(normaliseKey(originalName), value)
    }
  })
}

onMounted(async () => {
  if (!mapEl.value) return

  map = L.map(mapEl.value, {
    attributionControl: false,
  }).setView([-37.8136, 144.9631], 10)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map)

  await loadSuburbScores()

  const response = await fetch(geojsonData)
  const data = await response.json()

  suburbLayer = L.geoJSON(data, {
    style: (feature) => getSuburbStyle(feature as any),
    onEachFeature: (feature, layer) => {
      const suburbName = getSuburbName(feature)
      //const metricValue = getMetricValue(suburbName, props.metric)
      //const metricLabel = getMetricLabel(props.metric)

      layer.on({
        mouseover: (e) => {
          if (e.target !== selectedLayer) {
            e.target.setStyle(getHoverStyle(feature))
          }
        },
        mouseout: (e) => {
          if (e.target !== selectedLayer) {
            suburbLayer?.resetStyle(e.target)
          }
        },
        click: () => {
          highlightSelectedSuburb(suburbName)

          emit('suburb-selected', {
            suburbName,
          })
        },
      })

      layer.bindPopup(`<strong>${suburbName}</strong>`)
    },
  }).addTo(map)

  highlightSelectedSuburb(props.selectedSuburb, false)
})

watch(
  () => props.selectedSuburb,
  (newSuburb) => {
    highlightSelectedSuburb(newSuburb)
  }
)

watch(
  () => props.metric,
  () => {
    refreshLayerStyles()
  }
)

onBeforeUnmount(() => {
  map?.remove()
  map = null
})
</script>


<style scoped>
.map-wrapper {
  width: 100%;
  height: clamp(320px, 55vh, 700px);
  min-height: 320px;
}

.map-canvas {
  width: 100%;
  height: 100%;
  border-radius: 12px;
  overflow: hidden;
}

/* Tablet */
@media (max-width: 992px) {
  .map-wrapper {
    height: clamp(300px, 50vh, 550px);
  }
}

/* Mobile */
@media (max-width: 576px) {
  .map-wrapper {
    height: 320px;
  }
}
</style>
