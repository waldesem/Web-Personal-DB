<script setup lang="ts">
import { Roles, type Person } from "@/types";

const { $api } = useNuxtApp();

const session = useSessionStore();

const lock = useLock();

const personId = computed(() => useRoute().params.id as string);

const { data, status, refresh } = await useAsyncData<Person>(
  "person",
  () => $api<Person>("/routes/persons/" + personId.value),
  { default: () => ({}) as Person },
);

// Определяем функцию для переключения режима редактирования
async function switchStatus(): Promise<void> {
  if (session.user?.id !== data.value.user_id) {
    if (!confirm("Анкета значится за другим пользователем. Продолжить?")) {
      return;
    }
    status.value = "pending";
    await $api.raw("/routes/persons/status/" + personId.value);
    await refresh();
    lock.value = false;
  } else {
    lock.value = !lock.value;
  }
}
</script>

<template>
  <UContainer>
    <UPageHeader
      :title="
        `${data.surname} ${data.firstname} ${data.patronymic ?? ''}`.trimEnd()
      "
      :ui="{ title: 'text-red-800' }"
    >
      <template #links>
        <!-- Кнопки переключения режима редактирования -->
        <div
          v-if="session.user?.role === Roles.user"
          class="flex items-center space-x-4"
        >
          <UButton
            variant="outline"
            :loading="status === 'pending'"
            :color="
              session.user?.id !== data.user_id
                ? 'error'
                : lock
                  ? 'secondary'
                  : 'success'
            "
            :label="
              session.user?.id !== data.user_id
                ? 'Закрыто'
                : lock
                  ? 'Доступно'
                  : 'Изменение'
            "
            :icon="
              session.user?.id !== data.user_id
                ? 'i-lucide-lock'
                : lock
                  ? 'i-lucide-lock-open'
                  : 'i-lucide-edit'
            "
            @click="switchStatus"
          />
        </div>
      </template>
    </UPageHeader>
    <ContentTabsView :person="data" />
  </UContainer>
</template>
