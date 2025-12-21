<script setup lang="ts">
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
const {
  data: person,
  status,
  refresh,
} = await useAsyncData(
  "person",
  () => $api<Person>("/routes/persons/" + candId.value),
  { default: () => ({} as Person) }
);

// Вычисляем статус редактирования анкеты
const editable = computed(() => {
  return (
    person.value.editable &&
    userState.value.role == "user" &&
    userState.value.id == person.value.user_id
  );
});
// Передаем статус редактирования в другие компоненты
provide("editable", editable);

// Определяем функцию для переключения режима редактирования
async function switchSelf(): Promise<void> {
  if (person.value && person.value.user_id != userState.value.id) {
    if (person.value.editable) {
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
    refresh();
  } else {
    toasts.create();
  }
}
</script>

<template>
  <UPage>
    <UPageHeader
      :title="`${person?.surname} ${person?.firstname} ${
        person?.patronymic ?? ''
      }`"
      :ui="{
        root: 'relative border-none py-4 mb-2',
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
            :color="
              !person?.editable
                ? 'secondary'
                : person.user_id == userState.id
                ? 'success'
                : 'error'
            "
            :label="
              !person?.editable
                ? 'Доступно'
                : person.user_id == userState.id
                ? 'Изменение'
                : 'Закрыто'
            "
            :icon="
              !person?.editable
                ? 'i-lucide-lock-open'
                : person.user_id == userState.id
                ? 'i-lucide-edit'
                : 'i-lucide-lock'
            "
            @click="switchSelf"
          />
        </div>
      </template>
    </UPageHeader>

    <ContentItemTabs>
      <template #anketa-tab>
        <ContentAnketaTab
          :person="person"
          :status="status"
          :editable="editable"
        />
      </template>
    </ContentItemTabs>
  </UPage>
</template>
