<script setup lang="ts">
import { useDocumentVisibility, watchThrottled } from "@vueuse/core";
import type { Session } from "@/types";

const { $api } = useNuxtApp();
const visibility = useDocumentVisibility();

watchThrottled(
  visibility,
  async () => {
    try {
      userState.value = await $api<Session>("/routes/auth/session");
    } catch (error) {
      console.error(error);
    }
  },
  { immediate: true, throttle: 600000 }
);

// Объявляем функцию для выхода из системы и очистки данных пользователя
function logout() {
  if (!confirm("Вы действительно хотите выйти?")) return;
  useCookie("token").value = null;
  useCookie("refresh").value = null;
  userState.value = null;
  clearNuxtData();
  return navigateTo("/login");
}
</script>

<template>
  <UPage>
    <UHeader to="/persons" class="no-print">
      <template #title>
        <ElementsLogoDiv />
      </template>
      <template #default>
        <ClientOnly>
          <UNavigationMenu
            v-if="userState.role === 'admin'"
            :items="[
              {
                label: 'Пользователи',
                icon: 'i-lucide-users',
                to: '/users',
                disabled: userState.role !== 'admin',
              },
            ]"
            variant="link"
          />
        </ClientOnly>
      </template>
      <template #right>
        <ClientOnly>
          <UButton
            class="rounded-full"
            :label="userState.username ?? ''"
            :disabled="!userState.username"
            color="error"
            icon="i-lucide-log-out"
            @click="logout()"
          />
        </ClientOnly>
      </template>
    </UHeader>
    <UMain>
      <UContainer class="pt-16">
        <slot />
      </UContainer>
    </UMain>

    <USeparator type="dashed" class="h-px no-print" />

    <UFooter class="no-print">
      <template #left>
        <p class="text-sm">Copyright © {{ new Date().getFullYear() }}</p>
      </template>

      <template #right>
        <UButton
          icon="i-lucide-git-graph"
          label="GitHub"
          color="neutral"
          variant="ghost"
          to="https://github.com/waldesem/Web-Personal-DB"
          target="_blank"
        />
      </template>
    </UFooter>
  </UPage>
</template>
