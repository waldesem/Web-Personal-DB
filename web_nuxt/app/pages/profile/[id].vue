<script setup lang="ts">
import { useEventListener } from "@vueuse/core";
import type { Person } from "@/types";

await prefetchComponents("UModal");

const toasts = useToasts();

const print = ref(false);

useEventListener(window, "afterprint", (_event) => {
  print.value = false;
});

// Получаем данные id кандидата из URL
const route = useRoute();
const candId = computed(() => route.params.id as string);
provide("candId", candId);

// Используем плагин для передачи данных на сервер
const { $api } = useNuxtApp();

// Определяем функцию для получения данных из API
const { data, status, refresh } = await useAsyncData(
  "person",
  () => $api<Person>("/routes/persons/" + candId.value),
  { default: () => ({} as Person) }
);

// Вычисляем статус редактирования анкеты
const editable = computed(() => {
  return (
    data.value.editable &&
    userState.value.role == "user" &&
    userState.value.id == data.value.user_id
  );
});
// Передаем статус редактирования в другие компоненты
provide("editable", editable);

// Определяем функцию для переключения режима редактирования
async function switchSelf(): Promise<void> {
  if (data.value && data.value.user_id != userState.value.id) {
    if (data.value.editable) {
      if (
        !confirm(
          "Анкета редактируется другим пользователем. Переключить режим?"
        )
      ) {
        return;
      }
    } else if (!confirm("Вы хотите назначить анкету на себя?")) {
      return;
    }
  } else if (!confirm("Переключить режим редактирования?")) {
    return;
  }
  status.value = "pending";
  const { message } = await $api<Record<string, string>>(
    "/routes/self/" + candId.value
  );
  status.value = message as "success" | "error";
  if (message == "success") {
    await refresh();
  } else {
    toasts.create();
  }
}
</script>

<template>
  <UPage>
    <UPageHeader
      :title="`${data?.surname} ${data?.firstname} ${data?.patronymic ?? ''}`"
      :ui="{
        root: 'relative border-none py-4 mb-2',
        title: 'text-2xl sm:text-3xl text-red-800',
      }"
    >
      <template #links>
        <ClientOnly>
          <!-- Кнопки для загрузки файлов и переключения режима редактирования -->
          <div
            v-if="userState.role == 'user'"
            class="flex items-center space-x-4 no-print"
          >
            <UButton
              :loading="status === 'pending'"
              variant="outline"
              :icon="!print ? 'i-lucide-printer' : 'i-lucide-arrow-left'"
              :label="!print ? 'Печать' : 'Вернуться'"
              @click="print = !print"
            />
            <UButton
              v-if="!print"
              :loading="status === 'pending'"
              variant="outline"
              :color="
                !data?.editable
                  ? 'secondary'
                  : data.user_id == userState.id
                  ? 'success'
                  : 'error'
              "
              :label="
                !data?.editable
                  ? 'Доступно'
                  : data.user_id == userState.id
                  ? 'Изменение'
                  : 'Закрыто'
              "
              :icon="
                !data?.editable
                  ? 'i-lucide-lock-open'
                  : data.user_id == userState.id
                  ? 'i-lucide-edit'
                  : 'i-lucide-lock'
              "
              @click="switchSelf"
            />
          </div>
        </ClientOnly>
      </template>
    </UPageHeader>

    <KeepAlive>
      <ContentItemTabs v-if="!print">
        <template #anketa-tab>
          <ContentAnketaTab
            :person="data"
            :status="status"
            :editable="editable"
          />
          <USeparator />
          <!-- Выводим аккордеон с данными staffs, educations и т.д. -->
          <ContentItemDivs />
        </template>
      </ContentItemTabs>

      <ContentPrintDiv v-else />
    </KeepAlive>
  </UPage>
</template>
