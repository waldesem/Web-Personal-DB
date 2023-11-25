<script setup lang="ts">

const props = defineProps({
  slotOne: {
    type: Boolean,
    default: false
  },
  slotTwo: {
    type: Boolean,
    default: false
  },
  label: {
    type: String,
    default: ''
  },
  value: {
    type: String,
    default: ''
  },
  print: {
    type: Boolean,
    default: false
  }
});

</script>

<template>
  <div class="row" :class="{'d-print-none': props.print}">
    <div class="col-md-4">{{props.label}}  
      <slot v-if="slotOne" name="divOne"></slot>
    </div>
    <div class="col-md-8">{{props.value}}
      <slot v-if="slotTwo" name="divTwo"></slot>
    </div>
  </div>
</template>