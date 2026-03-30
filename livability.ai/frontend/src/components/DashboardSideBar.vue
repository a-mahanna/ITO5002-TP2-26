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

function getTransportAccessibilityScore(data?: SuburbApiResponse | null) {
  return data?.transport_score ?? data?.scores?.transport_score ?? data?.pt_score ?? data?.transport?.weighted_score ?? null
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
  <div class="container mt-5">
    <label for="suburbname" class="form-label">Selected Suburb</label>
    <div class="card mb-3" id="suburbname">
      <div class="card-body">
        <h5 class="card-title mb-0">{{ displayName() }}</h5>
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
            {{ getDeviationText(getTransportAccessibilityScore(props.suburbData), getTransportAverage(props.averages)) }}
          </span>
        </p>
      </div>
    </div>

    <!--<label for="aboutdata" class="form-label">About this data</label>
    <div class="card mb-3" id="aboutdata">
      <div class="card-body small">
        <p class="mb-2">
          <strong>Rent:</strong>
          Median weekly rent by property type. Some suburbs have limited rental listings and may be missing data for certain property types.
        </p>
        <p class="mb-2">
          <strong>Safety:</strong>
          Total recorded criminal offences for the suburb. Raw offence counts are best used as a general indicator only.
        </p>
        <p class="mb-0">
          <strong>Transport:</strong>
          Transport accessibility score based on weighted public transport availability. Higher means more nearby transport options.
        </p>
      </div>
    </div> -->
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

@media (min-width: 992px) {
  .sidebar-inner {
    position: sticky;
    top: 1rem;
  }
}

@media (max-width: 991.98px) {
  .sidebar-inner {
    position: static;
  }
}

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
