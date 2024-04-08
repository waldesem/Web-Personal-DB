<script setup lang="ts">
import { computed, onBeforeMount, ref, defineAsyncComponent } from "vue";
import { classifyStore } from "@/store/classify";
import { authStore } from "@/store/auth";
import { server } from "@/utilities/utils";

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

const storeAuth = authStore();
const storeClassify = classifyStore();

const todayDate = new Date();

const tableData = ref({
  header: "",
  stat: {
    region_id: 1,
    checks: [],
    start: new Date(todayDate.getFullYear(), todayDate.getMonth(), 1)
      .toISOString()
      .slice(0, 10),
    end: todayDate.toISOString().slice(0, 10),
  },
});

async function submitData(): Promise<void> {
  try {
    const response = await storeAuth.axiosInstance.get(
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
      storeClassify.classData.regions[tableData.value.stat.region_id];
  } catch (error) {
    console.log(error);
  }
}

onBeforeMount(async () => {
  await submitData();
});

computed(() => {
  tableData.value.header =
    storeClassify.classData.regions[tableData.value.stat.region_id];
});
</script>

<template>
  <div class="container py-3">
    <div class="row mb-3">
      <HeaderDiv
        :page-header="`Статистика по региону ${tableData.header} 
                за период c ${tableData.stat.start} по ${tableData.stat.end} г.`"
      />
    </div>
    <div class="py-3">
      <TableSlots
        :class="'table table-hover table-responsive align-middle'"
        :tbl-caption="'Решения по кандидатам'"
      >
        <template v-slot:thead>
          <tr>
            <th width="45%">Решение</th>
            <th>Количество</th>
          </tr>
        </template>
        <template v-slot:tbody>
          <tr
            height="50px"
            v-for="(value, index) in Object.keys(tableData.stat.checks)"
            :key="index"
          >
            <td>{{ value }}</td>
            <td>{{ Object.values(tableData.stat.checks)[index] }}</td>
          </tr>
        </template>
      </TableSlots>
    </div>

    <div class="row mb-3 ">
      <label class="col-form-label col-md-1" for="region">
        Регион:
      </label>
      <div class="col-md-3">
        <SelectObject
          :name="'region'"
          :select="storeClassify.classData.regions"
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
  </div>
</template>
