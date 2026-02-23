<script setup lang="ts">
import type { Session } from "@/types";

const { $api } = useNuxtApp();

const visibility = useDocumentVisibility();

const path = computed(() => window.location.origin);

const { data: user } = await useAsyncData(
  "session",
  () => $api<Session>("/routes/auth/session"),
  {
    watch: [refThrottled(visibility, 600000)],
    default: () => ({}) as Session,
  },
);

// Объявляем функцию для выхода из системы и очистки данных пользователя
async function logout() {
  if (!confirm("Вы действительно хотите выйти?")) return;
  const access = useCookie("access");
  const refresh = useCookie("refresh");
  await $api("/routes/auth/logout", {
    method: "POST",
    body: {
      refresh_token: refresh.value,
    },
  });
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
        <!--<ClientOnly>-->
        <UNavigationMenu
          v-if="user.role === 'admin'"
          :items="[
            {
              label: 'Пользователи',
              icon: 'i-lucide-users',
              to: '/users',
            },
          ]"
          variant="link"
        />
        <!--</ClientOnly>-->
      </template>
      <template #right>
        <!--<ClientOnly>-->
        <UButton
          class="rounded-full"
          :label="user.username ?? 'Выйти'"
          color="error"
          icon="i-lucide-log-out"
          @click="logout()"
        />
        <!--</ClientOnly>-->
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
