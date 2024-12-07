<script setup lang="ts">
const showNav = ref(true);
const isOpen = ref(false)

async function logout() {
  if (confirm("Вы действительно хотите выйти?")) {
    accessToken.value = null;
    refreshToken.value = null;
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
      label: "информация",
      icon: "i-heroicons-information-circle",
      to: "/info",
    },
  ],
  [
    {
      label: "выход",
      icon: "i-heroicons-arrow-left-end-on-rectangle",
      to: "/login",
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
    :ui="{ constrained: 'max-w-none', padding: 'px-4 sm:px-6 lg:px-12' }"
  >
    <header class="sticky pt-8 pb-16">
      <div class="flex justify-between relative">
        <div class="absolute top-0 left-0">
          <UButton
            icon="i-heroicons-bars-4"
            variant="ghost"
            @click="showNav = !showNav"
          />
        </div>
        <div class="absolute top-0 left-12 inline-flex text-xl font-bold">
          <h3 class="text-blue-800">STAFFSEC</h3>
          &nbsp;
          <h3 class="text-red-600">ФИНТЕХ</h3>
        </div>
        <div class="absolute top-0 right-0">
          <UButton
            icon="i-heroicons-bell"
            variant="ghost"
            @click="isOpen = !isOpen"
          />
          <!-- <USlideover v-model="isOpen"/> -->
        </div>
        <UPopover
          class="absolute top-0 right-12"
          mode="hover"
          :popper="{ placement: 'top-start' }"
        >
          <UAvatar :alt="stateUser.fullname" />
          <template #panel>
            <div class="m-3 text-center text-sm text-gray-600">
              <div>{{ stateUser.fullname }}</div>
              <div>Логин: {{ stateUser.username }}</div>
              <div>Регион: {{ stateUser.region }}</div>
              <div>Роль: {{ stateUser.role }}</div>
            </div>
          </template>
        </UPopover>
      </div>
    </header> 
    <div class="grid grid-cols-12 gap-6">
      <div
        v-if="showNav"
        class="flex flex-col w-full h-full col-span-2 pt-3 border-r border-gray-200"
      >
        <UVerticalNavigation
          :links="filtredLinks"
          :ui="{
            active:
              'text-red-800 dark:text-white before:bg-gray-0 dark:before:bg-gray-0',
            inactive:
              'text-primary-800 dark:text-gray-400 hover:text-red-600 dark:hover:text-white hover:before:bg-gray-0 dark:hover:before:bg-gray-800/50',
            size: 'text-xl mt-4',
            icon: {
              active: 'text-red-800 dark:text-white',
              inactive:
                'text-primary-800 dark:text-gray-400 hover:text-red-600 dark:hover:text-white',
            },
          }"
        />
      </div>
      <div
        class="flex flex-col py-8"
        :class="showNav ? 'col-span-10' : 'col-span-12'"
      >
        <slot />
      </div>
    </div>
  </UContainer>
</template>
