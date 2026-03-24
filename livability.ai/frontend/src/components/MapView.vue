<template>
  <div ref="mapEl" class="map-container"></div>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref } from 'vue'
import L from 'leaflet'
import geojsonData from '../data/melbournesuburbetymologywithgeometry.geojson?url'

const mapEl = ref<HTMLElement | null>(null)

let map: L.Map | null = null
let suburbLayer: L.GeoJSON | null = null

const emit = defineEmits<{
  (e: 'suburb-selected', suburbName: string): void
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

onMounted(async () => {
  if (!mapEl.value) return

  map = L.map(mapEl.value, {
  attributionControl: false
}).setView([-37.8136, 144.9631], 10)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map)

  const response = await fetch(geojsonData)
  const data = await response.json()

  suburbLayer = L.geoJSON(data, {
    style: getSuburbStyle,
    onEachFeature: (feature, layer) => {
      const suburbName =
        feature?.properties?.LOCALITY ||
        feature?.properties?.GAZLOC ||
        'Unknown suburb'

      layer.on({
        mouseover: (e) => {
          e.target.setStyle(getHoverStyle())
        },
        mouseout: (e) => {
          suburbLayer?.resetStyle(e.target)
        },
        click: (e) => {
          const clickedLayer = e.target
          map?.fitBounds(clickedLayer.getBounds())
          emit('suburb-selected', suburbName)
        },
      })

      layer.bindPopup(`<strong>${suburbName}</strong>`)
    },
  }).addTo(map)
})

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
