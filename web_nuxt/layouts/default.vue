<script setup lang="ts">
import type { Message } from "@/types";

const authFetch = useFetchAuth();

const messages = ref([] as Message[]);
const updated = ref("Данные обновляются...");

const { refresh, status } = await useLazyAsyncData("messages", async () => {
  messages.value = (await authFetch("/route/messages")) as Message[];
  updated.value = new Date().toLocaleTimeString("ru-RU");
});

async function clearMessages() {
  if (confirm("Вы действительно хотите очистить сообщения?")) {
    await authFetch("/route/messages", {
      method: "DELETE",
    });
    messages.value = [];
    updated.value = new Date().toLocaleTimeString("ru-RU");
  }
}

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

const isOpen = ref(false);
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
        <UTooltip :text="messages.length ? 'Есть непрочитанные сообщения' : 'Новых сообщений нет'">
          <UButton
            :icon="messages.length ? 'i-heroicons-bell-alert' : 'i-heroicons-bell'"
            :color="messages.length ? 'blue' : 'white'"
            variant="ghost"
            :loading="status == 'pending'"
            :disabled="!messages.length"
            @click="isOpen = true"
          />
        </UTooltip>
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
    <USlideover v-model="isOpen" :overlay="false">
      <div class="flex items-center justify-between mb-3">
        <UTooltip text="Обновить">
          <UButton
            icon="i-heroicons-arrow-path"
            variant="ghost"
            @click="refresh()"
          />
        </UTooltip>
        <UTooltip text="Очистить">
          <UButton
            icon="i-heroicons-x-mark"
            variant="ghost"
            @click="clearMessages"
          />
        </UTooltip>
      </div>
      <div class="text-sm font-bold py-1">
        {{ `Обновлено: ${updated}` }}
      </div>
      <div v-for="item in messages" :key="item.id" :item="item">
        <ElementsCardDiv>
          <template #header>
            {{ item.theme }}
          </template>
          {{ item.message }}
          <template #footer>
            {{ item.created }}
          </template>
        </ElementsCardDiv>
      </div>
    </USlideover>
  </UContainer>
</template>
