<template>
  <div class="alert alert-dismissible" :class="attr" role="info">{{text}}
    <button class="btn-close" type="button" data-bs-dismiss="alert"></button>
  </div>
</template>

<script setup lang="ts">

import { toRefs } from "vue";

const props = defineProps({
  attr: String,
  text: String
});

const { attr, text } = toRefs(props);

</script>