<template>
  <div>
    <label v-if="label" class="form-label">{{ label }}</label>

    <div class="row input-group form-control rounded-pill">
      <input
        type="text"
        class="col border border-0"
        :placeholder="placeholder"
        v-model="inputValue"
        @keyup.enter="handleSearch"
      />

      <button class="col-3 btn border rounded-pill mx-1" @click="handleSearch">
        Search
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
  label: {
    type: String,
    default: '',
  },
  placeholder: {
    type: String,
    default: 'Search suburb or LGA...',
  },
})

const emit = defineEmits(['update:modelValue', 'search'])

const inputValue = ref(props.modelValue)

watch(inputValue, (val) => {
  emit('update:modelValue', val)
})

watch(
  () => props.modelValue,
  (newVal) => {
    inputValue.value = newVal
  }
)

function handleSearch() {
  emit('search', inputValue.value)
  inputValue.value = ''
}
</script>
