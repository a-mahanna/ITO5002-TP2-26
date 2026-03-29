<script setup lang="ts">
const minBudget = 0
const maxBudget = 10000
const minCrime = 0
const maxCrime = 100
const minTransport = 0
const maxTransport = 100
</script>

<template>

  <div
    class="container d-flex flex-column align-items-center justify-content-center border border-light-subtle p-5 rounded">
    <div class="row">
      <h1 class="mb-4 text-center">Find Your Match</h1>
      <p class="mb-4 text-center">
        Use our suburb search to find the best match for your lifestyle. Whether you're looking for a quiet
        neighborhood, easy access to public transport, or budget friendly options, our search tool will help you
        discover the
        perfect suburb that fits your needs.
      </p>
      <p class="mb-4 text-center">
        Simply enter your preferences and let our algorithm do the work. Find your ideal suburb today and start living
        your best life!
      </p>
    </div>
    <div class="row d-flex">
      <div>
        <label>Enter your budget: </label>
        <input type="range" class="form-range" min="{{ minBudget }}" max="{{ maxBudget }}" v-model="min" />
      </div>
      <div>
        <label>Crime Rate Factor: </label>
        <input type="range" class="form-range" min="{{ minCrime }}" max="{{ maxCrime }}" v-model="min" />
      </div>
      <div>
        <label>Public Transport Access Factor: </label>
        <input type="range" class="form-range" min="{{ minTransport }}" max="{{ maxTransport }}" v-model="min" />
      </div>
    </div>
  </div>
</template>
