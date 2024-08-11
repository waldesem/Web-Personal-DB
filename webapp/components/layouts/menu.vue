<script setup lang="ts">
import { stateUser, stateClassify } from "@/state/state";

const classify = stateClassify();
const userState = stateUser();

async function removeToken(): Promise<void> {
  if (confirm("Вы действительно хотите выйти?")) {
    navigateTo("/login");
    localStorage.removeItem("user_token");
  }
}
</script>

<template>
  <div class="mx-auto px-16">
    <header class="sticky py-8">
      <div class="flex items-center justify-between grid grid-cols-12 gap-3">
        <div class="col-span-2">
          <h3 class="text-2xl text-primary font-bold">STAFFSEC FINTECH</h3>
        </div>
        <div class="col-span-9 h-[--header-height]">
          <DivsAlertMessage />
        </div>
        <div class="col-span-1">
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
    <div class="flex-col grid grid-cols-9 gap-8">
      <div class="col-span-1 py-2">
        <div class="text-xl text-primary mb-3">
          <NuxtLink to="/persons"> Кандидаты </NuxtLink>
        </div>
        <UDivider />
        <div
          v-if="
            userState.user.value.role == classify.classes.value.roles['user']
          "
          class="text-xl text-primary py-3"
        >
          <NuxtLink to="/resume">Создать</NuxtLink>
        </div>
        <UDivider
          v-if="
            userState.user.value.role == classify.classes.value.roles['user']
          "
        />
        <div class="text-xl text-primary py-3">
          <NuxtLink to="/info"> Информация</NuxtLink>
        </div>
        <UDivider />
        <div
          v-if="
            userState.user.value.role == classify.classes.value.roles['admin']
          "
          class="text-xl text-primary py-3"
        >
          <NuxtLink to="/users">Пользователи</NuxtLink>
        </div>
        <UDivider
          v-if="
            userState.user.value.role == classify.classes.value.roles['admin']
          "
        />
        <div class="text-xl text-primary py-3">
          <NuxtLink to="/" @click="removeToken">Выход</NuxtLink>
        </div>
      </div>
      <div class="col-span-8 py-3">
        <slot />
      </div>
    </div>
  </div>
</template>
