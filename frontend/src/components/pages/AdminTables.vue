<script setup lang="ts">

import { onBeforeMount, ref } from 'vue'
import { onBeforeRouteLeave } from 'vue-router';
import { authStore } from '@/store/token';
import { server, debounce } from '@share/utilities';

const storeAuth = authStore();

const tablesList = [
  'resume', 'staff', 'document', 'address', 'contact', 'workplace', 
  'relation', 'check', 'registry', 'poligraf','investigation', 'inquiry', 'tag'
];

const tableData = ref({
  table: '',
  tableItem: [],
  searchId: '',
  currentPage: 1,
  hasNext: 0,
  hasPrev: 0
});

onBeforeMount(() => {
  tableData.value.table = tablesList[0];
  console.log(tableData.value.table);
  getItem();
});

onBeforeRouteLeave(() => {
  Object.assign(tableData.value, {
    table: '',
    tableItem: [],
    searchId: '',
    currentPage: 1,
    hasNext: 0,
    hasPrev: 0
  })
});

async function getItem(): Promise<void> {

  try {
    const response = await storeAuth.axiosInstance.post(
      `${server}/table/${tableData.value.table}/${tableData.value.currentPage}`, {
        'id': tableData.value.searchId
      }
    );
    const [ datas, metadata ] = response.data;

    tableData.value.tableItem =  datas;
    tableData.value.hasNext = metadata.has_next;
    tableData.value.hasPrev = metadata.has_prev;
    
  } catch (error) {
    console.error(error);
  }
};

const searchItem = debounce(getItem, 500);

async function deleteItem(idItem: string): Promise<void>{
  try {
    const response = await storeAuth.axiosInstance.delete(
      `${server}/table/${tableData.value.table}/${idItem}`);
    console.log(response.status);
    getItem();
  
  } catch (error) {
    console.error(error);
  }
};


</script>

<template>
  <div class="container py-3">
    <div class="py-3">
      <h4>Таблицы</h4>
    </div>
    <div class="row py-3">
      <div class="col-md-3">
        <form class="form form-check" role="form">
          <select class="form-select" id="region" name="region" 
              v-model="tableData.table" 
              @change="tableData.currentPage = 1; getItem()">
            <option v-for="table, index in tablesList" :key="index" :value="table">
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
                      :key="index">{{ key }}</th>
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
    <div class="py-3">  
      <nav v-if="tableData.hasPrev || tableData.hasNext">
        <ul class="pagination justify-content-center">
          <li v-bind:class="{ 'page-item': true, disabled: !tableData.hasPrev }">
            <a class="page-link" href="#" 
               @click.prevent="tableData.currentPage -= 1; getItem()">
               Предыдущая
            </a>
          </li>
          <li v-bind:class="{ 'page-item': true, disabled: !tableData.hasNext }">
            <a class="page-link" href="#" 
              @click.prevent="tableData.currentPage += 1; getItem()">
               Следующая
              </a>
          </li>
        </ul>
      </nav>
    </div>
  </div>
</template>

<style scoped>
table td
{
  border-bottom: none;
}
</style>