<script setup lang="ts">
async function logout() {
  if (confirm("Вы действительно хотите выйти?")) {
    accessToken.value = null;
    clearNuxtData();
    return navigateTo("/login");
  }
  return;
}

const links = [
  [
    {
      label: "кандидаты",
      icon: "i-heroicons-user-circle",
      to: "/persons",
    },
  ],
  [
    {
      label: "создать",
      icon: "i-heroicons-newspaper",
      to: "/resume",
    },
  ],
  [
    {
      label: "пользователи",
      icon: "i-heroicons-user-group",
      to: "/users",
    },
  ],
  [
    {
      label: "статистика",
      icon: "i-heroicons-chart-pie",
      to: "/info",
    },
  ],
  [
    {
      label: stateUser.value.username,
      icon: "i-heroicons-arrow-left-end-on-rectangle",
      click: () => logout(),
    },
  ],
];

const filtredLinks = computed(() => {
  if (!stateUser.value) {
    return [];
  }
  if (stateUser.value.role === "admin") {
    return links.filter((item) => item[0].to !== "/resume");
  } else if (stateUser.value.role === "user") {
    return links.filter((item) => item[0].to !== "/users");
  } else {
    return links.filter(
      (item) => item[0].to !== "/users" && item[0].to !== "/resume"
    );
  }
});
</script>

<template>
  <UContainer
    :ui="{ constrained: 'max-w-screen-2xl', padding: 'px-4 sm:px-6 lg:px-12' }"
  >
    <div class="sticky flex items-center justify-between pt-8 pb-16">
      <div class="inline-flex flex items-center text-xl font-bold">
        <h3 class="text-blue-800">STAFFSEC</h3>
        &nbsp;
        <h3 class="text-red-600">ФИНТЕХ</h3>
      </div>
      <div class="flex items-center justify-end">
        <UHorizontalNavigation :links="filtredLinks" />
      </div>
    </div>
    <div>
      <slot />
    </div>
  </UContainer>
</template>
