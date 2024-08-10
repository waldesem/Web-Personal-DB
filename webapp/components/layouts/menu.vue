<script setup lang="ts">
import { stateUser, stateClassify } from "@/state/state";

const classify = stateClassify();
const userState = stateUser();

async function removeToken(): Promise<void> {
  localStorage.removeItem("user_token");
}

const colors = [
  { name: "system", value: "system" },
  { name: "light", value: "light" },
  { name: "dark", value: "dark" },
  { name: "sepia", value: "sepia" },
]
</script>

<template>
  <header class="bg-background/75 backdrop-blur border-b -mb-px sticky top-0 z-50 border-gray-200 dark:border-gray-800">
    <div class="mx-auto px-4 sm:px-6 lg:px-8 max-w-7xl flex items-center justify-between gap-3 h-[--header-height]">
      <div class="lg:flex-1 flex items-center gap-1.5">
        <h3 class="text-2xl text-opacity-75 text-primary font-bold">
          STAFFSEC FINTECH
        </h3>
      </div>
      <div class="items-center gap-x-8 hidden lg:flex">
        <DivsAlertMessage />
      </div>
      <div class="flex items-center justify-end lg:flex-1 gap-1.5">
        <div>
          <USelect
            v-model="$colorMode.preference"
            :options="colors"
          />
        </div>
      </div>
    </div>
  </header>
  <div class="mx-auto px-4 sm:px-6 lg:px-8 max-w-7xl">
    <div class="flex flex-col lg:grid lg:grid-cols-10 lg:gap-8">
      <div class="lg:col-span-2">
        <NuxtLink to="/persons" class="nav-link active"> Кандидаты </NuxtLink>
        <NuxtLink
          v-if="
            userState.user.value.role == classify.classes.value.roles['user']
          "
          to="/resume"
          class="nav-link active"
        >
          Создать
        </NuxtLink>
        <NuxtLink to="/info" class="nav-link active"> Информация </NuxtLink>
        <NuxtLink
          v-if="
            userState.user.value.role == classify.classes.value.roles['admin']
          "
          to="/users"
          class="nav-link active"
        >
          Пользователи
        </NuxtLink>
        <NuxtLink
          to="/login"
          class="link-opacity-50-hover"
          @click="removeToken"
        >
          Выход
        </NuxtLink>
      </div>
      <div class="lg:col-span-8">
        <slot />
      </div>
    </div>
  </div>
  <footer class="relative">
    <div class="mx-auto px-4 sm:px-6 lg:px-8 max-w-7xl py-8 lg:py-4 lg:flex lg:items-center lg:justify-between lg:gap-x-3">
      <div class="mt-3 lg:mt-0 lg:order-2 flex items-center justify-center">
        <p>2024 STAFFSEC FINTECH</p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
#staffsec {
  padding-bottom: 5vh;
}
footer {
  position: fixed;
  bottom: 0;
  width: 100%;
  height: 5vh;
}
</style>
