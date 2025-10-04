<script setup lang="ts">
useHead({
  htmlAttrs: { lang: "ru" },
  link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
  meta: [
    { name: "description", content: "Кадровая безопасность" },
    { name: "viewport", content: "width=device-width, initial-scale=1" },
    { charset: "utf-8" },
  ],
});

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
</script>

<template>
  <UApp>
    <NuxtLoadingIndicator color="red" :height="5" />
    <UHeader>
      <template #title>
        <NuxtLink to="/persons" title="На главную страницу">
          <div
            class="flex inline-flex items-center text-xl font-bold space-x-1"
          >
            <h3 class="text-blue-600">STAFFSEC</h3>
            <h3 class="text-red-600">ФИНТЕХ</h3>
          </div>
        </NuxtLink>
      </template>
      <template #default>
        <UNavigationMenu
          v-if="userState.role"
          :items="[
            {
              label: 'Пользователи',
              icon: 'i-lucide-users',
              to: '/users',
              disabled: userState.role !== 'admin',
            },
            {
              label: 'Кандидаты',
              icon: 'i-lucide-users-round',
              to: '/persons',
            },
          ]"
          variant="link"
        />
      </template>
      <template #right>
        <UButton
          class="rounded-full"
          :label="userState.username ?? ''"
          :disabled="!userState.username"
          color="error"
          icon="i-lucide-log-out"
          :title="userState.username ? 'Выход' : ''"
          @click="logout()"
        />
      </template>
    </UHeader>
    <UMain>
      <UContainer class="pt-16">
        <NuxtPage
          :transition="{
            name: 'page',
          }"
        />
      </UContainer>
    </UMain>
    <USeparator type="dashed" class="h-px" />
    <UFooter>
      <template #left>
        <p class="text-muted text-sm">
          Copyright © {{ new Date().getFullYear() }}
        </p>
      </template>

      <template #right>
        <UButton
          icon="i-lucide-computer"
          title="GitHub"
          color="neutral"
          variant="ghost"
          to="https://github.com/waldesem/Web-Personal-DB"
          target="_blank"
        />
      </template>
    </UFooter>
  </UApp>
</template>

<style>
/* .page-enter-active,
.page-leave-active {
  transition: all 0.2s;
}
.page-enter-from,
.page-leave-to {
  opacity: 0;
}

html,
body {
  scrollbar-gutter: stable;
} */

/* html {
    overflow-x: hidden;
    margin-right: calc(-1 * (100vw - 100%));
}

html {
    margin-left: calc(100vw - 100%);
    margin-right: 0;
} */
</style>
