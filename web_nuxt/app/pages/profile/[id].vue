<script setup lang="ts">
import { Roles, type Person } from "@/types";

const { $api } = useNuxtApp();

const session = useSessionStore();

const personId = computed(() => useRoute().params.id as string);

provide("personId", personId);

// Определяем функцию для получения данных из API
const { data, status, refresh } = await useAsyncData<Person>(
  "person",
  () => $api<Person>("/routes/persons/" + personId.value),
  { default: () => ({}) as Person },
);

provide("person", data);

const lock = ref(true);

const locked = computed(() => {
  return lock.value || session.user?.id !== data.value.user_id;
});

provide("locked", locked);

// Определяем функцию для переключения режима редактирования
async function switchStatus(): Promise<void> {
  status.value = "pending";
  if (session.user?.id !== data.value.user_id) {
    if (!confirm("Анкета значится за другим пользователем. Продолжить?")) {
      return;
    }
    await $api.raw("/routes/persons/status/" + personId.value);
    await refresh();
  }
  lock.value = !lock.value;
  status.value = "success";
}
</script>

<template>
  <UContainer>
    <UPageHeader
      :title="`${data.surname} ${data.firstname} ${data.patronymic ?? ''}`"
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
            :color="!locked ? 'success' : !lock ? 'secondary' : 'error'"
            :label="!locked ? 'Доступно' : !lock ? 'Изменение' : 'Закрыто'"
            :icon="
              !locked
                ? 'i-lucide-lock-open'
                : !lock
                  ? 'i-lucide-edit'
                  : 'i-lucide-lock'
            "
            @click="switchStatus"
          />
        </div>
      </template>
    </UPageHeader>
    <ContentTabsView :person="data" />
  </UContainer>
</template>
