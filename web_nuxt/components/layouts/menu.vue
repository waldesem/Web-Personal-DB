<script setup lang="ts">
import { stateUser, userToken } from "@/utils/auth";

const userState = stateUser();

async function removeToken(): Promise<void> {
  if (confirm("Вы действительно хотите выйти?")) {
    navigateTo("/login");
    userToken.value = "";
  }
}

const links = [
  [
    {
      label: "Кандидаты",
      to: "/persons",
    },
  ],
  [
    {
      label: "Создать",
      to: "/resume",
    },
  ],
  [
    {
      label: "Информация",
      to: "/info",
    },
  ],
  [
    {
      label: "Пользователи",
      to: "/users",
    },
  ],
  [
    {
      label: "Выход",
      to: "/login",
      click: () => removeToken(),
    },
  ],
];

const filtredLinks = computed(() => {
  if (userState.value.role !== "user") {
    return links.filter((item) => item[0].to !== "/resume");
  } else if (userState.value.role !== "admin") {
    return links.filter((item) => item[0].to !== "/users");
  } else if (userState.value.role !== "guest") {
    return links.filter(
      (item) => item[0].to !== "/users" && item[0].to !== "/resume"
    );
  } else {
    return links;
  }
});
</script>

<template>
  <UContainer
    :ui="{ constrained: 'max-w-none', padding: 'px-4 sm:px-6 lg:px-12' }"
  >
    <header class="sticky pt-8 pb-16">
      <div class="flex justify-between relative">
        <div class="absolute top-0 left-0 inline-flex text-2xl font-bold">
          <h3 class="text-primary">STAFFSEC</h3>
            &nbsp;
          <h3 class="text-red-800">ФИНТЕХ</h3>
        </div>
        <UButton
          class="absolute top-0 right-0"
          icon="i-heroicons-moon"
          :variant="$colorMode.preference == 'dark' ? 'soft' : 'ghost'"
          @click="$colorMode.preference = 'dark'"
        />
        <UButton
          class="absolute top-0 right-12"
          icon="i-heroicons-sun"
          :variant="$colorMode.preference == 'light' ? 'soft' : 'ghost'"
          @click="$colorMode.preference = 'light'"
        />
        <UPopover class="absolute top-0 right-24" mode="hover" :popper="{ placement: 'top-start' }">
          <UAvatar :alt="userState.fullname" />
          <template #panel>
            <ElementsCardDiv>
              <p class="text-center text-sm text-gray-500">
                {{ userState.fullname }}
              </p>
              <p class="text-center text-sm text-gray-500">
                Логин: {{ userState.username }}
              </p>
              <p class="text-center text-sm text-gray-500">
                Регион: {{ userState.region }}
              </p>
              <p class="text-center text-sm text-gray-500">
                Роль: {{ userState.role }}
              </p>
            </ElementsCardDiv>
          </template>
        </UPopover>
      </div>
    </header>
    <div class="grid grid-cols-12 gap-6">
      <div
        class="flex flex-col h-full col-span-2 pt-3 border-r border-gray-200"
      >
        <UVerticalNavigation
          :links="filtredLinks"
          :ui="{
            active:
              'text-red-900 dark:text-white before:bg-gray-0 dark:before:bg-gray-0',
            inactive:
              'text-gray-500 dark:text-gray-400 hover:text-red-600 dark:hover:text-white hover:before:bg-gray-0 dark:hover:before:bg-gray-800/50',
            size: 'text-xl text-primary mt-4',
          }"
        />
      </div>
      <div class="flex flex-col col-span-10 py-8">
        <slot />
      </div>
    </div>
  </UContainer>
</template>
