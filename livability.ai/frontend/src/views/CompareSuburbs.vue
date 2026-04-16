<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import {
  fetchCompareSuburbs,
  searchSuburbs,
  type CompareApiResponse,
  type SuburbApiResponse,
} from '@/services/api'

const suburb1 = ref('')
const suburb2 = ref('')
const suburb3 = ref('')

const suggestions1 = ref<string[]>([])
const suggestions2 = ref<string[]>([])
const suggestions3 = ref<string[]>([])

const showSuggestions1 = ref(false)
const showSuggestions2 = ref(false)
const showSuggestions3 = ref(false)

const loading = ref(false)
const error = ref('')
const results = ref<CompareApiResponse | null>(null)
const hasSearched = ref(false)

const suburbInputs = computed(() =>
  [suburb1.value, suburb2.value, suburb3.value]
    .map((name) => name.trim())
    .filter((name) => name.length > 0)
)

function formatCurrency(value: number | null | undefined) {
  if (value === null || value === undefined) return '$—'
  return `$${Number(value).toFixed(0)}`
}

function formatDistance(value: number | null | undefined) {
  if (value === null || value === undefined) return '—'
  return `${Number(value).toFixed(1)}km`
}

function formatNumber(value: number | null | undefined, digits = 1) {
  if (value === null || value === undefined) return '—'
  return Number(value).toFixed(digits).replace(/\.0$/, '')
}

function crimeRatePer1000(suburb: SuburbApiResponse) {
  return suburb.safety_score ?? suburb.scores?.safety_score ?? null
}

function transportAccessibilityScore(suburb: SuburbApiResponse) {
  return suburb.transport_score ?? suburb.scores?.transport_score ?? suburb.transport?.weighted_score ?? null
}

function hideSuggestions(inputNumber: 1 | 2 | 3) {
  window.setTimeout(() => {
    if (inputNumber === 1) showSuggestions1.value = false
    if (inputNumber === 2) showSuggestions2.value = false
    if (inputNumber === 3) showSuggestions3.value = false
  }, 150)
}

function showSuggestions(inputNumber: 1 | 2 | 3) {
  if (inputNumber === 1) showSuggestions1.value = true
  if (inputNumber === 2) showSuggestions2.value = true
  if (inputNumber === 3) showSuggestions3.value = true
}

async function loadSuggestions(
  query: string,
  target: typeof suggestions1
) {
  const cleaned = query.trim()

  if (cleaned.length < 1) {
    target.value = []
    return
  }

  try {
    const response = await searchSuburbs(cleaned)
    target.value = Array.isArray(response?.results)
      ? response.results.map((item: any) => item.name).slice(0, 6)
      : []
  } catch {
    target.value = []
  }
}

watch(suburb1, async (value) => {
  await loadSuggestions(value, suggestions1)
})

watch(suburb2, async (value) => {
  await loadSuggestions(value, suggestions2)
})

watch(suburb3, async (value) => {
  await loadSuggestions(value, suggestions3)
})

function selectSuggestion(inputNumber: 1 | 2 | 3, suburbName: string) {
  if (inputNumber === 1) {
    suburb1.value = suburbName
    suggestions1.value = []
    showSuggestions1.value = false
  }

  if (inputNumber === 2) {
    suburb2.value = suburbName
    suggestions2.value = []
    showSuggestions2.value = false
  }

  if (inputNumber === 3) {
    suburb3.value = suburbName
    suggestions3.value = []
    showSuggestions3.value = false
  }
}

async function compareSuburbs() {
  error.value = ''
  results.value = null
  hasSearched.value = true

  if (suburbInputs.value.length < 2) {
    error.value = 'Please enter at least 2 suburbs to compare.'
    return
  }

  loading.value = true

  try {
    results.value = await fetchCompareSuburbs(suburbInputs.value)
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to compare suburbs'
  } finally {
    loading.value = false
  }
}

function suburbKey(suburb: any, index: number) {
  return suburb.name ?? suburb.suburb ?? `suburb-${index}`
}

const displayedSuburbs = computed(() => results.value?.suburbs ?? [])
</script>

