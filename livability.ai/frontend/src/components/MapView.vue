<template>
  <div ref="mapEl" class="map-container"></div>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import geojsonData from '../data/melbournesuburbetymologywithgeometry.geojson?url'

const props = defineProps<{
  selectedSuburb?: string | null
}>()

const mapEl = ref<HTMLElement | null>(null)

let map: L.Map | null = null
let suburbLayer: L.GeoJSON | null = null
let selectedLayer: L.Path | null = null

const emit = defineEmits<{
  (e: 'suburb-selected', payload: { suburbName: string; info: string | null }): void
}>()

function getSuburbStyle() {
  return {
    color: '#495057',
    weight: 1,
    fillColor: '#adb5bd',
    fillOpacity: 0.5,
  }
}

function getHoverStyle() {
  return {
    color: '#212529',
    weight: 2,
    fillColor: '#6c757d',
    fillOpacity: 0.7,
  }
}

function getSelectedStyle() {
  return {
    color: '#0d6efd',
    weight: 3,
    fillColor: '#74c0fc',
    fillOpacity: 0.75,
  }
}

function getSuburbName(feature: any) {
  return (
    feature?.properties?.LOCALITY ||
    feature?.properties?.GAZLOC ||
    'Unknown suburb'
  )
}

function getSuburbInfo(feature: any) {
  return (
    feature?.properties?.DETAILS ||
    null
  )
} //cant get it to work yet

function highlightSelectedSuburb(name: string | null | undefined) {
  if (!suburbLayer) return

  selectedLayer = null

  suburbLayer.eachLayer((layer: any) => {
    suburbLayer?.resetStyle(layer)

    const suburbName = getSuburbName(layer.feature)

    if (name && suburbName.trim().toLowerCase() === name.trim().toLowerCase()) {
      layer.setStyle(getSelectedStyle())
      selectedLayer = layer

      if (layer.getBounds && map) {
        map.fitBounds(layer.getBounds(), { padding: [20, 20] })
      }
    }
  })
}

onMounted(async () => {
  if (!mapEl.value) return

  map = L.map(mapEl.value, {
    attributionControl: false,
  }).setView([-37.8136, 144.9631], 10)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map)

  const response = await fetch(geojsonData)
  const data = await response.json()

  suburbLayer = L.geoJSON(data, {
    style: getSuburbStyle,
    onEachFeature: (feature, layer) => {
  const suburbName = getSuburbName(feature)
  const suburbInfo = getSuburbInfo(feature)

  layer.on({
    mouseover: (e) => {
      if (e.target !== selectedLayer) {
        e.target.setStyle(getHoverStyle())
      }
    },
    mouseout: (e) => {
      if (e.target !== selectedLayer) {
        suburbLayer?.resetStyle(e.target)
      }
    },
    click: (e) => {
      const clickedLayer = e.target
      highlightSelectedSuburb(suburbName)
      map?.fitBounds(clickedLayer.getBounds(), { padding: [20, 20] })
      emit('suburb-selected', {
        suburbName,
        info: suburbInfo,
      })
    },
  })

  layer.bindPopup(`<strong>${suburbName}</strong>`)
}
  }).addTo(map)

  highlightSelectedSuburb(props.selectedSuburb)
})

watch(
  () => props.selectedSuburb,
  (newSuburb) => {
    highlightSelectedSuburb(newSuburb)
  }
)

onBeforeUnmount(() => {
  map?.remove()
  map = null
})
</script>

<style scoped>
.map-container {
  height: 500px;
  width: 100%;
  border-radius: 12px;
}
</style>
