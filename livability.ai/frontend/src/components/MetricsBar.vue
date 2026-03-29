<script setup lang="ts">
import type { AveragesApiResponse, SuburbApiResponse } from '@/services/api'

const props = defineProps<{
  selectedSuburb?: string | null
  suburbData?: SuburbApiResponse | null
  averages?: AveragesApiResponse | null
  loading?: boolean
  error?: string
}>()


function formatValue(value: number | null | undefined, suffix = '') {
  if (value === null || value === undefined) return '—'
  return `${value}${suffix}`
}

function formatCurrency(value: number | null | undefined) {
  if (value === null || value === undefined) return '—'
  return `$${value}/week`
}
</script>

<template>
<div class="container mt-5">
  <div class="row g-3 align-items-stretch">


    <!--<div class="col-12 col-md-4 d-flex">
      <div class="card flex-fill shadow-sm" id="scores">
        <div class="card-body">
          <h6 class="form-label">Livability Scores</h6>

          <p class="mb-2">
            <strong>Affordability Score:</strong>
            {{ formatValue(props.suburbData?.affordability_score) }}
          </p>
          <p class="mb-2">
            <strong>Safety Score:</strong>
            {{ formatValue(props.suburbData?.safety_score) }}
          </p>
          <p class="mb-0">
            <strong>Transport Score:</strong>
            {{ formatValue(props.suburbData?.transport_score) }}
          </p>
        </div>
      </div>
    </div>-->

    <div class="col-12 col-md-4 d-flex">
      <div class="card flex-fill shadow-sm" id="rentbreakdown">
        <div class="card-body">
          <h6 class="form-label">Rent Breakdown</h6>

          <p class="mb-2">
            <strong>1 bed flat:</strong>
            {{ formatCurrency(props.suburbData?.rent?.['1bed_flat']) }}
          </p>
          <p class="mb-2">
            <strong>2 bed flat:</strong>
            {{ formatCurrency(props.suburbData?.rent?.['2bed_flat']) }}
          </p>
          <p class="mb-2">
            <strong>3 bed flat:</strong>
            {{ formatCurrency(props.suburbData?.rent?.['3bed_flat']) }}
          </p>
          <p class="mb-2">
            <strong>2 bed house:</strong>
            {{ formatCurrency(props.suburbData?.rent?.['2bed_house']) }}
          </p>
          <p class="mb-2">
            <strong>3 bed house:</strong>
            {{ formatCurrency(props.suburbData?.rent?.['3bed_house']) }}
          </p>
          <p class="mb-0">
            <strong>4 bed house:</strong>
            {{ formatCurrency(props.suburbData?.rent?.['4bed_house']) }}
          </p>
        </div>
      </div>
    </div>

    <div class="col-12 col-md-4 d-flex">
      <div class="card flex-fill shadow-sm" id="transportbreakdown">
        <div class="card-body">
          <h6 class="form-label">Transport Breakdown</h6>

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
        </div>
      </div>
    </div>

  </div>
</div>
</template>
