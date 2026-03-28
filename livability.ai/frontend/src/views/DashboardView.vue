<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import MapView from '../components/MapView.vue'
import DashboardSideBar from '@/components/DashboardSideBar.vue'
import MetricsBar from '@/components/MetricsBar.vue'
import {
  fetchAverages,
  fetchSuburbByName,
  type AveragesApiResponse,
  type SuburbApiResponse,
} from '@/services/api'

const props = defineProps<{
  selectedSuburb?: string | null
  setSelectedSuburb?: (name: string) => void
}>()

const selectedMetric = ref<'safety_score' | 'transport_score' | 'rent_score'>(
  'safety_score'
)

const currentSelectedSuburb = ref<string | null>(props.selectedSuburb ?? null)
const suburbData = ref<SuburbApiResponse | null>(null)
const averages = ref<AveragesApiResponse | null>(null)
const loading = ref(false)
const error = ref('')

function handleMapClick(payload: { suburbName: string }) {
  currentSelectedSuburb.value = payload.suburbName
  props.setSelectedSuburb?.(payload.suburbName)
}

async function loadSuburbDetails(name: string) {
  loading.value = true
  error.value = ''

  try {
    const data = await fetchSuburbByName(name)
    suburbData.value = data
    console.log('Loaded suburb data:', data)
  } catch (err) {
    suburbData.value = null
    error.value = err instanceof Error ? err.message : 'Failed to load suburb details'
  } finally {
    loading.value = false
  }
}

async function loadAverages() {
  try {
    const data = await fetchAverages()
    averages.value = data
    console.log('Loaded averages:', data)
  } catch (err) {
    console.error('Failed to load averages:', err)
  }
}

watch(
  () => props.selectedSuburb,
  (newSuburb) => {
    currentSelectedSuburb.value = newSuburb ?? null
  },
  { immediate: true }
)

watch(
  currentSelectedSuburb,
  (newSuburb) => {
    if (!newSuburb) {
      suburbData.value = null
      error.value = ''
      return
    }

    loadSuburbDetails(newSuburb)
  },
  { immediate: true }
)

onMounted(() => {
  loadAverages()
})
</script>

<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-9">
        <MapView
          :selected-suburb="currentSelectedSuburb"
          :metric="selectedMetric"
          @suburb-selected="handleMapClick"
        />
      </div>

      <div class="col-3">
        <DashboardSideBar
          :selected-suburb="currentSelectedSuburb"
          :suburb-data="suburbData"
          :averages="averages"
          :loading="loading"
          :error="error"
          :selected-metric="selectedMetric"
          @update-metric="selectedMetric = $event"
        />
      </div>
    </div>

    <div class="row justify-content-center">
      <MetricsBar
        :selected-suburb="currentSelectedSuburb"
        :suburb-data="suburbData"
        :averages="averages"
        :loading="loading"
        :error="error"
        :selected-metric="selectedMetric"
      />
    </div>
  </div>
</template>

<style scoped></style>
