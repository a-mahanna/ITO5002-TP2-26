<script setup lang="ts">
import { ref, watch } from 'vue'
import { searchSuburbs } from '@/services/api'

const model = defineModel<string>({ default: '' })
const emit = defineEmits<{
  (e: 'search', suburbName: string): void
}>()

const suggestions = ref<Array<{ name: string }>>([])
const loading = ref(false)
let latestRequestId = 0

function dedupeByName(items: Array<{ name: string }>) {
  const seen = new Set<string>()
  return items.filter((item) => {
    const key = item.name.trim().toLowerCase()
    if (!key || seen.has(key)) return false
    seen.add(key)
    return true
  })
}

async function loadSuggestions(query: string) {
  const cleaned = query.trim()
  const requestId = ++latestRequestId

  if (!cleaned) {
    suggestions.value = []
    return
  }

  loading.value = true
  try {
    const response = await searchSuburbs(cleaned)
    if (requestId !== latestRequestId) return

    const incoming = Array.isArray(response?.results)
      ? response.results.map((item: any) => ({ name: item.name }))
      : []

    suggestions.value = dedupeByName(incoming)
  } catch (error) {
    if (requestId !== latestRequestId) return
    console.error('Failed to load suburb suggestions:', error)
    suggestions.value = []
  } finally {
    if (requestId === latestRequestId) {
      loading.value = false
    }
  }
}

function chooseSuggestion(name: string) {
  model.value = name
  suggestions.value = []
  emit('search', name)
}

watch(model, (value) => {
  loadSuggestions(value)
})
</script>

<template>
  <div class="position-relative">
    <input
      v-model="model"
      type="text"
      class="form-control"
      placeholder="Search suburb"
      @keyup.enter="chooseSuggestion(model)"
    />

    <div class="list-group position-absolute w-100 mt-1 shadow-sm" style="z-index: 9999;" v-if="suggestions.length > 0">
      <button
        v-for="item in suggestions"
        :key="item.name"
        type="button"
        class="list-group-item list-group-item-action"
        @click="chooseSuggestion(item.name)"
      >
        {{ item.name }}
      </button>
    </div>

    <div v-else-if="loading" class="small text-muted mt-1">Searching...</div>
  </div>
</template>
