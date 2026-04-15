<script setup lang="ts">
import type { SuburbApiResponse } from '@/services/api'

const props = defineProps<{
  selectedSuburb?: string | null
  suburbData?: SuburbApiResponse | null
  loading?: boolean
  error?: string
}>()

function formatValue(value: number | null | undefined, suffix = '') {
  if (value === null || value === undefined) return '—'
  return `${value}${suffix}`
}

function formatCurrency(value: number | null | undefined) {
  if (value === null || value === undefined) return 'Rental data not available'
  return `$${value}/week`
}

function transportAccessibilityScore() {
  return (
    props.suburbData?.transport_score ??
    props.suburbData?.scores?.transport_score ??
    props.suburbData?.pt_score ??
    props.suburbData?.transport?.weighted_score ??
    null
  )
}
</script>

<template>
  <div class="container mt-5">
    <div class="row g-3 align-items-stretch">
      <div class="col-12 col-md-4 d-flex">
        <div class="card flex-fill shadow-sm" id="rentbreakdown">
          <div class="card-body">
            <h6 class="form-label">Rent Breakdown</h6>
            <div class="row">
            <div class="col-5">
              <p class="mb-2"><strong>1 bed flat:</strong> {{ formatCurrency(props.suburbData?.rent?.['1bed_flat']) }}</p>
            <p class="mb-2"><strong>2 bed flat:</strong> {{ formatCurrency(props.suburbData?.rent?.['2bed_flat']) }}</p>
            <p class="mb-2"><strong>3 bed flat:</strong> {{ formatCurrency(props.suburbData?.rent?.['3bed_flat']) }}</p>
            </div>
            <div class="col-5">
              <p class="mb-2"><strong>2 bed house:</strong> {{ formatCurrency(props.suburbData?.rent?.['2bed_house']) }}</p>
            <p class="mb-2"><strong>3 bed house:</strong> {{ formatCurrency(props.suburbData?.rent?.['3bed_house']) }}</p>
            <p class="mb-0"><strong>4 bed house:</strong> {{ formatCurrency(props.suburbData?.rent?.['4bed_house']) }}</p>
            </div>
              </div>


            <p class="mb-0 text-muted small">
              Median weekly rent by property type. Some suburbs have limited rental listings and may be missing data for certain property types.
            </p>
          </div>
        </div>
      </div>

      <div class="col-12 col-md-4 d-flex">
        <div class="card flex-fill shadow-sm" id="transportbreakdown">
          <div class="card-body">
            <h6 class="form-label">Transport Accessibility</h6>

            <p class="mb-2">
              <strong>Accessibility Score:</strong>
              {{ formatValue(transportAccessibilityScore()) }}
            </p>
                      <p class="mb-2">
            <strong>Bus Stops:</strong>
            {{ formatValue(props.suburbData?.transport?.bus_stops) }}
          </p>
          <p class="mb-2">
            <strong>Train Stops:</strong>
            {{ formatValue(props.suburbData?.transport?.train_stops) }}
          </p>
          <p class="mb-2">
            <strong>Tram Stops:</strong>
            {{ formatValue(props.suburbData?.transport?.tram_stops) }}
          </p>
          <p class="mb-2">
            <strong>Total Stops:</strong>
            {{ formatValue(props.suburbData?.transport?.total_stops) }}
          </p>
          <p class="mb-0">
            <strong>Weighted Score:</strong>
            {{ formatValue(props.suburbData?.transport?.weighted_score) }}
          </p>
            <p class="mb-0 text-muted small">
              This score reflects weighted public transport availability nearby. We are intentionally showing the accessibility score rather than raw stop counts.
            </p>
          </div>
        </div>
      </div>
      <div class="col-12 col-md-4 d-flex">
        <div class="card flex-fill shadow-sm" id="transportbreakdown">
          <div class="card-body">
            <h6 class="form-label">Crime Rate</h6>

            <p class="mb-2">
              <strong>Total Offences:</strong>
              {{ formatValue(props.suburbData?.crime_rate) }}
            </p>
            <p class="mb-0 text-muted small">
              Total recorded criminal offences for the suburb. Raw offence counts are best used as a general indicator only.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
