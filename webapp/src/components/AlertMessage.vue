<template>
  <div class="alert alert-dismissible" :class="attr" role="info">{{text}}
    <button class="btn-close" type="button" data-bs-dismiss="alert"></button>
  </div>
</template>

<script setup lang="ts">

const props = defineProps({
  attr: String,
  text: String
});

</script>