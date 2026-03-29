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

function displayName() {
  return (
    props.suburbData?.name ||
    props.suburbData?.suburb ||
    props.selectedSuburb ||
    'No suburb selected'
  )
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

function getDeviationClass(
  suburbValue: number | null | undefined,
  avgValue: number | null | undefined,
  higherIsBetter: boolean
) {
  if (
    suburbValue === null ||
    suburbValue === undefined ||
    avgValue === null ||
    avgValue === undefined ||
    avgValue === 0
  ) {
    return 'text-muted'
  }

  const diff = suburbValue - avgValue

  if (diff === 0) return 'text-muted'

  const isFavourable = higherIsBetter ? diff > 0 : diff < 0
  return isFavourable ? 'text-success' : 'text-warning'
}

function formatValue(value: number | null | undefined, suffix = '') {
  if (value === null || value === undefined) return '—'
  return `${value}${suffix}`
}

function formatCurrency(value: number | null | undefined) {
  if (value === null || value === undefined) return '—'
  return `$${value}/week`
}

/*function handleMetricChange(event: Event) {
  const value = (event.target as HTMLSelectElement).value as
    | 'safety_score'
    | 'transport_score'
    | 'rent_score'

  emit('update-metric', value)
}*/
</script>

<template>
  <div class="container">
    <label for="suburbname" class="form-label">Selected Suburb</label>
    <div class="card mb-3" id="suburbname">
      <div class="card-body">
        <h5 class="card-title mb-0">{{ displayName() }}</h5>
      </div>
    </div>
       <!-- <label for="metricSelect" class="form-label">Map Metric</label>
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
    </div>-->

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
      <strong>Median Rent: </strong>
      <span>
        {{ getDeviationText(props.suburbData?.median_rent, props.averages?.median_rent) }}
      </span>
    </p>

    <p class="mb-2">
      <strong>Crime: </strong>
      <span
        :class="getDeviationClass(props.suburbData?.crime_rate, props.averages?.crime_rate, false)"
      >
        {{ getDeviationText(props.suburbData?.crime_rate, props.averages?.crime_rate) }}
      </span>
    </p>

    <p class="mb-2">
      <strong>Transport: </strong>
      <span
        :class="getDeviationClass(props.suburbData?.transport_score, props.averages?.transport_score, true)"
      >
        {{ getDeviationText(props.suburbData?.transport_score, props.averages?.transport_score) }}
      </span>
    </p>

    <p class="mb-0">
      <strong>PT Score: </strong>
      <span
        :class="getDeviationClass(props.suburbData?.pt_score, props.averages?.pt_score, true)"
      >
        {{ getDeviationText(props.suburbData?.pt_score, props.averages?.pt_score) }}
      </span>
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
