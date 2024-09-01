<script setup lang="ts">
import { stateUser, stateClassify, userToken } from "@/state/state";

const classify = stateClassify();
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
  if (userState.user.value.role !== classify.classes.value.roles["user"]) {
    return links.filter((item) => item[0].to !== "/resume");
  } else if (
    userState.user.value.role !== classify.classes.value.roles["admin"]
  ) {
    return links.filter((item) => item[0].to !== "/users");
  } else if (
    userState.user.value.role !== classify.classes.value.roles["guest"]
  ) {
    return links.filter(
      (item) => item[0].to !== "/users" && item[0].to !== "/resume"
    );
  } else {
    return links;
  }
});
</script>

<template>
  <UContainer :ui="{ constrained: 'max-w-none', padding: 'px-4 sm:px-6 lg:px-12' }">
    <div class="flex flex-col h-screen">
      <header class="sticky py-8">
        <div class="flex justify-between grid grid-cols-12 gap-3">
          <div class="col-span-2">
            <h3 class="text-2xl text-red-800 font-bold">STAFFSEC FINTECH</h3>
          </div>
          <div class="col-span-10 relative">
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
            <UButton
              v-if="userState.user.value.username"
              class="absolute top-0 right-24"
              icon="i-heroicons-user"
              variant="ghost"
              :title="userState.user.value.username"
            />
          </div>
        </div>
      </header>
      <div
        class="flex flex-grow flex-col grid grid-cols-12 gap-3"
        style="padding-bottom: 5vh"
      >
        <div class="col-span-2 py-3">
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
        <div class="col-span-10 py-8">
          <slot />
        </div>
      </div>
      <footer
        class="flex justify-center py-3 bg-white border-t dark:bg-gray-800 dark:border-gray-700"
      >
        <a
          class="text-gray-500"
          href="https://github.com/waldesem/Web-Personal-DB"
          target="_blank"
          >GitHub</a
        >
      </footer>
    </div>
  </UContainer>
</template>
