<script setup lang="ts">
import { useFileDialog } from "@vueuse/core";
import type { Person } from "@/types";

await prefetchComponents("UModal");

const toasts = useToasts();

// Получаем данные id кандидата из URL
const route = useRoute();
const candId = computed(() => route.params.id as string);
provide("candId", candId);

// Используем плагин для передачи данных на сервер
const { $api } = useNuxtApp();

// Определяем функцию для получения данных из API
const { data, status, refresh } = await useAsyncData("person", () =>
  $api<Person>("/routes/persons/" + candId.value)
);

// Вычисляем статус редактирования анкеты
const editable = computed(() => {
  return (
    data.value &&
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

// Определяем диалог загрузки файлов
const { open, onChange } = useFileDialog();

// Определяем функцию для загрузки файлов
onChange(async (files) => {
  if (!files) return;
  const formData = new FormData();
  for (const file of files) {
    if (file.size > 10 * 1024 * 1024) {
      toasts.create("info", "Размер одного файла не должен превышать 10 МБ");
      continue;
    }
    formData.append("file", file);
  }
  const { message } = await $api<Record<string, string>>(
    `/routes/files/${candId.value}`,
    {
      method: "POST",
      body: formData,
    }
  );
  status.value = message as "success" | "error";
  if (message == "success") {
    toasts.create(message, "Файлы успешно загружены");
  } else {
    toasts.create();
  }
});
</script>

<template>
  <UPage>
    <UPageHeader
      :title="`${data?.surname} ${data?.firstname} ${data?.patronymic ?? ''}`"
      :ui="{
        root: 'relative border-none py-4',
        title: 'text-2xl sm:text-3xl text-red-800',
      }"
    >
      <template #links>
        <!-- Кнопки для загрузки файлов и переключения режима редактирования -->
        <div
          v-if="userState.role == 'user'"
          class="flex items-center space-x-4"
        >
          <UButton
            :loading="status === 'pending'"
            variant="outline"
            icon="i-lucide-printer"
            label="Печать"
            @click="navigateTo('/print')"
          />
          <UButton
            v-if="editable"
            :loading="status === 'pending'"
            variant="outline"
            icon="i-lucide-cloud-upload"
            label="Загрузить"
            @click="open()"
          />
          <UButton
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
                ? 'Редакция'
                : 'Занято'
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
      </template>
    </UPageHeader>

    <!-- Меню для переключения между вкладками -->
    <ContentItemTabs>
      <template #anketa-tab>
        <ContentAnketaTab
          :person="data ?? ({} as Person)"
          :status="status"
          :editable="editable"
        />
        <USeparator />
        <!-- Выводим аккордеон с данными staffs, educations и т.д. -->
        <ContentItemDivs />
      </template>
    </ContentItemTabs>
  </UPage>
</template>
