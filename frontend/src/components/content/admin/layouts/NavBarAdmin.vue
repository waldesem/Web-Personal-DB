<script setup lang="ts">
import { defineAsyncComponent } from 'vue';

const NavBar = defineAsyncComponent(
  () => import("@components/layouts/NavBar.vue")
);
</script>

<template>
  <NavBar 
    :arg="'bg-secondary'"
    :brand="'ADMIN'"
  >
    <template v-slot:navbar>
      <li class="nav-item">
        <router-link
          :to="{ name: 'users' }"
          class="nav-link active"
          href="#"
        >
          Пользователи
        </router-link>
      </li>
    </template>
  </NavBar>
</template>
