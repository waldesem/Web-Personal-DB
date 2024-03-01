<script setup lang="ts">
import { defineAsyncComponent } from 'vue';

const NavBar = defineAsyncComponent(
  () => import("@components/layouts/NavBar.vue")
);
const MessageDiv = defineAsyncComponent(
  () => import('../divs/MessageDiv.vue')
)
</script>

<template>
  <MessageDiv />
  <NavBar 
    :arg="'bg-primary'"
    :brand="'STAFFSEC'"
  >
  <template v-slot:navbar>
    <li class="nav-item">
      <router-link
        :to="{ name: 'persons', params: { group: 'staffsec' } }"
        class="nav-link active"
      >
        Кандидаты
      </router-link>
    </li>
    <li class="nav-item">
      <router-link
        :to="{ name: 'resume', params: { group: 'staffsec' } }"
        class="nav-link active"
      >
        Создать
      </router-link>
    </li>
    <li class="nav-item">
      <router-link
        :to="{ name: 'information', params: { group: 'staffsec' } }"
        class="nav-link active"
      >
        Информация
      </router-link>
    </li>
    <li class="nav-item">
      <router-link
        :to="{ name: 'contacts', params: { group: 'staffsec' } }"
        class="nav-link active"
      >
        Контакты
      </router-link>
    </li>
    <li class="nav-item">
      <router-link
        :to="{ name: 'manager', params: { group: 'staffsec' } }"
        class="nav-link active"
        href="#"
      >
        Файлы
      </router-link>
    </li>
  </template>
  </NavBar>
</template>