<template>
  <div class="container py-4">
    <section class="card border border-light-subtle shadow-sm mb-4 search-card">
      <div class="card-body">
        <h1 class="text-center mb-4">Compare Suburbs</h1>
        <p class="text-center compare-subtitle mb-5">
          Enter up to 3 suburbs below to compare
        </p>

        <div class="row g-4">
          <div class="col-md-4">
            <label class="form-label">Suburb 1</label>
            <div class="position-relative">
              <input v-model="suburb1" type="text" class="form-control" placeholder="e.g. Camberwell"
                @focus="showSuggestions(1)" @blur="hideSuggestions(1)" />

              <ul v-if="showSuggestions1 && suggestions1.length" class="list-group autocomplete-list">
                <li v-for="suggestion in suggestions1" :key="suggestion" class="list-group-item list-group-item-action"
                  @mousedown.prevent="selectSuggestion(1, suggestion)">
                  {{ suggestion }}
                </li>
              </ul>
            </div>
          </div>

          <div class="col-md-4">
            <label class="form-label">Suburb 2</label>
            <div class="position-relative">
              <input v-model="suburb2" type="text" class="form-control" placeholder="e.g. Preston"
                @focus="showSuggestions(2)" @blur="hideSuggestions(2)" />

              <ul v-if="showSuggestions2 && suggestions2.length" class="list-group autocomplete-list">
                <li v-for="suggestion in suggestions2" :key="suggestion" class="list-group-item list-group-item-action"
                  @mousedown.prevent="selectSuggestion(2, suggestion)">
                  {{ suggestion }}
                </li>
              </ul>
            </div>
          </div>

          <div class="col-md-4">
            <label class="form-label">Suburb 3 (optional)</label>
            <div class="position-relative">
              <input v-model="suburb3" type="text" class="form-control" placeholder="e.g. Kew"
                @focus="showSuggestions(3)" @blur="hideSuggestions(3)" />

              <ul v-if="showSuggestions3 && suggestions3.length" class="list-group autocomplete-list">
                <li v-for="suggestion in suggestions3" :key="suggestion" class="list-group-item list-group-item-action"
                  @mousedown.prevent="selectSuggestion(3, suggestion)">
                  {{ suggestion }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <div class="text-center mt-4">
        <button class="btn btn-dark px-4" @click="compareSuburbs" :disabled="loading">
          {{ loading ? 'Comparing...' : 'Compare suburbs' }}
        </button>
      </div>

      <p v-if="error" class="text-danger mt-3 mb-0 text-center">
        {{ error }}
      </p>
    </section>

    <section v-if="displayedSuburbs.length" class="mb-4">
      <div class="row g-4">
        <div v-for="(suburb, index) in displayedSuburbs" :key="suburbKey(suburb, index)" class="col-lg-4 col-md-6">
          <div class="card h-100 shadow-sm border border-light-subtle p-4">
            <h2 class="suburb-name mb-4">
              {{ suburb.name ?? suburb.suburb ?? 'Unknown suburb' }}
            </h2>

            <div class="metric-line mb-3">
              <strong>Distance to CBD:</strong>
              {{ formatDistance(suburb.distance_to_cbd_km) }}
            </div>

            <div class="mb-4">
              <h3 class="section-heading">Rent Breakdown (Median per week):</h3>
              <table class="table table-bordered rent-table mb-0">
                <tbody>
                  <tr>
                    <td>1 bed flat: {{ formatCurrency(suburb.rent?.['1bed_flat']) }}</td>
                    <td>2 bed flat: {{ formatCurrency(suburb.rent?.['2bed_flat']) }}</td>
                  </tr>
                  <tr>
                    <td>3 bed flat: {{ formatCurrency(suburb.rent?.['3bed_flat']) }}</td>
                    <td>2 bed house: {{ formatCurrency(suburb.rent?.['2bed_house']) }}</td>
                  </tr>
                  <tr>
                    <td>3 bed house: {{ formatCurrency(suburb.rent?.['3bed_house']) }}</td>
                    <td>4 bed house: {{ formatCurrency(suburb.rent?.['4bed_house']) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="mb-4">
              <h3 class="section-heading">Crime</h3>
              <p class="mb-1">
                Crime score:
                {{ formatNumber(crimeRatePer1000(suburb)) }}
              </p>
              <p class="mb-0">
                Crime rate (per 1,000):
                {{ formatNumber(suburb.crime?.offence_rate_1000, 0) }}
              </p>
            </div>

            <div>
              <h3 class="section-heading">Public Transport Accessibility</h3>
              <p class="mb-1">
                Train stations:
                {{ formatNumber(suburb.transport?.train_stops, 0) }}
              </p>
              <p class="mb-1">
                Tram stops:
                {{ formatNumber(suburb.transport?.tram_stops, 0) }}
              </p>
              <p class="mb-1">
                Bus stops:
                {{ formatNumber(suburb.transport?.bus_stops, 0) }}
              </p>
              <p class="mb-0">
                Transport accessibility score:
                {{ formatNumber(transportAccessibilityScore(suburb)) }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section v-else-if="hasSearched && !loading && !error" class="border p-4 text-center">
      No matching suburbs were returned. Check the suburb spelling and try again.
    </section>
  </div>
</template>

<style scoped>
.autocomplete-list {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  z-index: 20;
  max-height: 220px;
  overflow-y: auto;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.autocomplete-list .list-group-item {
  cursor: pointer;
}
</style>
