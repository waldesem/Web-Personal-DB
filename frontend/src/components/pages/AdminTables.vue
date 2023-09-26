<script setup lang="ts">

import { storeAdmin } from '@/store/admin';

const adminStore = storeAdmin();

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
              v-model="adminStore.tableData.table" 
              @change="adminStore.getItem()">
            <option v-for="table, index in adminStore.tablesList" :key="index" :value="table">
              {{ table }}
            </option>
          </select>
        </form>
      </div>
      <div class="col-md-8">
        <form @input="adminStore.idHandler" class="form form-check" role="form">
          <input class="form-control" id="name" name="name" placeholder="Поиск ID" type="text" 
                  v-model="adminStore.tableData.searchId">
        </form>
      </div>
    </div>
    <div v-if="adminStore.tableData.tableItem.length" class="table-responsive py-3">
      <table class="table table-hover align-middle">
        <thead> 
          <tr>
            <th width="95%" v-for="key, index in Object.keys(adminStore.tableData.tableItem[0])" 
                      :key="index">{{ key }}</th>
            <th width="5%">action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row, index in adminStore.tableData.tableItem" :key="index">
            <td v-for="val, index in Object.values(row)" :key="index">{{ val }}</td>
            <td>
              <a href="#" @click="adminStore.deleteItem(row['id'])" title="Удалить">
                <i class="bi bi-trash"></i>
              </a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="py-3">  
      <nav v-if="adminStore.tableData.hasPrev || adminStore.tableData.hasNext">
        <ul class="pagination justify-content-center">
          <li v-bind:class="{ 'page-item': true, disabled: !adminStore.tableData.hasPrev }">
            <a class="page-link" href="#" v-on:click.prevent="adminStore.switchPage(adminStore.tableData.hasPrev, adminStore.tableData.currentPage, 'previous', 'table')">Предыдущая</a>
          </li>
          <li v-bind:class="{ 'page-item': true, disabled: !adminStore.tableData.hasNext }">
            <a class="page-link" href="#" v-on:click.prevent="adminStore.switchPage(adminStore.tableData.hasNext, adminStore.tableData.currentPage, 'next', 'table')">Следующая</a>
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