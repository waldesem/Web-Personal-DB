<script setup lang="ts">
const toasts = useToasts();

const person = usePersonStore();

const session = useSessionStore();

// Определяем функцию для получения данных из API
const { status, refresh } = await useAsyncData("person", () =>
  person.getPerson(),
);

// Определяем функцию для переключения режима редактирования
async function switchStatus(): Promise<void> {
  if (person.data && person.data.user_id != session.user?.id) {
    if (person.data.locked) {
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
  const response = await person.switchStatus();
  status.value = "success";
  if (response?.status == 200) {
    refresh();
  } else {
    toasts.create();
  }
}
</script>

<template>
  <UContainer>
    <UPageHeader
      :title="`${person.data.surname} ${person.data.firstname} ${person.data.patronymic ?? ''}`"
      :ui="{ title: 'text-red-800' }"
    >
      <template #links>
        <!-- Кнопки переключения режима редактирования -->
        <div
          v-if="session.user?.role == 'user' && !person.data.locked"
          class="flex items-center space-x-4"
        >
          <UButton
            variant="outline"
            :loading="status === 'pending'"
            :color="
              !person.data.locked
                ? 'secondary'
                : person.data.user_id == session.user?.id
                  ? 'success'
                  : 'error'
            "
            :label="
              !person.data.locked
                ? 'Доступно'
                : person.data.user_id == session.user?.id
                  ? 'Изменение'
                  : 'Закрыто'
            "
            :icon="
              !person.data.locked
                ? 'i-lucide-lock-open'
                : person.data.user_id == session.user?.id
                  ? 'i-lucide-edit'
                  : 'i-lucide-lock'
            "
            @click="switchStatus"
          />
        </div>
      </template>
    </UPageHeader>
    <ContentTabsView />
  </UContainer>
</template>
