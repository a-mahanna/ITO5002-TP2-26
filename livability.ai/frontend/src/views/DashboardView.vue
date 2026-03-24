<script setup lang="ts">
import MapView from '../components/MapView.vue'
import { watch, ref } from 'vue'


</script>

<template>
  <div class="container">
    <div class="row justify-content-center border border-light-subtle">
      <div class="col-9">
        <!--map--> <MapView />
      </div>
      <div class="col-3 border border-light-subtle">
          <!--side bar-->
          side bar
      </div>
    </div>

  </div>
</template>

<style scoped></style>
