<script setup lang="ts">
// import { useFileSystemAccess } from '@vueuse/core'

interface Query {
  status: string;
  message: string;
  result: Record<string, string>[];
}

const { $api } = useNuxtApp();

const globalFilter = ref();
const query = ref("");

const { data: tables } = await useLazyAsyncData("metadata", () =>
  $api<{ [key: string]: [key: string] }>("/routes/metadata")
);

const { data, status, refresh } = await useLazyAsyncData(
  "query",
  () =>
    $api<Query>("/routes/query", {
      method: "POST",
      body: {
        query: query.value,
      },
    }),
  { immediate: false }
);

const validate = () => {
  const errors = [];
  if (!query.value)
    errors.push({ name: "query", message: "Введите SQl-запрос" });
  if (!query.value.toLowerCase().startsWith("select"))
    errors.push({
      name: "query",
      message: "Запрос должен быть в формате: SELECT * FROM persons",
    });
  return errors;
};

function saveJSON() {
  const dataToSave = JSON.stringify(data.value?.result, null, 2);
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

const tabs = computed(() => {
  if (tables.value) {
    Object.keys(tables.value).map((table) => {
      return { label: table };
    });
  }
  return [{ label: "" }];
});
</script>

<template>
  <UPage>
    <UPageHeader
      title="Расширенный запрос"
      :ui="{
        root: 'relative border-none py-4',
        title: 'text-2xl sm:text-3xl text-gray-800',
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

    <UCollapsible v-if="tables">
      <UButton
        class="group"
        label="Показать структуру"
        color="neutral"
        variant="subtle"
        trailing-icon="i-lucide-chevron-down"
        block
        :ui="{
          trailingIcon:
            'group-data-[state=open]:rotate-180 transition-transform duration-200',
        }"
      />
      <template #content>
        <UTabs v-if="tabs && tabs[0]?.label" :items="tabs" variant="link">
          <template #content="{ item }">
            <div v-if="data" class="px-4">
              <div
                v-for="(value, key) in data.result[item.label as keyof typeof data.result]"
                :key="key"
              >
                <ElementsLabelValue :label="key" :value="value" />
              </div>
            </div>
          </template>
        </UTabs>
      </template>
    </UCollapsible>

    <UAlert
      v-if="data?.status === 'error'"
      :description="data?.message"
      color="error"
      icon="i-lucide-terminal"
      title="Error"
      variant="subtle"
      close
    />

    <UCard v-else class="mt-4">
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
        :data="data?.result"
      />
    </UCard>
  </UPage>
</template>
