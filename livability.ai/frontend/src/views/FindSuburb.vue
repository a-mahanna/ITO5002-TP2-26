<script setup lang="ts">
import { ref } from 'vue'

const minBudget = 0
const maxBudget = 10000
const minCrime = 0
const maxCrime = 100
const minTransport = 0
const maxTransport = 100

const budget = ref(500)
const crimeFactor = ref(50)
const transportFactor = ref(50)
</script>

<template>
  <div
    class="container d-flex flex-column align-items-center justify-content-center border border-light-subtle p-5 rounded"
  >
    <div class="row">
      <h1 class="mb-4 text-center">Find Your Match</h1>
      <p class="mb-4 text-center">
        Use our suburb search to find the best match for your lifestyle. Whether you're
        looking for a quiet neighborhood, easy access to public transport, or budget
        friendly options, our search tool will help you discover the perfect suburb that
        fits your needs.
      </p>
      <p class="mb-4 text-center">
        Simply enter your preferences and let our algorithm do the work. Find your ideal
        suburb today and start living your best life!
      </p>
    </div>

    <div class="row w-100 d-flex">
      <div class="mb-4">
        <label class="form-label">Enter your budget: {{ budget }}</label>
        <input
          v-model="budget"
          type="range"
          class="form-range"
          :min="minBudget"
          :max="maxBudget"
        />
      </div>

      <div class="mb-4">
        <label class="form-label">Crime Rate Factor: {{ crimeFactor }}</label>
        <input
          v-model="crimeFactor"
          type="range"
          class="form-range"
          :min="minCrime"
          :max="maxCrime"
        />
      </div>

      <div class="mb-2">
        <label class="form-label">Public Transport Access Factor: {{ transportFactor }}</label>
        <input
          v-model="transportFactor"
          type="range"
          class="form-range"
          :min="minTransport"
          :max="maxTransport"
        />
      </div>
    </div>
  </div>
</template>
