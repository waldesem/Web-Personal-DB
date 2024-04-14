<script setup lang="ts"></script>
<template>
  <div class="navbar navbar-expand fs-5">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">STAFFSEC - MTS Bank</a>
      <div class="nav flex-column">
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
  </div>
</template>