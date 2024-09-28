<script setup lang="ts">

const authFetch = useFetchAuth();
const userState = stateUser();
const todayDate = new Date();

const tableData = ref({
  region: userState.value.region,
  start: new Date(todayDate.getFullYear(), todayDate.getMonth(), 1)
    .toISOString()
    .slice(0, 10),
  end: todayDate.toISOString().slice(0, 10),
});

/**
 * Get statistics from server
 */
const { refresh, data, status } = await useLazyAsyncData(
  "statistics",
  async () => {
    const stat = await authFetch("/api/information", {
      params: {
        start: tableData.value.start,
        end: tableData.value.end,
        region: tableData.value.region,
      },
    });
    return stat;
  }
);
</script>

<template>
  <div>
    <ElementsHeaderDiv
      :div="'py-1'"
      :header="`Информация по региону ${tableData.region.toLocaleUpperCase()} за период с ${new Date(
        tableData.start
      ).toLocaleDateString()} г. по ${new Date(
        tableData.end
      ).toLocaleDateString()} г.`"
    />
    <div class="my-8">
      <UTable
        :loading="status == 'pending'"
        :progress="{ color: 'red', animation: 'swing' }"
        :empty-state="{
          icon: 'i-heroicons-circle-stack-20-solid',
          label: 'Статистика за указанный период отсутствует.',
        }"
        :rows="(data as Record<string, string>[])"
        :columns="[
          { key: 'conclusion', label: 'Решение' },
          { key: 'count', label: 'Количество' },
        ]"
      />
      <div class="flex grid grid-cols-12 gap-3 mt-8">
        <div class="col-span-2">
          <UFormGroup class="mb-3" size="md" label="Регион">
            <USelect
              v-model="tableData.region"
              :disable="userState.region != 'main'"
              :options="[
                'Главный офис',
                'РЦ Юг',
                'РЦ Запад',
                'РЦ Урал',
                'РЦ Восток',
              ]"
              @change="refresh"
            />
          </UFormGroup>
        </div>
        <div class="col-span-2">
          <div class="px-3">
            <UFormGroup size="md" label="Начало периода">
              <UInput v-model="tableData.start" type="date" @change="refresh" />
            </UFormGroup>
          </div>
        </div>
        <div class="col-span-2">
          <div class="px-3">
            <UFormGroup size="md" label="Конец периода">
              <UInput v-model="tableData.end" type="date" @change="refresh" />
            </UFormGroup>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
