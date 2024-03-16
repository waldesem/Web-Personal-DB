<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount } from "vue";
import { classifyStore } from "@store/classify";
import { authStore } from "@/store/auth";
import { alertStore } from "@store/alert";
import { debounce, server } from "@utilities/utils";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/layouts/HeaderDiv.vue")
);
const SelectDiv = defineAsyncComponent(
  () => import("@components/elements/SelectDiv.vue")
);
const InputLabel = defineAsyncComponent(
  () => import("@components/elements/InputLabel.vue")
);
const TableSlots = defineAsyncComponent(
  () => import("@components/elements/TableSlots.vue")
);
const PageSwitcher = defineAsyncComponent(
  () => import("@components/layouts/PageSwitcher.vue")
);

const storeClassify = classifyStore();
const storeAuth = authStore();
const storeAlert = alertStore();

onBeforeMount(async () => {
  await getItem(1);
});

const tableData = ref({
  table: storeClassify.classData.tables[0],
  items: [],
  search: "",
  currentPage: 1,
  hasNext: false,
  hasPrev: false,
});

async function getItem(page: number): Promise<void> {
  tableData.value.currentPage = page;
  try {
    const response = await storeAuth.axiosInstance.get(
      `${server}/table/${tableData.value.table}/${page}`,
      {
        params: {
          search: tableData.value.search,
        }
      }
    );
    const [datas, metadata] = response.data;
    tableData.value.items = datas;
    tableData.value.hasNext = metadata.has_next;
    tableData.value.hasPrev = metadata.has_prev;
  } catch (error) {
    storeAlert.alertMessage.setAlert("alert-warning", error as string);
  }
};

async function deleteItem(idItem: string): Promise<void> {
  if (confirm(`Вы действительно хотите удалить запись?`)) {
    try {
      const response = await storeAuth.axiosInstance.delete(
        `${server}/table/${tableData.value.table}/${idItem}`
      );
      console.log(response.status);
      storeAlert.alertMessage.setAlert(
        "alert-warning",
        `Запись ${idItem} из ${tableData.value.table} удалена`
      );
      getItem(tableData.value.currentPage);
    } catch (error) {
      storeAlert.alertMessage.setAlert("alert-warning", error as string);
    }
  }
};

const searchItem = debounce(() => {
  getItem(1);
}, 500);
</script>

<template>
  <div class="container py-3">
    <HeaderDiv :page-header="'Таблицы'" :cls="'text-secondary'" />
    <div class="row py-3">
      <div class="col-md-3">
        <form class="form form-check" role="form">
          <SelectDiv  v-if="storeClassify.classData.tables.length"
            :lbl-class="'visually-hidden'"
            :label="'Таблица'"
            :slc-class="'col-md-12'"
            :name="'region'"
            :isneed="false"
            :select="storeClassify.classData.tables"
            v-model="tableData.table"
            @change-event="getItem(1)"
          />
        </form>
      </div>
      <div class="col-md-8">
        <form @input="searchItem" class="form form-check" role="form">
          <InputLabel
            :lbl-cls="'visually-hidden'"
            :cls-input="'col-lg-12'"
            :lbl="'Поиск'"
            :id="'name'"
            :name="'name'"
            v-model="tableData.search"
          />
        </form>
      </div>
    </div>
    <TableSlots 
      v-if="tableData.items.length"
      :tbl-caption="`Список ${tableData.table}`"
    >
      <template v-slot:thead>
        <tr>
          <th
            v-for="(key, index) in Object.keys(tableData.items[0])"
            :key="index"
          >
            {{ key }}
          </th>
          <th width="5%">action</th>
        </tr>
      </template>
      <template v-slot:tbody>
        <tr v-for="(row, index) in tableData.items" :key="index">
          <td v-for="(val, index) in Object.values(row)" :key="index">
            {{ val }}
          </td>
          <td>
            <a
              href="#"
              @click="deleteItem(row['id'])"
              title="Удалить"
            >
              <i class="bi bi-trash"></i>
            </a>
          </td>
        </tr>
      </template>
    </TableSlots>
    <PageSwitcher
      :has_prev="tableData.hasPrev"
      :has_next="tableData.hasNext"
      :switchPrev="tableData.currentPage - 1"
      :switchNext="tableData.currentPage + 1"
      @switch="getItem"
    />
  </div>
</template>

<style scoped>
table td {
  border-bottom: none;
}
</style>
