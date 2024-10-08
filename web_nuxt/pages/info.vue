<script setup lang="ts">
import { useDateFormat, useNow } from "@vueuse/core";

const authFetch = useFetchAuth();
const userState = useUserState();

const tableData = ref({
  region: userState.value.region,
  start: useDateFormat(useNow(), "YYYY-MM").value + "-01",
  end: useDateFormat(useNow(), "YYYY-MM-DD").value,
  stat: [] as Record<string, string>[],
});

/**
 * Get statistics from server
 */
const { refresh, status } = await useLazyAsyncData("stats", async () => {
  const response = await authFetch("/api/information", {
    params: {
      start: tableData.value.start,
      end: tableData.value.end,
      region: tableData.value.region,
    },
  });
  tableData.value.stat = response as Record<string, string>[];
});
</script>

<template>
  <div>
    <ElementsHeaderDiv
      :div="'py-1'"
      :header="`Информация по региону ${tableData.region} за период с ${tableData.start} г. по ${tableData.end} г.`"
    />
    <div class="my-8">
      <UTable
        :loading="status == 'pending'"
        :progress="{ color: 'red', animation: 'swing' }"
        :empty-state="{
          icon: 'i-heroicons-circle-stack-20-solid',
          label: 'Статистика за указанный период отсутствует.',
        }"
        :rows="(tableData.stat as Record<string, string>[])"
        :columns="[
          { key: 'conclusion', label: 'Решение' },
          { key: 'count', label: 'Количество' },
        ]"
      />
      <div class="flex grid grid-cols-12 gap-3 mt-8">
        <div class="col-span-2">
          <UFormGroup class="mb-3" label="Регион">
            <USelect
              v-model="tableData.region"
              :disabled="userState.region != 'Главный офис'"
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
            <UFormGroup label="Начало периода">
              <UInput v-model="tableData.start" type="date" @change="refresh" />
            </UFormGroup>
          </div>
        </div>
        <div class="col-span-2">
          <div class="px-3">
            <UFormGroup label="Конец периода">
              <UInput v-model="tableData.end" type="date" @change="refresh" />
            </UFormGroup>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
