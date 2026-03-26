<script setup lang="ts">
import { watch } from 'vue'
import MapView from '../components/MapView.vue'
import DashboardSideBar from '@/components/DashboardSideBar.vue'



const props = defineProps<{
  selectedSuburb?: string | null
  selectedInfo?: string | null
  setSelectedSuburb?: (name: string) => void
}>()

function handleMapClick(payload: { suburbName: string; info: string | null }) {
  props.setSelectedSuburb?.(payload.suburbName, payload.info)
}

watch(
  () => props.selectedSuburb,
  (newSuburb) => {
    if (!newSuburb) return
  },
  { immediate: true }
)
watch(
  () => props.selectedInfo,
  (newInfo) => {
    if (!newInfo) return
  }, { immediate: true }
)
</script>

<template>
  <div class="container">
    <div class="row justify-content-center border border-light-subtle">
      <div class="col-9">
        <MapView :selectedSuburb="props.selectedSuburb" @suburb-selected="handleMapClick" />
      </div>

      <div class="col-3 border border-light-subtle">
        <DashboardSideBar :suburb="props.selectedSuburb" :info="props.selectedInfo" />
      </div>
    </div>
  </div>
</template>

<style scoped></style>
