<script setup lang="ts">
import type { Person, Session } from "@/types";

// Используем плагин для передачи данных на сервер
const { $api } = useNuxtApp();

const { data: user } = useNuxtData<Session>("session");

const toasts = useToasts();

const editable = useEditable();

// Получаем данные id кандидата из URL
const route = useRoute();

const candId = computed(() => route.params.id as string);

provide("candId", candId);

// Определяем функцию для получения данных из API
const { data, status, refresh } = await useAsyncData(
  "person",
  () => $api<Person>("/routes/persons/" + candId.value),
  { default: () => ({}) as Person },
);

// Вычисляем статус редактирования анкеты
editable.value = computed(() => {
  return (
    data.value.editable &&
    user.value?.role === "user" &&
    user.value?.id === data.value.user_id
  );
}).value;

// Определяем функцию для переключения режима редактирования
async function switchStatus(): Promise<void> {
  if (data.value && data.value.user_id != user.value?.id) {
    if (data.value.editable) {
      if (
        !confirm(
          "Анкета редактируется другим пользователем. Переключить режим?",
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
    "/routes/status/" + candId.value,
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
  <UContainer>
    <UPageHeader
      :title="`${data?.surname} ${data?.firstname} ${data?.patronymic ?? ''}`"
      :ui="{ title: 'text-red-800' }"
    >
      <template #links>
        <ClientOnly>
          <!-- Кнопки переключения режима редактирования -->
          <div v-if="user?.role == 'user'" class="flex items-center space-x-4">
            <UButton
              variant="outline"
              :loading="status === 'pending'"
              :color="
                !data?.editable
                  ? 'secondary'
                  : data.user_id == user?.id
                    ? 'success'
                    : 'error'
              "
              :label="
                !data?.editable
                  ? 'Доступно'
                  : data.user_id == user?.id
                    ? 'Изменение'
                    : 'Закрыто'
              "
              :icon="
                !data?.editable
                  ? 'i-lucide-lock-open'
                  : data.user_id == user?.id
                    ? 'i-lucide-edit'
                    : 'i-lucide-lock'
              "
              @click="switchStatus"
            />
          </div>
        </ClientOnly>
      </template>
    </UPageHeader>
    <ContentTabsView />
  </UContainer>
</template>
