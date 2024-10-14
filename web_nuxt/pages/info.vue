<script setup lang="ts">
import { useDateFormat, useNow } from "@vueuse/core";

const authFetch = useFetchAuth();
const userState = useUserState();

const region = ref(userState.value.region);
const start = ref(useDateFormat(useNow(), "YYYY-MM").value + "-01");
const end = ref(useDateFormat(useNow(), "YYYY-MM-DD").value);
const stat = ref([] as Record<string, string>[]);

/**
 * Get statistics from server
 */
const { status } = await useLazyAsyncData(
  "stats",
  async () => {
    const response = await authFetch("/api/information", {
      params: {
        start: start.value,
        end: end.value,
        region: region.value,
      },
    });
    stat.value = response as Record<string, string>[];
  },
  {
    watch: [region, start, end],
  }
);
</script>

<template>
  <div>
    <ElementsHeaderDiv
      :div="'py-1'"
      :header="`Информация по региону ${region} за период с ${start} г. по ${end} г.`"
    />
    <div class="my-8">
      <UTable
        :loading="status == 'pending'"
        :progress="{ color: 'red', animation: 'swing' }"
        :empty-state="{
          icon: 'i-heroicons-circle-stack-20-solid',
          label: 'Статистика за указанный период отсутствует.',
        }"
        :rows="(stat as Record<string, string>[])"
        :columns="[
          { key: 'conclusion', label: 'Решение' },
          { key: 'count', label: 'Количество' },
        ]"
      />
      <div class="flex grid grid-cols-12 gap-3 mt-8">
        <div class="col-span-2">
          <UFormGroup class="mb-3" label="Регион">
            <USelect
              v-model="region"
              :disabled="userState.region != 'Главный офис'"
              :options="[
                'Главный офис',
                'РЦ Юг',
                'РЦ Запад',
                'РЦ Урал',
                'РЦ Восток',
              ]"
            />
          </UFormGroup>
        </div>
        <div class="col-span-2">
          <div class="px-3">
            <UFormGroup label="Начало периода">
              <UInput v-model="start" type="date" />
            </UFormGroup>
          </div>
        </div>
        <div class="col-span-2">
          <div class="px-3">
            <UFormGroup label="Конец периода">
              <UInput v-model="end" type="date" />
            </UFormGroup>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
