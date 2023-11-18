<script setup lang="ts">

import { onBeforeMount, ref } from 'vue'
import { onBeforeRouteLeave } from 'vue-router';
import { authStore } from '@/store/token';
import { alertStore } from '@store/alert';
import { classifyStore} from '@store/classify'
import { server, debounce } from '@share/utilities';
import PageSwitcher from '@components/layouts/PageSwitcher.vue';
import HeaderDiv from '@components/layouts/HeaderDiv.vue';

const storeAuth = authStore();
const storeAlert = alertStore();
const storeClassify = classifyStore()

const searchItem = debounce(getItem, 500);

const tableData = ref({
  table: '',
  tableItem: [],
  searchId: '',
  currentPage: 1,
  hasNext: false,
  hasPrev: false
});

onBeforeMount(() => {
  tableData.value.table = storeClassify.classifyItems.tables['tables'][0];
  getItem();
});

onBeforeRouteLeave((_to: any, _from: any, next: () => void) => {
  Object.assign(tableData.value, {
    table: '',
    tableItem: [],
    searchId: '',
    currentPage: 1,
    hasNext: false,
    hasPrev: false
  });
  next()
});

async function getItem(page = tableData.value.currentPage): Promise<void> {
  try {
    const response = await storeAuth.axiosInstance.post(
      `${server}/table/${tableData.value.table}/${page}`, {
        'id': tableData.value.searchId
      }
    );
    const [ datas, metadata ] = response.data;

    tableData.value.tableItem = datas;
    tableData.value.hasNext = metadata.has_next;
    tableData.value.hasPrev = metadata.has_prev;
    
  } catch (error) {
    storeAlert.setAlert('alert-warning', error as string);
  }
};

async function deleteItem(idItem: string): Promise<void>{
  if (confirm(`Вы действительно хотите удалить запись?`)) {
    try {
      const response = await storeAuth.axiosInstance.delete(
        `${server}/table/${tableData.value.table}/${idItem}`);
      console.log(response.status);
      storeAlert.setAlert('alert-warning', 
                          `Запись ${idItem} из ${tableData.value.table} удалена`);
      getItem();
    } catch (error) {
      storeAlert.setAlert('alert-warning', error as string);
    }
  };
};

</script>

<template>
  <div class="container py-3">
    <HeaderDiv :page-header="'Таблицы'" />
    <div class="row py-3">
      <div class="col-md-3">
        <form class="form form-check" role="form">
          <select class="form-select" id="region" name="region" 
              v-model="tableData.table" 
              @change="tableData.currentPage = 1; getItem()">
            <option v-for="table, index in storeClassify.classifyItems.tables['tables']" 
                          :key="index" :value="table">
              {{ table }}
            </option>
          </select>
        </form>
      </div>
      <div class="col-md-8">
        <form @input="searchItem" class="form form-check" role="form">
          <input class="form-control" id="name" name="name" placeholder="Поиск ID" type="text" 
                 v-model="tableData.searchId">
        </form>
      </div>
    </div>
    <div v-if="tableData.tableItem.length" class="table-responsive py-3">
      <table class="table table-hover align-middle">
        <thead> 
          <tr>
            <th v-for="key, index in Object.keys(tableData.tableItem[0])" 
                      :key="index">
              {{ key }}
            </th>
            <th width="5%">action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row, index in tableData.tableItem" :key="index">
            <td v-for="val, index in Object.values(row)" :key="index">{{ val }}</td>
            <td>
              <a href="#" @click="deleteItem(row['id'])" title="Удалить">
                <i class="bi bi-trash"></i>
              </a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <PageSwitcher :has_prev = "tableData.hasPrev"
                  :has_next = "tableData.hasNext"
                  :switchPrev = "tableData.currentPage -1"
                  :switchNext = "tableData.currentPage +1" 
                  :switchPage = "getItem"/>
  </div>
</template>

<style scoped>
table td
{
  border-bottom: none;
}
</style>