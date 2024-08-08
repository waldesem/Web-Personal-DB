<script setup lang="ts">
import { onBeforeMount, ref } from "vue";
import { server, stateClassify, stateUser } from "@/state/state";

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
    const { data } = await useLazyFetch(`${server}/information`, {
      onRequest({request, options}) {
          options.headers = {
            Authorization: `Bearer ${localStorage.getItem("user_token")}`,
          };
        },
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
    <ElementsHeaderDiv
      :page-header="`Статистика по региону ${tableData.region} 
            за период c ${tableData.start} по ${tableData.end} г.`"
    />
    <ElementsTableSlots
      :class="'table table-hover table-responsive align-middle py-3'"
    >
      <template v-slot:caption>{{ `Решения по кандидатам` }}</template>
      <template v-slot:thead>
        <tr>
          <th width="45%">Решение</th>
          <th>Количество</th>
        </tr>
      </template>
      <template v-slot:tbody>
        <tr v-for="(row, idx) in tableData.checks" :key="idx">
          <td>{{ row[0] }}</td>
          <td>{{ row[1] }}</td>
        </tr>
      </template>
    </ElementsTableSlots>

    <div class="row mb-3">
      <label class="col-form-label col-md-1" for="region"> Регион: </label>
      <div class="col-md-3">
        <ElementsSelectDiv
          :place="'Регион'"
          :name="'region'"
          :select="classifyState.classes.value.regions"
          :disable="
            userState.user.value.region !=
            classifyState.classes.value.regions['main']
          "
          v-model="tableData.region"
          @submit-data="submitData"
        />
      </div>
      <label class="col-form-label col-md-1" for="start"> Период: </label>
      <div class="col-md-2">
        <ElementsInputElement
          :name="'start'"
          :typeof="'date'"
          v-model="tableData.start"
          @submit-data="submitData"
        />
      </div>
      <div class="col-md-2">
        <ElementsInputElement
          :name="'end'"
          :typeof="'date'"
          v-model="tableData.end"
          @submit-data="submitData"
        />
      </div>
    </div>
  </LayoutsMenu>
</template>
