<script setup lang="ts">
import { inject } from "vue";
import { server } from "@utilities/utils";

const pageIdentity = inject("pageIdentity") as string;

const props = defineProps({
  hasAdmin: Boolean
})
</script>

<template>
  <div class="container py-5 d-print-none">
    <footer class="d-flex justify-content-around py-3 my-4 border-top">
      <a 
        :href="`${server}/docs`" 
        target="”_blank”" 
        title="OpenAPI">
          <i class="bi bi-book-half"> OpenAPI</i>
      </a>
      <router-link v-if="pageIdentity === 'admin'"
        :hidden="props.hasAdmin"
        title="StaffSec"
        :to="{name: 'persons' }"
      >
        StaffSec
      </router-link>
      <router-link v-else
        :hidden="props.hasAdmin"
        title="Admin"
        :to="{name: 'users' }"
      >
        StaffSec
      </router-link>
      <a
        href="https://github.com/waldesem/Web-Personal-DB"
        target="”_blank”"
        title="Github"
      >
        <i class="bi bi-github"> Github</i>
      </a>
    </footer>
  </div>
</template>
