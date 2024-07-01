<script setup lang="ts">
const emit = defineEmits(["cancel"]);
const props = defineProps({
  offset: {
    type: Boolean,
    default: true
  },
  submitBtn: {
    type: String,
    default: "Принять",
  },
  resetBtn: {
    type: String,
    default: "Очистить",
  },
  cancelBtn: {
    type: String,
    default: "Отмена",
  }
})
</script>

<template>
  <div class="row mb-3">
    <div :class="{'offset-lg-2 col-lg-10' : props.offset}">
      <div class="btn-group" role="group">
        <button
          class="btn btn-md btn-outline-primary"
          name="submit"
          type="submit"
        >
          {{ props.submitBtn }}
        </button>
        <button 
          class="btn btn-md btn-outline-danger"
          name="reset" 
          type="reset"
        >
          {{ props.resetBtn }}
        </button>
        <button 
          class="btn btn-md btn-outline-secondary"
          name="cancel" 
          type="button"
          @click="$emit('cancel')"
        >
          {{ props.cancelBtn }}
        </button>
      </div>
    </div>
  </div>
</template>