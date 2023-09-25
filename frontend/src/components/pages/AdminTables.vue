<script setup lang="ts">

import { storeAdmin } from '@/store/admin';

const adminStore = storeAdmin();

</script>

<template>
  <div class="container py-3">
    <div class="py-5">
      <h4>Таблицы</h4>
    </div>
    <div class="row">
      <div class="col-md-3">
        <form class="form form-check" role="form">
          <select class="form-select" id="region" name="region" 
              v-model="adminStore.tableData.table" 
              @change="adminStore.getItem(adminStore.tableData.table)">
            <option v-for="table, index in adminStore.tablesList" :key="index" :value="table">
              {{ table }}
            </option>
          </select>
        </form>
      </div>
        <form @input="adminStore.idHandler" class="form form-check" role="form">
            <div class="row py-3">
              <input class="form-control" id="name" name="name" placeholder="Поиск ID" type="text" 
                  v-model="adminStore.tableData.searchId">
            </div>
        </form>
    </div>
    <div class="py-3">
      <table class="table table-responsive align-middle no-bottom-border">
        <thead> 
          <tr>
            <th v-for="key, index in Object.keys(adminStore.tableData.tableItem[0])" :key="index">{{ key }}</th>
          </tr>
        </thead>
        <tbody v-if="adminStore.tableData.tableItem">
          <tr>
            <td :colspan="adminStore.tableData.tableItem.length+2">
              <table v-for="row, index in adminStore.tableData.tableItem" :key="index" 
                  class="table table-responsive table-hover align-middle">
                <tbody>
                  <tr v-if="adminStore.tableData.itemId !== row['id']">
                    <td>{{ Object.values(row) }}</td>
                    <td width="5%">
                      <a class="btn btn-link" title="Изменить"
                          @click="adminStore.tableData.itemAction='edit'; 
                                  adminStore.tableData.itemId=row['id'];
                                  adminStore.tableData.itemForm=row">
                        <i class="bi bi-pencil-square"></i>
                      </a>
                    </td>
                    <td width="5%">
                      <a href="#" @click="adminStore.deleteItem(row['id'])" title="Удалить">
                        <i class="bi bi-trash"></i>
                      </a>
                    </td>
                  </tr>
                  <tr v-if="adminStore.tableData.itemAction === 'edit' &&  adminStore.tableData.itemId === row['id']" >
                    <td colspan="9">
                      <form @submit.prevent="adminStore.updateItem" class="form form-check">
                        <div class="row">
                          <div v-for="key, index in Object.keys(adminStore.tableData.tableItem[0])" :key="index">
                            <input class="form-control form-control-sm" :id="key" :name="key" type="text" v-model="adminStore.tableData.itemForm[key]">
                          </div>
                          <div>
                            <button class="btn btn-outline-primary btn-sm" type="submit">Принять</button>
                          </div>
                          <div>
                            <button class="btn btn-outline-primary btn-sm" @click="adminStore.tableData.itemAction = '';
                                                                                        adminStore.tableData.itemId= ''">Отмена
                            </button>
                          </div>
                        </div>
                      </form>
                    </td>
                  </tr>
                </tbody>
              </table>
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