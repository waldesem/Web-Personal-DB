<script setup lang="ts">
import { defineAsyncComponent } from 'vue';

const NavBar = defineAsyncComponent(
  () => import("@components/layouts/NavBar.vue")
);

const props = defineProps({
  fullName: String,
  userLogout: {
    type: Function,
    required: true,
  }
});
</script>

<template>
  <NavBar 
    :arg="'bg-secondary'"
    :brand="'ADMIN'"
    :full-name="props.fullName"
    :log-out="props.userLogout"
  >
    <template v-slot:navbar>
      <li class="nav-item">
        <router-link
          :to="{ name: 'users', params: { group: 'admins' } }"
          class="nav-link active"
          href="#"
        >
          Пользователи
        </router-link>
      </li>

      <li class="nav-item">
        <router-link
          :to="{ name: 'table', params: { group: 'admins' } }"
          class="nav-link active"
          href="#"
        >
          Таблицы
        </router-link>
      </li>
    </template>
  </NavBar>
</template>
