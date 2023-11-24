<script setup lang="ts">

const props = defineProps({
  id: String,
  idx: Number,
  label: String,
});

</script>


<template>
  <a class="btn btn-primary" data-bs-toggle="collapse" :href="`#${props.id}`">
    {{props.label}}
  </a>
  <div class="collapse" :class="idx===0 ? 'show' : ''" :id="`${props.id}`">
    <div class="card card-body">
      <slot></slot>
    </div>
  </div>
</template>
