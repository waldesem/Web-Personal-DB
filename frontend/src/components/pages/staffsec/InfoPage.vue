<script setup lang="ts">
import { onBeforeMount, ref, defineAsyncComponent } from "vue";
import { stateClassify, stateUser } from "@/state";
import { axiosAuth } from "@/auth";
import { server } from "@/utilities";
import { AxiosError } from "axios";
import { router } from "@/router";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/content/elements/HeaderDiv.vue")
);
const SelectDiv = defineAsyncComponent(
  () => import("@components/content/elements/SelectDiv.vue")
);
const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const TableSlots = defineAsyncComponent(
  () => import("@components/content/elements/TableSlots.vue")
);

const todayDate = new Date();

const tableData = ref({
  stat: {
    region: stateClassify.regions['main'],
    checks: <Record<string, any>>{},
    start: new Date(todayDate.getFullYear(), todayDate.getMonth(), 1)
      .toISOString()
      .slice(0, 10),
    end: todayDate.toISOString().slice(0, 10),
  },
});
async function submitData(): Promise<void> {
  try {
    const response = await axiosAuth.get(`${server}/information`, {
      params: {
        start: tableData.value.stat.start,
        end: tableData.value.stat.end,
        region: tableData.value.stat.region,
      },
    });
    tableData.value.stat.checks = response.data;
  } catch (error: AxiosError | any) {
    if (error.request.status == 401 || error.request.status == 403) {
      router.push({ name: "login" });
    } else {
      console.error(error);
    }
  }
}

onBeforeMount(async () => {
  await submitData();
});
</script>

<template>
  <HeaderDiv
    :page-header="`Статистика по региону ${tableData.stat.region} 
            за период c ${tableData.stat.start} по ${tableData.stat.end} г.`"
  />
  <TableSlots :class="'table table-hover table-responsive align-middle py-3'">
    <template v-slot:caption>{{ `Решения по кандидатам` }}</template>
    <template v-slot:thead>
      <tr>
        <th width="45%">Решение</th>
        <th>Количество</th>
      </tr>
    </template>
    <template v-slot:tbody>
      <tr v-for="(key, value) in tableData.stat.checks" :key="key">
        <td>{{ key }}</td>
        <td>{{ value }}</td>
      </tr>
    </template>
  </TableSlots>

  <div class="row mb-3">
    <label class="col-form-label col-md-1" for="region"> Регион: </label>
    <div class="col-md-3">
      <SelectDiv
        :place="'Регион'"
        :name="'region'"
        :select="stateClassify.regions"
        :disable="!stateUser.hasAdmin"
        v-model="tableData.stat.region"
        @submit-data="submitData"
      />
    </div>
    <label class="col-form-label col-md-1" for="start"> Период: </label>
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
