<template>
  <div class="home-screen">
    <div class="container py-5">
      <div class="mx-auto content-wrap">
        <section class="hero-section text-center mb-5">
          <div class="hero-badge mb-3">Livability.AI</div>

          <h1 class="hero-title mb-3">Find your ideal Melbourne suburb</h1>

          <p class="hero-text mx-auto mb-0">
            Everyone deserves a home that is safe, affordable, and well connected.
            Livability.ai brings together suburb data on rent, crime, and public
            transport in one place, so Melbourne renters can discover suburbs that
            truly match their needs.
          </p>
        </section>

        <section class="mb-5">
          <h3 class="section-title text-center mb-4">What we measure</h3>

          <div class="row g-4">
            <div class="col-md-4">
              <div class="info-card h-100 text-center">
                <div class="icon-wrap mb-3">💰</div>
                <h4 class="card-title">Rent</h4>
                <p class="card-text mb-0">
                  Median rent by suburb, property type, and number of bedrooms.
                </p>
              </div>
            </div>

            <div class="col-md-4">
              <div class="info-card h-100 text-center">
                <div class="icon-wrap mb-3">🛡️</div>
                <h4 class="card-title">Crime</h4>
                <p class="card-text mb-0">
                  Crime offence rate per 1,000 people to help compare suburb safety.
                </p>
              </div>
            </div>

            <div class="col-md-4">
              <div class="info-card h-100 text-center">
                <div class="icon-wrap mb-3">🚉</div>
                <h4 class="card-title">Public Transport</h4>
                <p class="card-text mb-0">
                  Transport stops by type plus an accessibility score for convenience.
                </p>
              </div>
            </div>
          </div>
        </section>

        <section>
          <h3 class="section-title text-center mb-4">Ways to explore</h3>

          <div class="row g-4">
            <div class="col-md-4">
              <RouterLink to="/SuburbSearch" class="explore-card text-decoration-none h-100">
                <div class="explore-icon mb-3">🔍</div>
                <h4 class="explore-title">Suburb Search</h4>
                <p class="explore-text mb-0">
                  Search for a suburb and view its rent, crime, and transport profile.
                </p>
              </RouterLink>
            </div>

            <div class="col-md-4">
              <RouterLink to="/FindYourMatch" class="explore-card text-decoration-none h-100">
                <div class="explore-icon mb-3">✨</div>
                <h4 class="explore-title">Find Your Match</h4>
                <p class="explore-text mb-0">
                  Get suburb recommendations based on your budget and priorities.
                </p>
              </RouterLink>
            </div>

            <div class="col-md-4">
              <RouterLink to="/CompareSuburbs" class="explore-card text-decoration-none h-100">
                <div class="explore-icon mb-3">📊</div>
                <h4 class="explore-title">Suburb Comparison</h4>
                <p class="explore-text mb-0">
                  Compare suburbs side by side to see which one suits you best.
                </p>
              </RouterLink>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// No script needed for now
</script>

<style scoped>
.home-screen {
  min-height: 100vh;
  background: linear-gradient(180deg, #f8fafc 0%, #eef2f7 100%);
}

.content-wrap {
  max-width: 980px;
}

.hero-section {
  padding: 2rem 1rem 1rem;
}

.hero-badge {
  display: inline-block;
  padding: 0.45rem 0.9rem;
  border-radius: 999px;
  background: #111827;
  color: #ffffff;
  font-size: 0.9rem;
  font-weight: 600;
  letter-spacing: 0.02em;
}

.hero-title {
  font-size: 2.3rem;
  font-weight: 800;
  color: #111827;
  line-height: 1.2;
}

.hero-text {
  max-width: 720px;
  font-size: 1.1rem;
  line-height: 1.8;
  color: #374151;
}

.section-title {
  font-size: 1.6rem;
  font-weight: 700;
  color: #111827;
}

.info-card,
.explore-card {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #d1d5db;
  border-radius: 18px;
  padding: 1.75rem 1.5rem;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.info-card:hover,
.explore-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 14px 32px rgba(15, 23, 42, 0.1);
  border-color: #9ca3af;
}

.icon-wrap,
.explore-icon {
  width: 58px;
  height: 58px;
  margin: 0 auto;
  border-radius: 16px;
  display: grid;
  place-items: center;
  font-size: 1.7rem;
  background: #f3f4f6;
}

.card-title,
.explore-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 0.8rem;
  color: #111827;
}

.card-text,
.explore-text {
  font-size: 1rem;
  line-height: 1.7;
  color: #4b5563;
}

.explore-card {
  display: block;
  height: 100%;
  text-align: center;
}

@media (prefers-color-scheme: dark) {
  .home-screen {
    background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
  }

  .hero-badge {
    background: #e5e7eb;
    color: #111827;
  }

  .hero-title {
    color: #f8fafc;
  }

  .hero-text {
    color: #cbd5e1;
  }

  .section-title {
    color: #f8fafc;
  }

  .info-card,
  .explore-card {
    background: rgba(30, 41, 59, 0.9);
    border: 1px solid #334155;
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.25);
  }

  .info-card:hover,
  .explore-card:hover {
    border-color: #64748b;
    box-shadow: 0 16px 34px rgba(0, 0, 0, 0.3);
  }

  .icon-wrap,
  .explore-icon {
    background: #334155;
  }

  .card-title,
  .explore-title {
    color: #f8fafc;
  }

  .card-text,
  .explore-text {
    color: #cbd5e1;
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 1.8rem;
  }

  .hero-text {
    font-size: 1rem;
  }

  .section-title {
    font-size: 1.35rem;
  }
}
</style>
