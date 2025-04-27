<script setup lang="ts">

const region = ref(stateUser.value.region);
const start = ref(new Date().toISOString().split("T")[0].slice(0, 8) + "01");
const end = ref(new Date().toISOString().split("T")[0]);
const stat = ref([] as Record<string, string>[]);

/**
 * Get statistics from server
 */
const { status } = await useLazyAsyncData(
  "stats",
  async () => {
    stat.value = (await useFetchAuth("/route/info", {
      params: {
        start: start.value,
        end: end.value,
        region: region.value,
      },
    })) as Record<string, string>[];
  },
  {
    watch: [region, start, end],
  }
);
</script>

<template>
  <div class="mb-6">
    <div class="py-1">
      <h3 class="text-2xl text-red-800 font-bold">
        {{
          `Информация по региону ${region} за период с ${start} г. по ${end} г.`
        }}
      </h3>
    </div>
    <div class="my-6">
      <UTable
        :loading="status == 'pending'"
        :progress="{ color: 'red', animation: 'swing' }"
        :empty-state="{
          icon: 'i-heroicons-circle-stack-20-solid',
          label: 'Статистика за указанный период отсутствует.',
        }"
        :data="(stat as Record<string, string>[])"
        :columns="[
          { accessorKey: 'conclusion', header: 'Решение' },
          { accessorKey: 'count', header: 'Количество' },
        ]"
      />
      <div class="flex grid grid-cols-12 gap-3 mt-8">
        <div class="col-span-2">
          <UFormField class="mb-3" label="Регион">
            <USelect
              v-model="region"
              :items="[
                'Главный офис',
                'РЦ Юг',
                'РЦ Запад',
                'РЦ Урал',
                'РЦ Восток',
              ]"
              :placeholder="stateUser.region"
            />
          </UFormField>
        </div>
        <div class="col-span-2">
          <div class="px-3">
            <UFormField label="Начало периода">
              <UInput v-model="start" type="date" />
            </UFormField>
          </div>
        </div>
        <div class="col-span-2">
          <div class="px-3">
            <UFormField label="Конец периода">
              <UInput v-model="end" type="date" />
            </UFormField>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
