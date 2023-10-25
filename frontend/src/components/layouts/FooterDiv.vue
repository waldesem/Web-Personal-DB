<script setup lang="ts">

import { server } from '@share/utilities';
import { profileStore } from '@/store/profile';

const storeProfile = profileStore();

</script>

<template>
  <div v-if="!storeProfile.printPdf" class="container py-5">
    <footer class="d-flex justify-content-around py-3 my-4 border-top">
      <a :href="`${server}/docs`" target=”_blank” title="OpenAPI">
        <i class="bi bi-book-half"> OpenAPI</i>
      </a>
      &nbsp;
      <a href="https://github.com/waldesem/Web-Personal-DB" target=”_blank” title="Github">
        <i class="bi bi-github">  Github</i>
      </a>
    </footer>
  </div>
</template>