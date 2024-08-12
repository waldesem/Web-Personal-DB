<script setup lang="ts">
import { onBeforeMount, ref } from "vue";
import { server, stateClassify, stateUser } from "@/state/state";
import { useFetchAuth } from "@/utils/auth";

const classifyState = stateClassify();
const userState = stateUser();
const todayDate = new Date();

const tableData = ref({
  region: userState.user.value.region,
  checks: <Array<any>>[],
  start: new Date(todayDate.getFullYear(), todayDate.getMonth(), 1)
    .toISOString()
    .slice(0, 10),
  end: todayDate.toISOString().slice(0, 10),
});

async function submitData(): Promise<void> {
  try {
    const authFetch = useFetchAuth();
    const data = await authFetch(`${server}/information`, {
      params: {
        start: tableData.value.start,
        end: tableData.value.end,
        region: tableData.value.region,
      },
    });
    tableData.value.checks = data as unknown as Array<any>;
  } catch (error: any) {
    console.error(error);
  }
}

onBeforeMount(async () => {
  await submitData();
});
</script>

<template>
  <LayoutsMenu>
    <div class="py-8">
      <h3 class="text-2xl text-red-800 font-bold">
        {{
          `Информация по региону ${tableData.region} 
            за период c ${tableData.start} по ${tableData.end} г.`
        }}
      </h3>
    </div>
    <UTable :rows="tableData.checks" :columns="['Решение', 'Количество']">
      <template #caption>
        <caption class="text-left">Решения по кандидатам</caption>
      </template>
    </UTable>
    <div class="flex grid grid-cols-12 gap-3 mt-4">
      <div class="col-span-2">
        <UFormGroup class="mb-3" size="md" label="Регион">
          <USelect
            :disable="
              userState.user.value.region !=
              classifyState.classes.value.regions['main']
            "
            v-model="tableData.region"
            :options="Object.values(classifyState.classes.value.regions)"
            @submit-data="submitData"
          />
        </UFormGroup>
      </div>
      <div class="flex col-span-2">
        <div class="grid grid-cols-2 gap-3">
          <div class="col-span-1">
            <UFormGroup size="md" label="Начало периода">
              <UInput
                v-model="tableData.start"
                type="date"
                @submit-data="submitData"
              />
            </UFormGroup>     
          </div>     
          <div class="col-span-1">
            <UFormGroup size="md" label="Конец периода">
              <UInput
                v-model="tableData.end"
                type="date"
                @submit-data="submitData"
              />
            </UFormGroup>
          </div>
        </div>
      </div>
    </div>
  </LayoutsMenu>
</template>
