<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import logoLight from '@/assets/logo.svg'
import logoDark from '@/assets/logo-dark.svg'

const selectedSuburb = ref('')

function setSelectedSuburb(name: string) {
  selectedSuburb.value = name
}

function getLogo() {
  return window.matchMedia('(prefers-color-scheme: dark)').matches
    ? logoDark
    : logoLight
}
</script>

<template>
  <header>
    <div class="container">
      <div class="row align-items-start livability-logo">
        <img alt="livability logo" class="logo col-6 mx-auto" :src="getLogo()" width="125" height="125" />

        <div class="row col-6 my-auto mx-auto">
          <nav class="d-flex justify-content-center">
            <div>
              <RouterLink class="translate-middle" to="/">Home</RouterLink>
            </div>
            <div>
              <RouterLink class="translate-middle" to="/SuburbSearch">Suburb Search</RouterLink>
            </div>
            <div>
              <RouterLink class="translate-middle" to="/FindYourMatch">Find your match</RouterLink>
            </div>
            <div>
              <RouterLink class="translate-middle" to="/CompareSuburbs">Compare suburbs</RouterLink>
            </div>
          </nav>
        </div>
      </div>
    </div>
  </header>

  <RouterView :selectedSuburb="selectedSuburb" :setSelectedSuburb="setSelectedSuburb" />

  <footer class="container text-center py-4 mt-5">
    <p class="mb-0">Median rent statistics sourced from Victoria Government Department of Families, Fairness and Housing
      Rental Report, which is updated quarterly.
      Crime statistics sourced from the Crime Statistics Agency latest Victorian crime data for offence count which is
      updated quarterly, with population rate calculated based on suburb population data from Australian Bureau of
      Statistics 2021 Census. Crime statistics should be used as a general indicator only and do not directly equate to
      safety.
      Public transport statistics are sourced from the Transport Victoria public transport lines and stops data, with
      suburb boundaries provided by the Australian Bureau of Statistics Australian Statistical Geography Standard (ASGS)
      Edition 3.
    </p>
    <p class="mb-0">&copy; 2026 Livability.ai. All rights reserved.</p>
  </footer>
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
