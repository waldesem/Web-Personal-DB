<script setup lang="ts">

import { ref } from 'vue';

const props = defineProps({
  id: String,
  idx: Number
});

const toggle = ref(true);

</script>


<template>
  <a class="link-primary" role="button" data-bs-toggle="collapse" :href="`#${props.id}`"
     @click="toggle = !toggle">
    <i class="bi" :class="toggle ? 'bi-plus-circle' : 'bi-dash-circle'"></i>
      {{'ID #' + props.id}}
  </a>
  <div class="collapse" :class="{'show': props.idx == 0}" :id="props.id">
    <div class="card card-body">
      <slot></slot>
    </div>
  </div>
</template>
