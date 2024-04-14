<script setup lang="ts"></script>
<template>
  <div class="navbar navbar-expand sticky-top fs-5 d-print-none p-3">
    <div class="nav flex-column">
      <a class="nav-link text-info fs-3 fw-bold">STAFFSEC - MTS Bank</a>
      <hr class="text-info">
      <router-link
        :to="{ name: 'persons' }"
        class="nav-link active"
      >
        Кандидаты
      </router-link>
      <hr class="text-info">
      <router-link
        :to="{ name: 'resume' }"
        class="nav-link active"
      >
        Создать
      </router-link>
      <hr class="text-info">
      <router-link
        :to="{ name: 'information' }"
        class="nav-link active"
      >
        Информация
      </router-link>
      <hr class="text-info">
      <router-link
        :to="{ name: 'contacts' }"
        class="nav-link active"
      >
        Контакты
      </router-link>
      <hr class="text-info">
      <router-link
        :to="{ name: 'gpt' }"
        class="nav-link active"
      >
        PrivateGPT
      </router-link>
    </div>
  </div>
</template>