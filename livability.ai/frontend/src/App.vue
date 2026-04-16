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
  <div class="app-shell">
    <header class="site-header py-3">
      <div class="container position-relative">
        <RouterLink to="/" class="logo-left text-decoration-none">
          <img :src="getLogo()" alt="Livability.ai logo" />
        </RouterLink>

        <div class="header-card mx-auto">
          <nav class="main-nav">
            <RouterLink to="/" class="nav-link-custom">Home</RouterLink>
            <RouterLink to="/SuburbSearch" class="nav-link-custom">Suburb Search</RouterLink>
            <RouterLink to="/FindYourMatch" class="nav-link-custom">Find Your Match</RouterLink>
            <RouterLink to="/CompareSuburbs" class="nav-link-custom">Compare Suburbs</RouterLink>
          </nav>
        </div>
      </div>
    </header>

    <main>
      <RouterView :selectedSuburb="selectedSuburb" :setSelectedSuburb="setSelectedSuburb" />
    </main>

    <footer class="site-footer container text-center py-4 mt-5">
      <p class="mb-3 footer-text">
        Median rent statistics sourced from Victoria Government Department of Families, Fairness and Housing
        Rental Report, which is updated quarterly.
        Crime statistics sourced from the Crime Statistics Agency latest Victorian crime data for offence count which is
        updated quarterly, with population rate calculated based on suburb population data from Australian Bureau of
        Statistics 2021 Census. Crime statistics should be used as a general indicator only and do not directly equate to
        safety.
        Public transport statistics are sourced from the Transport Victoria public transport lines and stops data, with
        suburb boundaries provided by the Australian Bureau of Statistics Australian Statistical Geography Standard (ASGS)
        Edition 3.
      </p>
      <p class="mb-0 footer-copy">&copy; 2026 Livability.ai. All rights reserved.</p>
    </footer>
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
}

.site-header {
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(12px);
}

.logo-left {
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  z-index: 2;
}

.logo-left img {
  width: 160px; /* bigger logo */
  height: auto;
  object-fit: contain;

  transform: translateY(-10px); /* lift it slightly */
  transition: transform 0.2s ease;
}

.logo-left:hover img {
  transform: scale(1.05);
}

.header-card {
  max-width: 720px;
  display: flex;
  justify-content: center;
  padding: 0.85rem 1.2rem;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid #d1d5db;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
}

.main-nav {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.nav-link-custom {
  text-decoration: none;
  color: #4b5563;
  font-weight: 600;
  padding: 0.65rem 1rem;
  border-radius: 999px;
  transition: all 0.2s ease;
}

.nav-link-custom:hover {
  background: #f3f4f6;
  color: #111827;
}

.nav-link-custom.router-link-exact-active {
  background: #111827;
  color: #ffffff;
  box-shadow: 0 6px 16px rgba(17, 24, 39, 0.18);
}

.site-footer {
  max-width: 1100px;
}

.footer-text {
  color: #6b7280;
  line-height: 1.7;
  font-size: 0.95rem;
}

.footer-copy {
  color: #4b5563;
  font-weight: 600;
}

@media (prefers-color-scheme: dark) {
  .header-card {
    background: rgba(30, 41, 59, 0.9);
    border-color: #334155;
    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.28);
  }

  .nav-link-custom {
    color: #cbd5e1;
  }

  .nav-link-custom:hover {
    background: #334155;
    color: #f8fafc;
  }

  .nav-link-custom.router-link-exact-active {
    background: #e2e8f0;
    color: #0f172a;
    box-shadow: none;
  }

  .footer-text {
    color: #94a3b8;
  }

  .footer-copy {
    color: #e2e8f0;
  }
}

@media (max-width: 768px) {
  .logo-left {
    position: static;
    transform: none;
    display: flex;
    justify-content: center;
    margin-bottom: 1rem;
  }

  .logo-left img {
    width: 90px;
  }

  .header-card {
    margin-top: 0.5rem;
    padding: 1rem;
    border-radius: 18px;
  }

  .main-nav {
    gap: 0.4rem;
  }

  .nav-link-custom {
    padding: 0.55rem 0.85rem;
    font-size: 0.95rem;
  }
}
</style>
