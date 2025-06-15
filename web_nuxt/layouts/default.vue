<script setup lang="ts">
import type { NavigationMenuItem } from '@nuxt/ui'

const userState = useUserState();

// async function logout() {
//   if (!confirm("Вы действительно хотите выйти?")) return;
//   accessToken.value = null;
//   clearNuxtData();
//   return navigateTo("/login");
// }

const items = ref<NavigationMenuItem[]>([
  {
    label: 'Кандидаты',
    icon: 'i-heroicons-user-group',
    to: '/persons',
    active: true,
  },
  {
    label: 'Пользователи',
    icon: 'i-heroicons-users',
    to: '/users',
    disabled: !userState.role == 'admin',
  },
  {
    label: 'Справочник',
    icon: 'i-heroicons-phone-arrow-up-right-solid',
    to: '/phones',
    target: '_blank',
  },
  {
    label: 'GitHub',
    icon: 'i-simple-icons-github',
    to: 'https://github.com/waldesem/Web-Personal-DB',
    target: '_blank',
  },
  {
    label: userState.username,
    icon: 'i-heroicons-arrow-left-end-on-rectangle',
    disabled: true,
    to: '/login',
  }
])
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
        <UNavigationMenu :items="items" class="w-full justify-center" />
        <!-- <UButton
          v-if="userState.role == 'admin'"
          class="rounded-full"
          icon="i-heroicons-users"
          color="warning"
          to="/users"
          label="Пользователи"
        />
        <UButton
          class="rounded-full"
          icon="i-heroicons-phone-arrow-up-right-solid"
          to="/phones"
          label="Справочник"
        />
        <UButton
          class="rounded-full"
          :label="userState.username"
          color="error"
          icon="i-heroicons-arrow-left-end-on-rectangle"
          title="Выход"
          @click="logout()"
        /> -->
      </div>
    </div>
    <div class="flex flex-col gap-4 px-1 mb-6">
      <slot />
    </div>
  </UContainer>
</template>
