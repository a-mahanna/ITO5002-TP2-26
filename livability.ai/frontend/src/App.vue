<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import SearchBar from './components/SearchBar.vue'

const search = ref('')
const selectedSuburb = ref('')
const selectedInfo = ref('')


function formatSuburbName(input: string) {
  return input
    .trim()
    .toLowerCase()
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

function runSearch(suburbName: string, info?: string | null) {
  const cleaned = formatSuburbName(suburbName)
  if (!cleaned) return

  search.value = cleaned
  selectedSuburb.value = cleaned
  selectedInfo.value = info || ''
}
</script>

<template>
  <header>
    <div class="container">
      <div class="row border border-light-subtle align-items-start">
        <img alt="livability logo" class="logo col-4 my-auto" src="@/assets/logo.svg" width="125" height="125" />
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
  :setSelectedSuburb="runSearch"
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
