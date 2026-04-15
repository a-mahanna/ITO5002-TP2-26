<script setup lang="ts">
import type { AveragesApiResponse, SuburbApiResponse } from '@/services/api'
import SearchBar from './SearchBar.vue'
import { ref, watch } from 'vue'

const search = ref('')

const props = defineProps<{
  selectedSuburb?: string | null
  setSelectedSuburb?: (name: string) => void
  suburbData?: SuburbApiResponse | null
  averages?: AveragesApiResponse | null
  loading?: boolean
  error?: string
  selectedMetric?: 'safety_score' | 'transport_score' | 'rent_score'
}>()

watch(
  () => props.selectedSuburb,
  (newValue) => {
    search.value = newValue ?? ''
  },
  { immediate: true }
)

function displayName() {
  return (
    props.suburbData?.name ||
    props.suburbData?.suburb ||
    props.selectedSuburb ||
    'No suburb selected'
  )
}

function formatSuburbName(input: string) {
  return input
    .trim()
    .replace(/\s+/g, ' ')
    .toLowerCase()
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

function runSearch(suburbName: string) {
  const cleaned = formatSuburbName(suburbName)
  if (!cleaned) return

  search.value = cleaned
  props.setSelectedSuburb?.(cleaned)
}

function getTransportAccessibilityScore(data?: SuburbApiResponse | null) {
  return (
    data?.transport_score ??
    data?.scores?.transport_score ??
    data?.pt_score ??
    data?.transport?.weighted_score ??
    null
  )
}

function getTransportAverage(avg?: AveragesApiResponse | null) {
  return avg?.transport_score ?? avg?.pt_score ?? null
}

function getDeviationText(
  suburbValue: number | null | undefined,
  avgValue: number | null | undefined
) {
  if (
    suburbValue === null ||
    suburbValue === undefined ||
    avgValue === null ||
    avgValue === undefined ||
    avgValue === 0
  ) {
    return '—'
  }

  const diff = ((suburbValue - avgValue) / avgValue) * 100
  const absDiff = Math.abs(diff).toFixed(1)

  if (diff === 0) return 'At average'
  return diff > 0 ? `${absDiff}% above average` : `${absDiff}% below average`
}

function formatValue(value: number | null | undefined, suffix = '') {
  if (value === null || value === undefined) return '—'
  return `${value}${suffix}`
}

function formatCurrency(value: number | null | undefined) {
  if (value === null || value === undefined) return 'Rental data not available for this suburb'
  return `$${value}/week`
}
</script>

<template>


  <div class="container mt-3">
    <!--<label for="suburbname" class="form-label">Selected Suburb</label>
    <div class="card mb-3" id="suburbname">
      <div class="card-body">
        <h5 class="card-title mb-0">{{ displayName() }}</h5>
      </div>
    </div>-->
    <label for="suburbname" class="form-label">Selected Suburb</label>
    <div class="card mb-3">
      <SearchBar v-model="search" @search="runSearch" />
    </div>

    <label for="overview" class="form-label">Overview</label>
    <div class="card mb-3" id="overview">
      <div class="card-body">
        <p class="mb-2">
          <strong>Distance to CBD:</strong>
          {{ formatValue(props.suburbData?.distance_to_cbd_km, ' km') }}
        </p>
        <p class="mb-2">
          <strong>Median Rent:</strong>
          {{ formatCurrency(props.suburbData?.median_rent) }}
        </p>
        <p class="mb-2">
          <strong>Total Offences:</strong>
          {{ formatValue(props.suburbData?.crime_rate) }}
        </p>
        <p class="mb-0">
          <strong>Transport Accessibility Score:</strong>
          {{ formatValue(getTransportAccessibilityScore(props.suburbData)) }}
        </p>
      </div>
    </div>

    <label for="averagecompare" class="form-label">Comparison to Melbourne Average</label>
    <div class="card mb-3" id="averagecompare">
      <div class="card-body">
        <p class="mb-2">
          <strong>Median Rent:</strong>
          <span>
            {{ getDeviationText(props.suburbData?.median_rent, props.averages?.median_rent) }}
          </span>
        </p>

        <p class="mb-2">
          <strong>Crime:</strong>
          <span>
            {{ getDeviationText(props.suburbData?.crime_rate, props.averages?.crime_rate) }}
          </span>
        </p>

        <p class="mb-0">
          <strong>Transport Accessibility:</strong>
          <span>
            {{ getDeviationText(
              getTransportAccessibilityScore(props.suburbData),
              getTransportAverage(props.averages)
            ) }}
          </span>
        </p>
      </div>
    </div>
  </div>
</template>
