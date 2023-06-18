<template>
  <div class="py-3">
    <div class="alert alert-dismissible" :class="attr" role="info">{{text}}
      <button class="btn-close" type="button" data-bs-dismiss="alert"></button>
    </div>
  </div>
</template>

<script setup lang="ts">

import { defineProps, toRefs } from "vue";

const props = defineProps({
  attr: String,
  text: String
});

const { attr, text } = toRefs(props);

</script>