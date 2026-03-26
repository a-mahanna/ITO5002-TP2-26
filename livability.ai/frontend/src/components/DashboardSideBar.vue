<script setup lang="ts">
import { watch, ref } from 'vue'


const props = defineProps<{
  suburb?: string | null
  info?: string | null
}>()

</script>

<template>
  <div class="container sidebar">
  <div class="card align-items-center my-3" label="Selected Area">
    <p>{{ props.suburb }}</p>
  </div>
  <div class="card align-items-center my-3">
    <p>{{ props.info }}</p>>
  </div>
  <div class="card align-items-center my-3">
    comparison to City average
  </div>
  </div>
  </template>
