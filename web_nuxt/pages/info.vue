<script setup lang="ts">
import { server, stateClassify, stateUser } from "@/state/state";
import { useFetchAuth } from "@/utils/auth";

const classifyState = stateClassify();
const userState = stateUser();
const todayDate = new Date();

const tableData = ref({
  region: userState.user.value.region,
  checks: [] as Array<unknown>,
  start: new Date(todayDate.getFullYear(), todayDate.getMonth(), 1)
    .toISOString()
    .slice(0, 10),
  end: todayDate.toISOString().slice(0, 10),
});

/**
 * Get statistics from server
 */
async function getStatData(): Promise<void> {
  const authFetch = useFetchAuth();
  tableData.value.checks = (await authFetch(`${server}/information`, {
    params: {
      start: tableData.value.start,
      end: tableData.value.end,
      region: tableData.value.region,
    },
  })) as Array<unknown>;
}

await getStatData();
</script>

<template>
  <LayoutsMenu>
    <div class="my-14">
    <UTable :rows="tableData.checks" :columns="['Решение', 'Количество']">
      <template #caption>
        <caption class="text-left">
          {{
          `Информация по региону ${tableData.region} 
            за период c ${tableData.start} по ${tableData.end} г.`
        }}
        </caption>
      </template>
    </UTable>
    <div class="flex grid grid-cols-12 gap-3 mt-4">
      <div class="col-span-2">
        <UFormGroup class="mb-3" size="md" label="Регион">
          <USelect
            v-model="tableData.region"
            :disable="
              userState.user.value.region !=
              classifyState.classes.value.regions['main']
            "
            :options="Object.values(classifyState.classes.value.regions)"
            @submit-data="getStatData"
          />
        </UFormGroup>
      </div>
      <div class="flex col-span-2">
        <div class="px-3">
          <UFormGroup size="md" label="Начало периода">
            <UInput
              v-model="tableData.start"
              type="date"
              @submit-data="getStatData"
            />
          </UFormGroup>
        </div>
        <div class="px-3">
          <UFormGroup size="md" label="Конец периода">
            <UInput
              v-model="tableData.end"
              type="date"
              @submit-data="getStatData"
            />
          </UFormGroup>
        </div>
      </div>
    </div>
    </div>
  </LayoutsMenu>
</template>
