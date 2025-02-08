<script setup lang="ts">
async function logout() {
  if (confirm("Вы действительно хотите выйти?")) {
    accessToken.value = "";
    clearNuxtData();
    return navigateTo("/login");
  }
  return;
}

const links = [
  [
    {
      label: "ПОЛЬЗОВАТЕЛИ",
      icon: "i-heroicons-user-group",
      to: "/users",
    },
  ],
  [
    {
      label: "СТАТИСТИКА",
      icon: "i-heroicons-chart-pie",
      to: "/info",
    },
  ],
];
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
      <div
        v-if="stateUser.role == 'admin'"
        class="flex items-center justify-end"
      >
        <UHorizontalNavigation
          :ui="{
            active: 'text-red-600',
            inactive: 'text-blue-600',
            icon: {
              active: 'text-red-600',
              inactive: 'text-blue-600',
            },
          }"
          :links="links"
        />
      </div>
      <div class="flex items-center justify-end">
        <UTooltip text="Выход">
          <UButton
            :label="stateUser.username"
            color="red"
            icon="i-heroicons-arrow-left-end-on-rectangle"
            :ui="{ rounded: 'rounded-full' }"
            @click="logout()"
          />
        </UTooltip>
      </div>
    </div>
    <div>
      <slot />
    </div>
  </UContainer>
</template>
