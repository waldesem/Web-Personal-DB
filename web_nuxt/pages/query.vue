<script setup lang="ts">
const { $api } = useNuxtApp();

const query = ref("");
const items = ref([]) as Ref<Record<string, string>[]>;
const globalFilter = ref();

const { data, status } = useLazyAsyncData(async () => {
  const response = (await $api("/routes/metadata", {
    query: {
      query: query.value,
    },
  })) as Ref<{ [key: string]: [key: string] }>;
  return response;
});

async function onSubmit() {
  status.value = "pending";
  const response = (await $api("/routes/query", {
    query: {
      query: query.value,
    },
  })) as Record<string, string>[];
  items.value = response;
  status.value = "success";
}

const validate = () => {
  const errors = [];
  if (!query.value)
    errors.push({ name: "query", message: "Введите SQl-запрос" });
  if (!query.value.toLowerCase().startsWith("select"))
    errors.push({
      name: "query",
      message: "Запрос должен начинаться SELECT...",
    });
  return errors;
};

async function saveJSON() {
  const dataToSave = JSON.stringify(items.value, null, 2);
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
  if (data.value) {
    Object.keys(data.value).map((table) => {
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
      @submit.prevent="onSubmit"
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

    <UCollapsible v-if="data" label="Таблица данных">
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
        <UTabs v-if="tabs" :items="tabs" variant="link">
          <template #content="{ item }">
            <div class="px-4">
              <div
                v-for="(value, key) in data[item['label'] as keyof typeof data]"
                :key="key"
              >
                {{ key }} - {{ value }}
              </div>
            </div>
          </template>
        </UTabs>
      </template>
    </UCollapsible>

    <UCard class="mt-4">
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
        :data="items"
    /></UCard>
  </UPage>
</template>
