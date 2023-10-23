<script setup lang="ts">

import { server } from '@share/utilities';
import { profileStore } from '@/store/profile';

const storeProfile = profileStore();

</script>

<template>
  <div v-if="!storeProfile.printPdf" class="container py-5">
    <footer class="d-flex flex-wrap justify-content-around align-items-center py-3 my-4 border-top">
      <p>
        <a :href="`${server}/docs`" target=”_blank” title="OpenAPI">
          <i class="bi bi-book-half"></i>
        </a>
      </p>
      <p>
        <a href="https://github.com/waldesem/Web-Personal-DB" target=”_blank” title="Github">
          <i class="bi bi-github"></i>
        </a>
      </p>
    </footer>
  </div>
</template>