<script setup lang="ts">
</script>
<template>
  <div class="d-print-none bg-primary-light text-white">
    <ul class="list-group list-group-flush">
      <li class="list-group-item list-group-item-action">
        <router-link
          :to="{ name: 'persons' }"
          class="link-opacity-50-hover"
        >
          Кандидаты
        </router-link>
      </li>
      <li class="list-group-item list-group-item-action">
        <router-link
          :to="{ name: 'resume' }"
          class="link-opacity-50-hover"
        >
          Создать
        </router-link>
      </li>
      <li class="list-group-item list-group-item-action">
        <router-link
          :to="{ name: 'information' }"
          class="link-opacity-50-hover"
        >
          Информация
        </router-link>
      </li>
      <li class="list-group-item list-group-item-action">
        <router-link
          :to="{ name: 'contacts' }"
          class="link-opacity-50-hover"
        >
          Контакты
        </router-link>
      </li>
      <li><hr class="dropdown-divider"></li>
      <li class="list-group-item list-group-item-action">
        <a 
          href="http://github.com/waldesem" 
          target="_blank" 
          class="link-opacity-50-hover"
        >
          github
        </a>
      </li>
    </ul>
  </div>
</template>