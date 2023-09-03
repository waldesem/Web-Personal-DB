<script setup lang="ts">
/* Компонент NavBarAdmin - выводит навигационную панель в шапке сайта для администратора.
Содержит ссылки на страницы: Пользователи, Регионы */
</script>

<template>
    <div class="container-fluid">
    <nav class="navbar navbar-expand navbar-nav mr-auto navbar-dark bg-secondary">
      <div class="container">
        <a class="navbar-brand" href="#">Admin-StaffSec</a>
        <div class="navbar-nav mr-auto collapse navbar-collapse" id="navbarContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">      
            <li class="nav-item">
                <router-link :to="{ name: 'users' }" class="nav-link active" href="#">Пользователи</router-link>
            </li>
          </ul>                                
        </div>
        <div class="d-flex px-2">
          <router-link :to="{name: 'login'}" class="nav-link active" data-bs-toggle="tooltip" data-bs-placement="right" title="Выход"><i class="bi bi-box-arrow-in-right"></i></router-link>
        </div>
      </div>
    </nav>
  </div>
</template>