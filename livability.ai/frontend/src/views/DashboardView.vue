<script setup lang="ts">
import { onMounted, ref, watch, computed } from 'vue'
import {
  fetchAverages,
  fetchSuburbByName,
  fetchSimilarSuburbs,
  type AveragesApiResponse,
  type SuburbApiResponse,
  type SimilarSuburbsApiResponse,
} from '@/services/api'
import MapView from '../components/MapView.vue'
import DashboardSideBar from '@/components/DashboardSideBar.vue'
import MetricsBar from '@/components/MetricsBar.vue'
const props = defineProps<{
  selectedSuburb?: string | null
  setSelectedSuburb?: (name: string) => void
}>()
const similarResults = ref<SimilarSuburbsApiResponse | null>(null)
const similarLoading = ref(false)
const similarError = ref('')
const showSimilarPanel = ref(false)

const selectedSuburbName = computed(
  () => suburbData.value?.name ?? suburbData.value?.suburb ?? ''
)

function formatCurrency(value: number | null | undefined) {
  if (value === null || value === undefined) return '$—'
  return `$${Number(value).toFixed(0)}`
}

function formatNumber(value: number | null | undefined, digits = 1) {
  if (value === null || value === undefined) return '—'
  return Number(value).toFixed(digits).replace(/\.0$/, '')
}

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

async function loadSimilarSuburbs() {
  if (!selectedSuburbName.value) return

  similarLoading.value = true
  similarError.value = ''
  showSimilarPanel.value = true

  try {
    similarResults.value = await fetchSimilarSuburbs(selectedSuburbName.value, 5)
  } catch (err) {
    similarError.value =
      err instanceof Error ? err.message : 'Failed to fetch similar suburbs'
    similarResults.value = null
  } finally {
    similarLoading.value = false
  }
}

async function loadSuburbDetails(name: string) {
  loading.value = true
  error.value = ''

  try {
    const data = await fetchSuburbByName(name)
    suburbData.value = data

    similarResults.value = null
    similarError.value = ''
    showSimilarPanel.value = false

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
        <MapView :selected-suburb="currentSelectedSuburb" :metric="selectedMetric" @suburb-selected="handleMapClick" />
      </div>

      <div class="col-3">
        <DashboardSideBar :selectedSuburb="props.selectedSuburb" :setSelectedSuburb="props.setSelectedSuburb"
          :suburbData="suburbData" :averages="averages" :loading="loading" :error="error" />
      </div>

    </div>
    <div class="row justify-content-center">
      <MetricsBar :selected-suburb="currentSelectedSuburb" :suburb-data="suburbData" :averages="averages"
        :loading="loading" :error="error" :selected-metric="selectedMetric" />
    </div>
  </div>

  <div v-if="suburbData" class="row justify-content-center mt-3">
  <div class="col-12 d-flex justify-content-center">
    <button
      class="btn btn-dark px-4"
      @click="loadSimilarSuburbs"
      :disabled="similarLoading || !selectedSuburbName"
    >
      {{ similarLoading ? 'Finding similar suburbs...' : 'Find Similar' }}
    </button>
  </div>
</div>
<section v-if="showSimilarPanel" class="row justify-content-center mt-4 mb-4">
  <div class="col-12">
    <div class="border border-light-subtle rounded p-4">
      <h3 class="mb-3">Similar suburbs to {{ selectedSuburbName }}</h3>

      <p v-if="similarError" class="text-danger mb-0">
        {{ similarError }}
      </p>

      <p v-else-if="similarLoading" class="mb-0">
        Loading similar suburbs...
      </p>

      <p v-else-if="similarResults?.error" class="mb-0">
        {{ similarResults.error }}
      </p>

      <div v-else-if="similarResults?.similar?.length" class="row g-3">
        <div
          v-for="(item, index) in similarResults.similar"
          :key="`${item.suburb}-${index}`"
          class="col-md-6 col-lg-4"
        >
          <div class="border border-light-subtle p-3 h-100">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <h5 class="mb-0">{{ item.suburb }}</h5>
              <span class="badge text-bg-dark">#{{ index + 1 }}</span>
            </div>

            <p class="mb-2">
              <strong>Similarity score:</strong>
              {{ formatNumber(item.similarity_score *100, 1) }}%
            </p>

            <p class="mb-1"><strong>Rent breakdown (weekly):</strong></p>
            <div class="row mb-2 small">
              <div class="col-6">
                <p class="mb-1">1 bed flat: {{ formatCurrency(item.rent?.['1bed_flat']) }}</p>
                <p class="mb-1">2 bed flat: {{ formatCurrency(item.rent?.['2bed_flat']) }}</p>
                <p class="mb-1">3 bed flat: {{ formatCurrency(item.rent?.['3bed_flat']) }}</p>
              </div>
              <div class="col-6">
                <p class="mb-1">2 bed house: {{ formatCurrency(item.rent?.['2bed_house']) }}</p>
                <p class="mb-1">3 bed house: {{ formatCurrency(item.rent?.['3bed_house']) }}</p>
                <p class="mb-1">4 bed house: {{ formatCurrency(item.rent?.['4bed_house']) }}</p>
              </div>
            </div>

            <p class="mb-2">
              <strong>Crime rate (per 1,000):</strong>
              {{ formatNumber(item.crime?.offence_rate_1000, 0) }}
            </p>

            <p class="mb-1">
              <strong>Transport score:</strong>
              {{ formatNumber(item.scores?.transport_score) }}
            </p>
            <p class="mb-1">
              Train: {{ formatNumber(item.transport?.train_stops, 0) }}
            </p>
            <p class="mb-1">
              Tram: {{ formatNumber(item.transport?.tram_stops, 0) }}
            </p>
            <p class="mb-0">
              Bus: {{ formatNumber(item.transport?.bus_stops, 0) }}
            </p>
          </div>
        </div>
      </div>

      <p v-else class="mb-0">No similar suburbs found.</p>
    </div>
  </div>
</section>
</template>

<style scoped></style>
