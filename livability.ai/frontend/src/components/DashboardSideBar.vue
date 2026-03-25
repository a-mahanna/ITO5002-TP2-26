<script setup lang="ts">
import { watch, ref } from 'vue'


const props = defineProps<{
  suburb?: string | null
  info?: string | null
}>()

</script>

<template>
  <div class="container sidebar">
  <div class="card rounded-pill text-center" label="Selected Area">
    <p>{{ suburb }}</p>
  </div>
  <div class="card text-center">
    <p>{{ info }}</p>>
  </div>
  <div class="card">
    comparison to City average
  </div>
  </div>
  </template>
