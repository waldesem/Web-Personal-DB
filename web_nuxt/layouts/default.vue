<script setup lang="ts">
import type { NavigationMenuItem } from "@nuxt/ui";

const userState = useUserState();

const { $customFetch } = useNuxtApp();

function logout() {
  if (!confirm("Вы действительно хотите выйти?")) return;
  $customFetch("/route/auth/logout") as Record<string, string>;
  accessToken.value = null;
  clearNuxtData();
  return navigateTo("/login");
}

const items = ref<NavigationMenuItem[]>([
  {
    label: "Пользователи",
    icon: "i-lucide-users",
    to: "/users",
  },
  {
    label: "Кандидаты",
    icon: "i-lucide-users-round",
    to: "/persons",
  },
  {
    label: "Исходный код",
    icon: "i-lucide-code",
    to: "https://github.com/waldesem/Web-Personal-DB",
    target: "_blank",
  },
]);
</script>

<template>
  <UContainer>
    <div
      class="flex items-center justify-between sticky top-0 z-50 bg-white pt-8 pb-16"
    >
      <NuxtLink to="/persons" title="На главную страницу">
        <div class="flex inline-flex items-center text-xl font-bold space-x-1">
          <h3 class="text-blue-600">STAFFSEC</h3>
          <h3 class="text-red-600">ФИНТЕХ</h3>
        </div>
      </NuxtLink>
      <div class="flex items-center space-x-4">
        <UNavigationMenu
          highlight
          :items="userState.role === 'admin' ? items : items.slice(1)"
          class="w-full justify-center"
        />
      </div>
      <UButton
        class="rounded-full"
        :label="userState.username"
        color="error"
        icon="i-lucide-log-out"
        title="Выход"
        @click="logout()"
      />
    </div>
    <div class="flex flex-col gap-4 px-1 mb-6">
      <slot />
    </div>
  </UContainer>
</template>
