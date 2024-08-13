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
      labelClass: "text-xl text-primary mb-3",
      to: "/persons",
    },
  ],
  [
    {
      label: "Создать",
      labelClass: "text-xl text-primary py-3",
      to: "/resume",
      disabled:
        userState.user.value.role !== classify.classes.value.roles["user"],
    },
  ],
  [
    {
      label: "Информация",
      labelClass: "text-xl text-primary py-3",
      to: "/info",
    },
  ],
  [
    {
      label: "Пользователи",
      labelClass: "text-xl text-primary py-3",
      to: "/users",
      disabled:
        userState.user.value.role !== classify.classes.value.roles["admin"],
    },
  ],
  [
    {
      label: "Выход",
      labelClass: "text-xl text-primary mt-3",
      to: "/login",
      click: () => removeToken(),
    },
  ],
];
</script>

<template>
  <div class="mx-auto px-16">
    <header class="sticky py-8">
      <div class="flex justify-between grid grid-cols-12 gap-3">
        <div class="col-span-2">
          <h3 class="text-2xl text-red-800 font-bold">STAFFSEC FINTECH</h3>
        </div>
        <div class="col-span-9 h-[--header-height]">
          <ElementsAlertMessage />
        </div>
        <div class="col-span-1 content-right">
          <UButton
            icon="i-heroicons-moon"
            :variant="$colorMode.preference == 'dark' ? 'soft' : 'ghost'"
            @click="$colorMode.preference = 'dark'"
          />
          <UButton
            icon="i-heroicons-sun"
            :variant="$colorMode.preference == 'light' ? 'soft' : 'ghost'"
            @click="$colorMode.preference = 'light'"
          />
        </div>
      </div>
    </header>
    <div class="flex flex-col grid grid-cols-12 gap-3">
      <div class="col-span-2 py-3">
        <UVerticalNavigation :links="links" :ui="{ active: '' }" />
      </div>
      <div class="col-span-10 py-3">
        <slot />
      </div>
    </div>
  </div>
</template>
