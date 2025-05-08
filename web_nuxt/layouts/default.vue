<script setup lang="ts">
import { UButton } from "@/.nuxt/components";

async function logout() {
  if (confirm("Вы действительно хотите выйти?")) {
    accessToken.value = "";
    clearNuxtData();
    return navigateTo("/login");
  }
  return;
}
</script>

<template>
  <UContainer
    :ui="{ constrained: 'max-w-screen-2xl', padding: 'px-4 sm:px-6 lg:px-12' }"
  >
    <div class="sticky flex items-center justify-between pt-8 pb-16">
      <UTooltip text="На главную страницу">
        <NuxtLink to="/persons">
          <div class="inline-flex flex items-center text-xl font-bold">
            <h3 class="text-blue-600">STAFFSEC</h3>
            &nbsp;
            <h3 class="text-red-600">ФИНТЕХ</h3>
          </div>
        </NuxtLink>
      </UTooltip>
      <div v-if="stateUser.role == 'admin'">
        <NuxtLink to="/users">ПОЛЬЗОВАТЕЛИ</NuxtLink>
      </div>
      <UTooltip text="Выход">
        <UButton
          class="rounded-full"
          :label="stateUser.username"
          color="error"
          icon="i-heroicons-arrow-left-end-on-rectangle"
          @click="logout()"
        />
      </UTooltip>
    </div>
    <div>
      <slot />
    </div>
  </UContainer>
</template>
