<script setup lang="ts"></script>
<template>
  <div class="navbar navbar-expand sticky-top fs-5 p-3">
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
    </div>
  </div>
</template>
