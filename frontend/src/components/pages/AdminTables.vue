<script setup lang="ts">

import { ref } from 'vue'
import { authStore } from '@/store/token';
import server from '@store/server';
import debounce from '@store/debounce';

const storeAuth = authStore();

const tableData = ref({
    table: '',
    tableItem: [],
    itemId: '',
    searchId: '',
    itemForm: <Record<string, any>>({}),
    itemAction: '',
    currentPage: 1,
    hasNext: false,
    hasPrev: false
  });

const tablesList = [
    'resume', 'staff', 'document', 'address', 'contact', 'workplace', 
    'relation', 'check', 'registry', 'poligraf','investigation',
    'inquiry'
  ];

/**
 * Retrieves a list of users from the server.
 *
 * @return {Promise<void>} - A promise that resolves with the list of users 
 * retrieved from the server.
 */
  async function getItem(): Promise<void>{
  try {
    const response = await storeAuth.axiosInstance.get(
      `${server}/table/${tableData.value.table}/${tableData.value.currentPage}`
    );
    const [ datas, has_prev, has_next ] = response.data;
    tableData.value.tableItem = datas;
    tableData.value.hasPrev = has_prev['has_prev'];
    tableData.value.hasNext = has_next['has_next'];

  } catch (error) {
    console.error(error);
  }
};

async function searchItem(): Promise<void> {
  if (tableData.value.searchId === '') {
    getItem();
    return
  }
  try {
    const response = await storeAuth.axiosInstance.post(
      `${server}/table/${tableData.value.table}/${tableData.value.currentPage}`, {
        'id': tableData.value.searchId
      }
      );
    const [ datas, has_prev, has_next ] = response.data;

    tableData.value.tableItem =  datas;
    tableData.value.hasPrev = has_prev['has_prev'];
    tableData.value.hasNext = has_next['has_next'];

  } catch (error) {
    console.error(error);
  }
};

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

function switchPage(hasPage: boolean, currPage: number, action: string) {
    if (hasPage && action === 'previous') {
      currPage -= 1;
    } else if (hasPage && action === 'next'){
      currPage += 1;
    };
    searchItem();
  };

const idHandler = debounce(searchItem, 500);

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
              @change="getItem()">
            <option :value="tablesList[0]" selected>{{ tablesList[0] }}</option>
            <option v-for="table, index in tablesList" :key="index" :value="table">
              {{ table }}
            </option>
          </select>
        </form>
      </div>
      <div class="col-md-8">
        <form @input="idHandler" class="form form-check" role="form">
          <input class="form-control" id="name" name="name" placeholder="Поиск ID" type="text" 
                  v-model="tableData.searchId">
        </form>
      </div>
    </div>
    <div v-if="tableData.tableItem.length" class="table-responsive py-3">
      <table class="table table-hover align-middle">
        <thead> 
          <tr>
            <th width="95%" v-for="key, index in Object.keys(tableData.tableItem[0])" 
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
            <a class="page-link" href="#" @click.prevent="switchPage(
              tableData.hasPrev, tableData.currentPage, 'previous')">Предыдущая</a>
          </li>
          <li v-bind:class="{ 'page-item': true, disabled: !tableData.hasNext }">
            <a class="page-link" href="#" @click.prevent="switchPage(
              tableData.hasNext, tableData.currentPage, 'next')">Следующая</a>
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