<script setup lang="ts">
import type { Message } from "@/types";

const authFetch = useFetchAuth();

const route = useRoute();

const messages = ref([] as Message[]);
const updated = ref(new Date());

const { refresh, status } = await useLazyAsyncData("messages", async () => {
  messages.value = (await authFetch("/route/messages")) as Message[];
  updated.value = new Date();
});

watch(route, () => {
  if (
    route.path == "/persons" &&
    new Date().getTime() - updated.value.getTime() > 1000 * 600
  )
    refresh();
});

async function clearMessages() {
  if (confirm("Вы действительно хотите очистить сообщения?")) {
    await authFetch("/route/messages", {
      method: "DELETE",
    });
    messages.value = [];
    updated.value = new Date();
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
      <div class="flex items-center justify-end space-x-4">
        <UTooltip
          :text="
            messages.length
              ? 'Есть непрочитанные сообщения'
              : 'Новых сообщений нет'
          "
        >
          <UButton
            :icon="
              messages.length ? 'i-heroicons-bell-alert' : 'i-heroicons-bell'
            "
            variant="ghost"
            size="xl"
            :loading="status == 'pending'"
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
      <div class="p-1" style="overflow-y: scroll">
        <div class="flex items-center justify-between m-3">
          <UTooltip text="Обновить">
            <UButton
              icon="i-heroicons-arrow-path"
              variant="ghost"
              @click="refresh()"
            />
          </UTooltip>
          <div class="text-sm font-bold">
            {{ `Обновлено: ${updated.toLocaleString("ru-RU")}` }}
          </div>
          <UTooltip text="Очистить">
            <UButton
              icon="i-heroicons-trash"
              variant="ghost"
              @click="clearMessages"
            />
          </UTooltip>
        </div>
        <div v-for="item in messages" :key="item.id" :item="item" class="m-3">
          <UCard
            :ui="{
              divide: '',
              body: { padding: 'px-1 py-2 sm:p-2' },
              header: {
                padding: 'px-1 py-2 sm:p-2',
                background: 'bg-gray-100',
              },
              footer: { padding: 'px-1 py-1 sm:p-1' },
            }"
          >
            <template #header>
              <div class="text-sm font-bold">
                {{ item.theme }}
              </div>
            </template>
            <div class="text-sm">
              {{ item.message }}
            </div>
            <template #footer>
              <div class="text-xs font-bold italic text-right">
                {{ new Date(item.created).toLocaleString("ru-RU") }}
              </div>
            </template>
          </UCard>
        </div>
      </div>
    </USlideover>
  </UContainer>
</template>
