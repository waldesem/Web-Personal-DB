<script setup lang="ts">

import { defineAsyncComponent, onBeforeMount } from 'vue'
import { onBeforeRouteLeave } from 'vue-router';
import { classifyStore} from '@store/classify'
import { tableStore } from '@store/tables';
import {  debounce } from '@share/utilities';

const PageSwitcher = defineAsyncComponent(() => import('@components/layouts/PageSwitcher.vue'));
const HeaderDiv = defineAsyncComponent(() => import('@components/layouts/HeaderDiv.vue'));

const storeClassify = classifyStore();
const storeTable = tableStore();

const searchItem = debounce(storeTable.tableData.getItem, 500);

onBeforeMount(() => {
  if (storeClassify.classifyItems.tables['tables'].length) {
    storeTable.tableData.table = storeClassify.classifyItems.tables['tables'][0];
    storeTable.tableData.getItem(1);
  }
});

onBeforeRouteLeave((_to: any, _from: any, next: () => void) => {
  Object.assign(storeTable.tableData.table, {
    table: '',
    tableItem: [],
    searchId: '',
    currentPage: 1,
    hasNext: false,
    hasPrev: false
  });
  next()
});

</script>

<template>
  <div class="container py-3">
    <HeaderDiv :page-header="'Таблицы'" />
    <div class="row py-3">
      <div class="col-md-3">
        <form class="form form-check" role="form">
          <select v-if="storeClassify.classifyItems.tables['tables'].length"
                  class="form-select" id="region" name="region" 
                  v-model="storeTable.tableData.table" 
                  @change="storeTable.tableData.getItem(1)">
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
                 v-model="storeTable.tableData.search">
        </form>
      </div>
    </div>
    <div v-if="storeTable.tableData.item.length" class="table-responsive py-3">
      <table class="table table-hover align-middle">
        <thead> 
          <tr>
            <th v-for="key, index in Object.keys(storeTable.tableData.item[0])" 
                      :key="index">
              {{ key }}
            </th>
            <th width="5%">action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row, index in storeTable.tableData.item" :key="index">
            <td v-for="val, index in Object.values(row)" :key="index">{{ val }}</td>
            <td>
              <a href="#" @click="storeTable.tableData.deleteItem(row['id'])" title="Удалить">
                <i class="bi bi-trash"></i>
              </a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <PageSwitcher :has_prev = "storeTable.tableData.hasPrev"
                  :has_next = "storeTable.tableData.hasNext"
                  :switchPrev = "storeTable.tableData.currentPage -1"
                  :switchNext = "storeTable.tableData.currentPage +1" 
                  :switchPage = "storeTable.tableData.getItem"/>
  </div>
</template>

<style scoped>
table td
{
  border-bottom: none;
}
</style>