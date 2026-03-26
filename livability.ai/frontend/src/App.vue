<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import SearchBar from './components/SearchBar.vue'
import geojsonDataUrl from './data/melbournesuburbetymologywithgeometry.geojson?url'

const search = ref('')
const selectedSuburb = ref('')
const selectedInfo = ref('')

const suburbInfoMap = ref<Record<string, string>>({})

function formatSuburbName(input: string) {
  return input
    .trim()
    .toLowerCase()
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

async function loadSuburbInfo() {
  try {
    const response = await fetch(geojsonDataUrl)
    const data = await response.json()

    const map: Record<string, string> = {}

    for (const feature of data.features ?? []) {
      const suburbName =
        feature?.properties?.LOCALITY ||
        feature?.properties?.GAZLOC ||
        ''

      const suburbInfo =
        feature?.properties?.DETAILS ||
        ''

      if (suburbName) {
        map[String(suburbName).trim().toUpperCase()] = suburbInfo.formatSuburbName()
      }
    }

    suburbInfoMap.value = map
  } catch (error) {
    console.error('Failed to load suburb info:', error)
  }
}

function setSelectedSuburb(suburbName: string, info?: string | null) {
  const cleaned = formatSuburbName(suburbName)
  if (!cleaned) return

  search.value = cleaned
  selectedSuburb.value = cleaned
  selectedInfo.value = info ?? suburbInfoMap.value[cleaned] ?? ''
}

function runSearch(suburbName: string) {
  setSelectedSuburb(suburbName)
}

onMounted(() => {
  loadSuburbInfo()
})
</script>

<template>
  <header>
    <div class="container">
      <div class="row border border-light-subtle align-items-start">
        <img
          alt="livability logo"
          class="logo col-4 my-auto"
          src="@/assets/logo.svg"
          width="125"
          height="125"
        />

        <div class="col-4 my-auto">
          <nav>
            <RouterLink to="/">Dashboard</RouterLink>
            <RouterLink to="/FindYourMatch">Find your match</RouterLink>
            <RouterLink to="/History">History</RouterLink>
            <RouterLink to="/about">About</RouterLink>
          </nav>
        </div>

        <div class="col-4 my-auto">
          <SearchBar
            v-model="search"
            @search="runSearch"
          />
        </div>
      </div>
    </div>
  </header>

  <RouterView
    :selectedSuburb="selectedSuburb"
    :selectedInfo="selectedInfo"
    :setSelectedSuburb="setSelectedSuburb"
  />
</template>

<style scoped>
nav a.router-link-exact-active {
  color: #00C2FF;
}

nav a.router-link-exact-inactive {
  color: grey;
}

nav a.router-link-exact-active:hover {
  background-color: #00C2FF;
}

nav a {
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}
</style>
