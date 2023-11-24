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
  }
});

</script>

<template>
  <div class="row">{{props.label}}
    <div class="col-md-4">      
      <slot v-if="slotOne" name="divOne"></slot>
    </div>
    <div class="col-md-8">{{props.label}}
      <slot v-if="slotTwo" name="divTwo"></slot>
    </div>
  </div>
</template>