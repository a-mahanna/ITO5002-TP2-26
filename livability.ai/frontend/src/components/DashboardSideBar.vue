<script setup lang="ts">

const props = defineProps<{
  suburb?: string | null
  info?: string | null
}>()

</script>

<template>
  <div class="container">
    <label for="suburbname" class="form-label mt-3">Selected Suburb</label>
    <div class="card align-items-center mb-3" id="suburbname">
      <p>{{ props.suburb }}</p>
    </div>
    <label for="suburbinfo" class="form-label mt-3">Suburb Information</label>
    <div class="card align-items-center mb-3" id="suburbinfo">
      <p>{{ props.info }}</p>
    </div>
    <label for="averagecompare" class="form-label mt-3">Comparison to City Average</label>
    <div class="card align-items-center mb-3" id="averagecompare">
      comparison to City average
    </div>
  </div>
</template>
