<script setup lang="ts">
const emit = defineEmits(["cancel"]);
const props = defineProps({
  subclass: {
    type: String,
    default: "outline",
  },
  submitNeeds: {
    type: Boolean,
    default: true,
  },
  submitBtn: {
    type: String,
    default: "Принять",
  },
  resetNeeds: {
    type: Boolean,
    default: true,
  },
  resetBtn: {
    type: String,
    default: "Очистить",
  },
  cancelNeeds: {
    type: Boolean,
    default: true,
  },
  cancelBtn: {
    type: String,
    default: "Отмена",
  }
})
</script>

<template>
  <button
    v-if="props.submitNeeds"
    class="btn btn-md d-print-none"
    :class="`btn-${props.subclass}-primary`"
    name="submit"
    type="submit"
  >
    {{ props.submitBtn }}
  </button>
  <button 
    v-if="props.resetNeeds"
    class="btn btn-md d-print-none" 
    :class="`btn-${props.subclass}-danger`"
    name="reset" 
    type="reset"
  >
    {{ props.resetBtn }}
  </button>
  <button 
    v-if="props.cancelNeeds"
    class="btn btn-md d-print-none" 
    :class="`btn-${props.subclass}-secondary`"
    name="cancel" 
    type="button"
    @click="$emit('cancel')"
  >
    {{ props.cancelBtn }}
  </button>
</template>