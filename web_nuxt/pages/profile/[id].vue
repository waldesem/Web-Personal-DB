<script setup lang="ts">
import { useFileDialog } from "@vueuse/core";
import type { Persons } from "@/types";

await prefetchComponents('UModal');

// Получаем данные id кандидата из URL
const route = useRoute();
const candId = computed(() => route.params.id as string);
// Передаем данные id кандидата в другие компоненты
provide("candId", candId);

const userState = useStateUser();

// Используем плагин для передачи данных на сервер
const { $api } = useNuxtApp();

// Определяем функцию для получения данных из API
const { data, status, refresh } = await useAsyncData("persons", async () => {
  return (await $api("/routes/persons/" + candId.value)) as Persons;
});

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
    useToasts();
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
      useToasts("info", "Размер одного файла не должен превышать 10 МБ");
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
    useToasts(message, "Файлы успешно загружены");
  } else {
    useToasts();
  }
});
</script>

<template>
  <UPage v-if="data">
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
            icon="i-lucide-cloud-upload"
            label="Загрузить файлы"
            @click="open()"
          />
          <UButton
            :loading="status === 'pending'"
            :color="
              !data?.editable
                ? 'secondary'
                : data.user_id == userState.id
                ? 'success'
                : 'error'
            "
            :label="
              !data?.editable
                ? 'Доступно для редактирования'
                : data.user_id == userState.id
                ? 'Назначено текущему пользователю'
                : 'Редактируется другим пользователем'
            "
            @click="switchSelf"
          />
        </div>
      </template>
    </UPageHeader>
    <!-- Меню для переключения между вкладками -->
    <ContentSharedTabs>
      <template #anketa-tab>
        <ContentAnketaTab
          :person="data"
          :status="status"
          :editable="editable"
        />
      </template>
    </ContentSharedTabs>
  </UPage>
</template>
