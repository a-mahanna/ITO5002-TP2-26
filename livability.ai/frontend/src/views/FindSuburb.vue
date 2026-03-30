<script setup lang="ts">
import { computed, ref } from 'vue'
import { fetchRecommendations, type RecommendApiResponse, type RecommendResult } from '@/services/api'

const propertyType = ref('2bed_flat')
const budget = ref(700)
const safetyWeight = ref(0.5)
const transportWeight = ref(0.5)
const results = ref<RecommendApiResponse | null>(null)
const loading = ref(false)
const error = ref('')

const propertyOptions = [
  { label: '1 bed flat', value: '1bed_flat' },
  { label: '2 bed flat', value: '2bed_flat' },
  { label: '3 bed flat', value: '3bed_flat' },
  { label: '2 bed house', value: '2bed_house' },
  { label: '3 bed house', value: '3bed_house' },
  { label: '4 bed house', value: '4bed_house' },
]

function formatCurrency(value: number | null | undefined) {
  if (value === null || value === undefined) return 'Rental data not available for this suburb'
  return `$${value}/week`
}

function formatValue(value: number | null | undefined, digits = 1) {
  if (value === null || value === undefined) return '—'
  return Number(value).toFixed(digits).replace(/\.0$/, '')
}

function transportAccessibilityScore(item: RecommendResult) {
  return item.scores?.transport_score ?? item.transport?.weighted_score ?? null
}

function safetyScore(item: RecommendResult) {
  return item.scores?.safety_score ?? null
}

function buildFrontendExplanation(item: RecommendResult) {
  const parts: string[] = []

  if (item.rent !== null && item.rent !== undefined) {
    if (item.rent <= budget.value) {
      const diff = Math.round(((budget.value - item.rent) / budget.value) * 100)
      parts.push(`Median rent is ${formatCurrency(item.rent)}, around ${diff}% below your selected maximum budget.`)
    } else {
      parts.push(`Median rent is ${formatCurrency(item.rent)}.`)
    }
  } else {
    parts.push('Rental data is not available for this suburb.')
  }

  if (safetyScore(item) !== null) {
    parts.push(`Safety score: ${formatValue(safetyScore(item))}.`)
  }

  if (transportAccessibilityScore(item) !== null) {
    parts.push(`Transport accessibility score: ${formatValue(transportAccessibilityScore(item))}.`)
  }

  if (item.distance_to_cbd_km !== null && item.distance_to_cbd_km !== undefined) {
    parts.push(`Distance to CBD: ${formatValue(item.distance_to_cbd_km)} km.`)
  }

  return parts.join(' ')
}

const sortedRecommendations = computed(() => {
  const items = [...(results.value?.recommendations ?? [])]

  return items.sort((a, b) => {
    const aSafety = a.scores?.safety_score ?? -Infinity
    const bSafety = b.scores?.safety_score ?? -Infinity
    const aTransport = transportAccessibilityScore(a) ?? -Infinity
    const bTransport = transportAccessibilityScore(b) ?? -Infinity
    const aPreference = a.preference_score ?? -Infinity
    const bPreference = b.preference_score ?? -Infinity
    const aDistance = a.distance_to_cbd_km ?? Infinity
    const bDistance = b.distance_to_cbd_km ?? Infinity

    if (safetyWeight.value > transportWeight.value) {
      if (bSafety !== aSafety) return bSafety - aSafety
      if (bPreference !== aPreference) return bPreference - aPreference
      return aDistance - bDistance
    }

    if (transportWeight.value > safetyWeight.value) {
      if (bTransport !== aTransport) return bTransport - aTransport
      if (bPreference !== aPreference) return bPreference - aPreference
      return aDistance - bDistance
    }

    if (bPreference !== aPreference) return bPreference - aPreference
    return aDistance - bDistance
  })
})

