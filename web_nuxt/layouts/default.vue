<script setup lang="ts">
const userState = useUserState();

async function logout() {
  if (!confirm("Вы действительно хотите выйти?")) return;
  accessToken.value = null;
  clearNuxtData();
  return navigateTo("/login");
}
</script>

<template>
  <UContainer>
    <div
      class="flex items-center justify-between sticky top-0 z-50 bg-white pt-8 pb-16"
    >
      <NuxtLink to="/persons" title="На главную страницу">
        <div class="flex inline-flex items-center text-xl font-bold">
          <h3 class="text-blue-600">STAFFSEC</h3>
          <USeparator orientation="vertical" size="lg" />
          <h3 class="text-red-600">ФИНТЕХ</h3>
        </div>
      </NuxtLink>
      <div v-if="userState.role == 'admin'">
        <UButton
          icon="i-heroicons-users"
          to="/users"
          variant="link"
          label="Пользователи"
        />
      </div>
      <UButton
        class="rounded-full"
        :label="userState.username"
        color="error"
        icon="i-heroicons-arrow-left-end-on-rectangle"
        title="Выход"
        @click="logout()"
      />
    </div>
    <div class="flex flex-col gap-4 px-1 mb-6">
      <slot />
    </div>
  </UContainer>
</template>
