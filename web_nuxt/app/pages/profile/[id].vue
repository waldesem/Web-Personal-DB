<script setup lang="ts">
const person = usePersonStore();

const personId = computed(() => useRoute().params.id as string);

// Определяем функцию для получения данных из API
const { status } = await useAsyncData("person", () =>
  person.getPerson(personId.value),
);

// Определяем функцию для переключения режима редактирования
async function switchStatus(): Promise<void> {
  status.value = "pending";
  await person.switchStatus();
  status.value = "success";
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
        <div v-if="!person.blocked" class="flex items-center space-x-4">
          <UButton
            variant="outline"
            :loading="status === 'pending'"
            :color="
              !person.locked ? 'success' : !person.lock ? 'secondary' : 'error'
            "
            :label="
              !person.locked
                ? 'Доступно'
                : !person.lock
                  ? 'Изменение'
                  : 'Закрыто'
            "
            :icon="
              !person.locked
                ? 'i-lucide-lock-open'
                : !person.lock
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