async function runSearch() {
  loading.value = true
  error.value = ''

  try {
    results.value = await fetchRecommendations({
      budget: budget.value,
      propertyType: propertyType.value,
      safetyWeight: safetyWeight.value,
      transportWeight: transportWeight.value,
      n: 12,
    })
  } catch (err) {
    console.error('Search failed:', err)
    results.value = null
    error.value = err instanceof Error ? err.message : 'Failed to fetch results'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="container py-4">
    <div class="card border border-light-subtle shadow-sm mb-4">
      <div class="card-body">
        <h1 class="mb-3 text-center">Find Your Match</h1>

        <p class="text-center text-muted mb-4">
          Select your property type, budget, and how much you care about safety and
          transport. We’ll rank matching suburbs for you.
        </p>

        <div class="row g-3">
          <div class="col-12 col-md-6">
            <label for="propertyType" class="form-label">Property Type</label>
            <select id="propertyType" v-model="propertyType" class="form-select">
              <option v-for="option in propertyOptions" :key="option.value" :value="option.value">
                {{ option.label }}
              </option>
            </select>
          </div>

          <div class="col-12 col-md-6">
            <label for="budget" class="form-label">Maximum Budget: ${{ budget }}/week</label>
            <input id="budget" v-model="budget" type="range" class="form-range" min="200" max="2000" step="10" />
            <input v-model="budget" type="number" class="form-control" min="200" max="2000" step="10" />
          </div>

          <div class="col-12 col-md-6">
            <label for="safetyWeight" class="form-label">
              Safety Importance: {{ Math.round(safetyWeight * 100) }}%
            </label>
            <input id="safetyWeight" v-model="safetyWeight" type="range" class="form-range" min="0" max="1" step="0.1" />
          </div>

          <div class="col-12 col-md-6">
            <label for="transportWeight" class="form-label">
              Transport Importance: {{ Math.round(transportWeight * 100) }}%
            </label>
            <input id="transportWeight" v-model="transportWeight" type="range" class="form-range" min="0" max="1" step="0.1" />
          </div>

          <div class="col-12 d-grid d-md-flex justify-content-md-end">
            <button class="btn btn-primary px-4" @click="runSearch" :disabled="loading">
              {{ loading ? 'Searching...' : 'Find Matches' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-if="results?.message" class="alert alert-warning">
      {{ results.message }}
    </div>

    <div v-if="sortedRecommendations.length" class="mb-3">
      <div class="d-flex justify-content-between align-items-center mb-3 flex-wrap gap-2">
        <h3 class="mb-0">Recommended Suburbs</h3>
        <small class="text-muted">
          Sorted by
          {{ safetyWeight > transportWeight ? 'safety first' : transportWeight > safetyWeight ? 'transport first' : 'overall match score' }}
          with distance to CBD as a tie-breaker.
        </small>
      </div>

      <div class="row g-3">
        <div v-for="item in sortedRecommendations" :key="item.suburb" class="col-12 col-lg-6">
          <div class="card h-100 shadow-sm border border-light-subtle">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start mb-2">
                <h5 class="card-title mb-0">{{ item.suburb }}</h5>
                <span class="badge text-bg-light">Match {{ formatValue(item.preference_score) }}</span>
              </div>

              <p class="mb-2"><strong>Rent:</strong> {{ formatCurrency(item.rent) }}</p>
              <p class="mb-2"><strong>Safety Score:</strong> {{ formatValue(item.scores?.safety_score) }}</p>
              <p class="mb-2"><strong>Transport Accessibility Score:</strong> {{ formatValue(transportAccessibilityScore(item)) }}</p>
              <p class="mb-2"><strong>Distance to CBD:</strong> {{ item.distance_to_cbd_km ?? '—' }} km</p>

              <p class="mb-0 text-muted">
                {{ buildFrontendExplanation(item) }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <div class="card border border-light-subtle shadow-sm mt-4">
        <div class="card-body small">
          <p class="mb-2">
            <strong>Rent:</strong> Median weekly rent by property type. Some suburbs may have missing rental data for some dwelling types.
          </p>
          <p class="mb-2">
            <strong>Safety:</strong> Uses suburb safety scores derived from recorded offences and should be treated as a general indicator.
          </p>
          <p class="mb-0">
            <strong>Transport:</strong> We display a transport accessibility score rather than raw stop counts so the interface is easier to interpret.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
