<script setup lang="ts">
import type { NavigationMenuItem } from "@nuxt/ui";

// Объявляем переменную для получения данных пользователя
const userState = useStateUser();

// Объявляем функцию для выхода из системы и очистки данных пользователя
async function logout() {
  if (!confirm("Вы действительно хотите выйти?")) return;
  const token = useCookie("token");
  const refresh = useCookie("refresh");
  await $fetch("/routes/auth/logout", {
    method: "POST",
    body: {
      access_token: token.value,
      refresh_token: refresh.value,
    },
  });
  token.value = null;
  refresh.value = null;
  clearNuxtData();
  return navigateTo("/login");
}

// Объявляем массив для хранения элементов меню
const items = ref<NavigationMenuItem[]>([
  {
    label: "Пользователи",
    icon: "i-lucide-users",
    to: "/users",
    disabled: userState.value.role !== "admin",
  },
  {
    label: "Кандидаты",
    icon: "i-lucide-users-round",
    to: "/persons",
  },
]);
</script>

<template>
  <!-- Контейнер для отображения контента -->
  <UContainer>
    <div
      class="flex items-center justify-between sticky top-0 z-50 bg-white pt-8 pb-16"
    >
      <!-- Ссылка на главную страницу -->
      <NuxtLink to="/persons" title="На главную страницу">
        <div class="flex inline-flex items-center text-xl font-bold space-x-1">
          <h3 class="text-blue-600">STAFFSEC</h3>
          <h3 class="text-red-600">ФИНТЕХ</h3>
        </div>
      </NuxtLink>
      <!-- Меню навигации -->
      <div class="flex items-center space-x-4">
        <UNavigationMenu
          highlight
          :items="items"
          class="w-full justify-center"
        />
      </div>
      <!-- Кнопка выхода из системы -->
      <UButton
        class="rounded-full"
        :label="userState.username"
        color="error"
        icon="i-lucide-log-out"
        title="Выход"
        @click="logout()"
      />
    </div>
    <!-- Содержимое страницы -->
    <div class="flex flex-col gap-4 px-1 mb-6">
      <slot />
    </div>
  </UContainer>
</template>
