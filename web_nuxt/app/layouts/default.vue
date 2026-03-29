<script setup lang="ts">
import { useSessionStore } from "@/stores/session";

const sessionStore = useSessionStore();

const visibility = useDocumentVisibility();

const path = computed(() => window.location.origin);

await useAsyncData("session", () => sessionStore.getUser(), {
  watch: [visibility],
});

// Объявляем функцию для выхода из системы и очистки данных пользователя
async function logout() {
  if (!confirm("Вы действительно хотите выйти?")) return;
  const access = useCookie("access");
  const refresh = useCookie("refresh");
  if (access.value || refresh.value) {
    await $fetch.raw("/routes/auth/logout", {
      method: "PATCH",
      body: {
        message: "delete",
        access_token: access.value,
        refresh_token: refresh.value,
      },
    });
  }
  access.value = null;
  refresh.value = null;
  return navigateTo("/login");
}
</script>

<template>
  <UPage>
    <UHeader to="/persons">
      <template #title>
        <ElementLogoDiv />
      </template>
      <template #default>
        <UNavigationMenu
          v-if="sessionStore.user?.role === 'admin'"
          :items="[
            {
              label: 'Пользователи',
              icon: 'i-lucide-users',
              to: '/users',
            },
          ]"
          variant="link"
        />
      </template>
      <template #right>
        <UButton
          class="rounded-full"
          :label="sessionStore.user?.username ?? 'Выйти'"
          color="error"
          icon="i-lucide-log-out"
          @click="logout()"
        />
      </template>
    </UHeader>

    <UMain class="pt-16">
      <slot />
    </UMain>

    <USeparator type="dashed" class="h-px" />

    <UFooter>
      <template #left>
        <p class="text-sm">Copyright © {{ new Date().getFullYear() }}</p>
      </template>

      <template #right>
        <UNavigationMenu
          :items="[
            {
              label: 'OpenAPI',
              to: `${path}/schema/swagger`,
              target: '_blank',
            },
            {
              label: 'GitHub',
              to: 'https://github.com/waldesem/Web-Personal-DB',
              target: '_blank',
            },
          ]"
          variant="link"
        />
      </template>
    </UFooter>
  </UPage>
</template>
