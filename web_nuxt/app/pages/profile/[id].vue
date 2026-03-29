<script setup lang="ts">
const personStore = usePersonStore();

const session = useSessionStore();

const toasts = useToasts();

// Определяем функцию для получения данных из API
const { status, refresh } = await useAsyncData("person", () =>
  personStore.getPerson(),
);

// Определяем функцию для переключения режима редактирования
async function switchStatus(): Promise<void> {
  if (personStore.person && personStore.person.user_id != session.user?.id) {
    if (personStore.person.editable) {
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
  const response = await personStore.switchStatus();
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
      :title="`${personStore.person.surname} ${personStore.person.firstname} ${personStore.person.patronymic ?? ''}`"
      :ui="{ title: 'text-red-800' }"
    >
      <template #links>
        <!-- Кнопки переключения режима редактирования -->
        <div
          v-if="session.user?.role == 'user' && !personStore.person.locked"
          class="flex items-center space-x-4"
        >
          <UButton
            variant="outline"
            :loading="status === 'pending'"
            :color="
              !personStore.person.editable
                ? 'secondary'
                : personStore.person.user_id == session.user?.id
                  ? 'success'
                  : 'error'
            "
            :label="
              !personStore.person.editable
                ? 'Доступно'
                : personStore.person.user_id == session.user?.id
                  ? 'Изменение'
                  : 'Закрыто'
            "
            :icon="
              !personStore.person.editable
                ? 'i-lucide-lock-open'
                : personStore.person.user_id == session.user?.id
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
