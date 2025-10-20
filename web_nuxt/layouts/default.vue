<script setup lang="ts">

definePageMeta({
  middleware: ["user"],
});

// Объявляем переменную для получения данных пользователя
const userState = useStateUser();

// Объявляем функцию для выхода из системы и очистки данных пользователя
function logout() {
  if (!confirm("Вы действительно хотите выйти?")) return;
  const token = useCookie("token");
  const refresh = useCookie("refresh");
  token.value = null;
  refresh.value = null;
  clearNuxtData();
  return navigateTo("/login");
}
</script>

<template>
  <div>
    <UHeader>
      <template #title>
        <NuxtLink to="/persons" title="На главную страницу">
          <ElementsLogoDiv />
        </NuxtLink>
      </template>
      <template #default>
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
      </template>
      <template #right>
        <UButton
          class="rounded-full"
          :label="userState.username ?? ''"
          :disabled="!userState.username"
          color="error"
          icon="i-lucide-log-out"
          @click="logout()"
        />
      </template>
    </UHeader>
    <UMain>
      <UContainer class="pt-16">
        <slot />
      </UContainer>
    </UMain>
    <USeparator type="dashed" class="h-px" />
    <UFooter>
      <template #left>
        <p class="text-sm">{{ new Date().getFullYear() }}</p>
      </template>

      <template #right>
        <UButton
          icon="i-lucide-computer"
          label="GitHub"
          color="neutral"
          variant="ghost"
          to="https://github.com/waldesem/Web-Personal-DB"
          target="_blank"
        />
      </template>
    </UFooter>
  </div>
</template>
