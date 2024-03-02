<script setup lang="ts">
import { defineAsyncComponent } from 'vue';

const NavBar = defineAsyncComponent(
  () => import("@components/layouts/NavBar.vue")
);
const MessageDiv = defineAsyncComponent(
  () => import('../divs/MessageDiv.vue')
)
const props = defineProps(["fullName"])
</script>

<template>

  <NavBar 
    :arg="'bg-primary'"
    :brand="'STAFFSEC'"
    :full-name="props.fullName"
  >
  <template v-slot:navbar>
    <li class="nav-item">
      <router-link
        :to="{ name: 'persons' }"
        class="nav-link active"
      >
        Кандидаты
      </router-link>
    </li>
    <li class="nav-item">
      <router-link
        :to="{ name: 'resume' }"
        class="nav-link active"
      >
        Создать
      </router-link>
    </li>
    <li class="nav-item">
      <router-link
        :to="{ name: 'information' }"
        class="nav-link active"
      >
        Информация
      </router-link>
    </li>
    <li class="nav-item">
      <router-link
        :to="{ name: 'contacts' }"
        class="nav-link active"
      >
        Контакты
      </router-link>
    </li>
    <li class="nav-item">
      <router-link
        :to="{ name: 'manager' }"
        class="nav-link active"
        href="#"
      >
        Файлы
      </router-link>
    </li>
    <MessageDiv />
  </template>
  </NavBar>
</template>