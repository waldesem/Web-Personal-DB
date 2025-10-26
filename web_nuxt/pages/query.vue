<script setup lang="ts">
const { $api } = useNuxtApp();

 const query = ref("");

const globalFilter = ref();

const { data, status, refresh } = useLazyAsyncData(
  async () => {
    const response = (await $api("/routes/query", {
      query: {
        query: query.value,
      },
    })) as Record<string, string>[];
    return response;
  },
  { immediate: false }
);

const validate = () => {
  const errors = [];
  if (!query.value) errors.push({ name: "query", message: "Введите SQl-запрос" });
  if (!query.value.toLowerCase().startsWith("select"))
    errors.push({
      name: "query",
      message: "Запрос должен начинаться SELECT...",
    });
  return errors;
};

async function saveJSON() {
  const dataToSave = JSON.stringify(data.value, null, 2);
  const blob = new Blob([dataToSave], { type: "application/json" });
  const url = URL.createObjectURL(blob);

  const link = document.createElement("a");
  link.href = url;
  link.download = "data.json";
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}
</script>

<template>
  <UPage>
    <UPageHeader
      title="Расширенный запрос"
      :ui="{
        root: 'relative border-none py-4',
        title: 'text-2xl sm:text-3xl text-red-800',
      }"
    />
    <!-- Строка поиска -->
    <UForm
      :validate="validate"
      :state="query"
      class="my-6"
      @submit.prevent="refresh"
    >
    <UFormField name="query">
      <UInput
        id="query"
        v-model="query"
        type="search"
        size="lg"
        placeholder="SQL-Запрос на выборку информации из базы данных"
        :ui="{ trailing: 'pr-0.5' }"
      >
        <template #trailing>
          <UButton variant="ghost" icon="i-lucide-search" type="submit" />
        </template>
      </UInput>
      </UFormField>
    </UForm>

    <UCard>
      <template #header>
        <div class="flex justify-between">
          <UInput
            v-model="globalFilter"
            class="max-w-sm"
            placeholder="Найти в таблице"
          />
          <UButton
            icon="i-lucide-save"
            variant="outline"
            label="Сохранить в JSON"
            @click="saveJSON()"
          />
        </div>
      </template>
      <UTable
        v-model:global-filter="globalFilter"
        loading-animation="swing"
        empty="Данные не найдены"
        sticky="header"
        :loading="status === 'pending'"
        :loading-color="'neutral'"
        :data="data"
    /></UCard>
  </UPage>
</template>
