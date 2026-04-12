<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, RouterView, useRouter } from 'vue-router'
import SearchBar from './components/SearchBar.vue'

const router = useRouter()

const search = ref('')
const selectedSuburb = ref('')

function formatSuburbName(input: string) {
  return input
    .trim()
    .replace(/\s+/g, ' ')
    .toLowerCase()
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

function setSelectedSuburb(suburbName: string) {
  const cleaned = formatSuburbName(suburbName)
  if (!cleaned) return

  search.value = cleaned
  selectedSuburb.value = cleaned
}

async function runSearch(suburbName: string) {
  setSelectedSuburb(suburbName)

  if (router.currentRoute.value.path !== '/') {
    await router.push('/')
  }
}

function getLogo() {
  if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
    return "src/assets/logo-dark.svg"
  } else {
    return "src/assets/logo.svg"
  }
}
</script>

<template>
  <header>
    <!--<div class="container">-->
    <div class="row align-items-start livability-logo">
      <img alt="livability logo" class="logo col-3 mx-auto" :src="getLogo()" width="125" height="125" />

      <div class="row col-6 my-auto mx-auto">
        <nav class="d-flex justify-content-center">
          <div>
            <RouterLink class="translate-middle" to="/Dashboard">Dashboard</RouterLink>
          </div>
          <div>
            <RouterLink class="translate-middle" to="/FindYourMatch">Find your match</RouterLink>
          </div>
          <div>
            <RouterLink class="translate-middle" to="/History">History</RouterLink>
          </div>
          <div>
            <RouterLink class="translate-middle" to="/about">About</RouterLink>
          </div>

        </nav>
      </div>

      <div class="col-2 my-auto mx-auto">
        <SearchBar v-model="search" @search="runSearch" />
      </div>
    </div>
    <!--</div>-->
  </header>

  <RouterView :selectedSuburb="selectedSuburb" :setSelectedSuburb="setSelectedSuburb" />
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
