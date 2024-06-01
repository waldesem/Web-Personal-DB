<script setup lang="ts">
import { computed, onBeforeMount, ref, defineAsyncComponent } from "vue";
import { stateClassify } from "@/state";
import { axiosAuth } from "@/auth";
import { server } from "@/utilities";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/content/elements/HeaderDiv.vue")
);
const SelectObject = defineAsyncComponent(
  () => import("@components/content/elements/SelectObject.vue")
);
const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const TableSlots = defineAsyncComponent(
  () => import("@components/content/elements/TableSlots.vue")
);

const todayDate = new Date();

const tableData = ref({
  header: "",
  stat: {
    region_id: 1,
    checks: <Record<string, any>>{},
    start: new Date(todayDate.getFullYear(), todayDate.getMonth(), 1)
      .toISOString()
      .slice(0, 10),
    end: todayDate.toISOString().slice(0, 10),
  },
});
async function submitData(): Promise<void> {
  try {
    const response = await axiosAuth.get(
      `${server}/information`,
      {
        params: {
          start: tableData.value.stat.start,
          end: tableData.value.stat.end,
          region_id: tableData.value.stat.region_id,
        },
      }
    );
    tableData.value.stat.checks = response.data;
    tableData.value.header =
      stateClassify.regions[tableData.value.stat.region_id];
  } catch (error) {
    console.log(error);
  }
}

onBeforeMount(async () => {
  await submitData();
});

computed(() => {
  tableData.value.header =
    stateClassify.regions[tableData.value.stat.region_id];
});
</script>

<template>
  <HeaderDiv
    :page-header="`Статистика по региону ${tableData.header} 
            за период c ${tableData.stat.start} по ${tableData.stat.end} г.`"
  />
  <TableSlots
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
      <tr
        v-for="(key, value) in tableData.stat.checks"
        :key="key"
      >
        <td>{{ stateClassify.conclusions[key] }}</td><td>{{ value }}</td>
      </tr>
    </template>
  </TableSlots>

  <div class="row mb-3 ">
    <label class="col-form-label col-md-1" for="region">
      Регион:
    </label>
    <div class="col-md-3">
      <SelectObject
        :name="'region'"
        :select="stateClassify.regions"
        v-model="tableData.stat.region_id"
        @submit-data="submitData"
      />
    </div>
    <label class="col-form-label col-md-1" for="start">
      Период:
    </label>
    <div class="col-md-2">
      <InputElement 
        :name="'start'" 
        :typeof="'date'"
        v-model="tableData.stat.start" 
        @submit-data="submitData"
        />
    </div>
    <div class="col-md-2">
      <InputElement 
        :name="'end'" 
        :typeof="'date'"
        v-model="tableData.stat.end" 
        @submit-data="submitData"
        />
    </div>
  </div>
</template>
