<script setup lang="ts">
import type { AveragesApiResponse, SuburbApiResponse } from '@/services/api'

const props = defineProps<{
  selectedSuburb?: string | null
  suburbData?: SuburbApiResponse | null
  averages?: AveragesApiResponse | null
  loading?: boolean
  error?: string
  selectedMetric?: 'safety_score' | 'transport_score' | 'rent_score'
}>()

const emit = defineEmits<{
  (e: 'update-metric', value: 'safety_score' | 'transport_score' | 'rent_score'): void
}>()

function displayName() {
  return (
    props.suburbData?.name ||
    props.suburbData?.suburb ||
    props.selectedSuburb ||
    'No suburb selected'
  )
}

function formatValue(value: number | null | undefined, suffix = '') {
  if (value === null || value === undefined) return '—'
  return `${value}${suffix}`
}

function formatCurrency(value: number | null | undefined) {
  if (value === null || value === undefined) return '—'
  return `$${value}/week`
}

function handleMetricChange(event: Event) {
  const value = (event.target as HTMLSelectElement).value as
    | 'safety_score'
    | 'transport_score'
    | 'rent_score'

  emit('update-metric', value)
}
</script>

<template>
  <div class="container">
    <label for="suburbname" class="form-label">Selected Suburb</label>
    <div class="card mb-3" id="suburbname">
      <div class="card-body">
        <h5 class="card-title mb-0">{{ displayName() }}</h5>
      </div>
    </div>
        <label for="metricSelect" class="form-label">Map Metric</label>
    <div class="card mb-3" id="metricSelectCard">
      <div class="card-body">
        <select
          id="metricSelect"
          class="form-select"
          :value="props.selectedMetric ?? 'safety_score'"
          @change="handleMetricChange"
        >
          <option value="safety_score">Safety Score</option>
          <option value="transport_score">Transport Score</option>
          <option value="rent_score">Affordability Score</option>
        </select>
      </div>
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
          <strong>Weighted PT Score:</strong>
          {{ formatValue(props.suburbData?.pt_score) }}
        </p>
      </div>
    </div>

    <label for="averagecompare" class="form-label">Comparison to Melbourne Average</label>
    <div class="card mb-3" id="averagecompare">
      <div class="card-body">
        <p class="mb-2">
          <strong>Melbourne Median Rent:</strong>
          {{ formatCurrency(props.averages?.median_rent) }}
        </p>
        <p class="mb-2">
          <strong>Melbourne Crime:</strong>
          {{ formatValue(props.averages?.crime_rate) }}
        </p>
        <p class="mb-2">
          <strong>Melbourne Transport:</strong>
          {{ formatValue(props.averages?.transport_score) }}
        </p>
        <p class="mb-0">
          <strong>Melbourne PT Score:</strong>
          {{ formatValue(props.averages?.pt_score) }}
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.sidebar-wrapper {
  width: 100%;
}

.sidebar-inner {
  width: 100%;
}

.sidebar-card {
  width: 100%;
  border-radius: 12px;
}

.card-body p {
  word-break: break-word;
}

/* Desktop: optional sticky sidebar */
@media (min-width: 992px) {
  .sidebar-inner {
    position: sticky;
    top: 1rem;
  }
}

/* Tablet and below */
@media (max-width: 991.98px) {
  .sidebar-inner {
    position: static;
  }
}

/* Small mobile screens */
@media (max-width: 576px) {
  .sidebar-card .card-body {
    padding: 0.9rem;
  }

  .card-title {
    font-size: 1.1rem;
  }

  .form-label {
    margin-bottom: 0.4rem;
  }
}
</style>
