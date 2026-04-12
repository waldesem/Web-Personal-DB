<script setup lang="ts">
import { Roles, type Person } from "@/types";

const { $api } = useNuxtApp();

const session = useSessionStore();

const personId = computed(() => useRoute().params.id as string);

const { data, status, refresh } = await useAsyncData<Person>(
  "person",
  () => $api<Person>("/routes/persons/" + personId.value),
  { default: () => ({}) as Person },
);

const lock = ref(true);

const locked = computed(() => {
  return lock.value && session.user?.id !== data.value.user_id;
});

provide("lock", lock);

// Определяем функцию для переключения режима редактирования
async function switchStatus(): Promise<void> {
  if (session.user?.id !== data.value.user_id) {
    if (!confirm("Анкета значится за другим пользователем. Продолжить?")) {
      return;
    }
    status.value = "pending";
    await $api.raw("/routes/persons/status/" + personId.value);
    await refresh();
  }
  lock.value = !lock.value;
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
            :color="locked ? 'error' : lock ? 'secondary' : 'success'"
            :label="locked ? 'Закрыто' : lock ? 'Доступно' : 'Изменение'"
            :icon="
              locked
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
