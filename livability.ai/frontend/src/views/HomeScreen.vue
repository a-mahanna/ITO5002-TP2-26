<template>
  <div class="home-screen">
    <div class="container py-5">
      <div class="mx-auto content-wrap">
        <h1 class="brand-title mb-3">Livability.ai</h1>

        <h2 class="hero-title mb-3">Find your ideal Melbourne suburb</h2>

        <p class="hero-text mb-5">
          Everyone deserves a home that is safe, affordable and well connected.
          Livability.ai brings together suburb data on rent, crime and public
          transport in one place, so Melbourne renters can find the suburb that
          works for them.
        </p>

        <section class="mb-5">
          <h3 class="section-title mb-4">What we measure</h3>

          <div class="row g-4">
            <div class="col-md-4">
              <div class="info-card h-100">
                <h4 class="card-title">Rent</h4>
                <p class="card-text mb-0">
                  Median rent per suburb by property type and number of bedrooms
                </p>
              </div>
            </div>

            <div class="col-md-4">
              <div class="info-card h-100">
                <h4 class="card-title">Crime</h4>
                <p class="card-text mb-0">
                  Crime offence rate per suburb
                </p>
              </div>
            </div>

            <div class="col-md-4">
              <div class="info-card h-100">
                <h4 class="card-title">Public transport</h4>
                <p class="card-text mb-0">
                  Public transport stops per suburb by transport type and accessibility score
                </p>
              </div>
            </div>
          </div>
        </section>

        <section>
          <h3 class="section-title mb-4">Ways to explore</h3>

          <div class="d-grid gap-3">
            <RouterLink to="/SuburbSearch" class="explore-card text-decoration-none">
              <div>
                <h4 class="explore-title">Suburb search</h4>
                <p class="explore-text mb-0">Search characteristics by suburb</p>
              </div>
            </RouterLink>

            <RouterLink to="/FindYourMatch" class="explore-card text-decoration-none">
              <div>
                <h4 class="explore-title">Find your match</h4>
                <p class="explore-text mb-0">Find suburbs that match your preferences</p>
              </div>
            </RouterLink>

            <RouterLink to="/Dashboard" class="explore-card text-decoration-none">
              <div>
                <h4 class="explore-title">Suburb comparison</h4>
                <p class="explore-text mb-0">Compare suburbs side by side</p>
              </div>
            </RouterLink>
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
  background: #f5f5f5;
}

.content-wrap {
  max-width: 900px;
}

.brand-title {
  font-size: 2.2rem;
  font-weight: 700;
  color: #111;
}

.hero-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111;
}

.hero-text {
  max-width: 760px;
  font-size: 1.05rem;
  line-height: 1.7;
  color: #333;
}

.section-title {
  font-size: 1.4rem;
  font-weight: 700;
  color: #111;
}

.info-card {
  background: white;
  border: 1px solid #222;
  padding: 1.5rem;
  min-height: 180px;
}

.card-title {
  font-size: 1.3rem;
  font-weight: 400;
  margin-bottom: 1rem;
  color: #111;
}

.card-text {
  font-size: 1rem;
  line-height: 1.7;
  color: #333;
}

.explore-card {
  display: block;
  background: white;
  border: 1px solid #222;
  padding: 1.5rem;
  transition: all 0.2s ease;
}

.explore-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
}

.explore-title {
  font-size: 1.35rem;
  font-weight: 400;
  margin-bottom: 1rem;
  color: #111;
}

.explore-text {
  font-size: 1rem;
  line-height: 1.6;
  color: #333;
}

@media (max-width: 768px) {
  .brand-title {
    font-size: 1.8rem;
  }

  .hero-title {
    font-size: 1.25rem;
  }

  .info-card {
    min-height: auto;
  }
}
</style>
