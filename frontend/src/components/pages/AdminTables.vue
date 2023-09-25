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
          <select class="form-select" id="region" name="region" v-model="adminStore.selectedTable" @change="adminStore.getItem(adminStore.selectedTable)">
            <option value="" selected>Выбор таблицы</option>
            <option v-for="table, index in adminStore.tables" :key="index" :value="table">{{ table }}</option>
          </select>
        </form>
      </div>
        <form @input="adminStore.searchItemHandeler" class="form form-check" role="form">
            <div class="row py-3">
                <input class="form-control" id="name" name="name" placeholder="Поиск ID" type="text" v-model="adminStore.searchID">
            </div>
        </form>
    </div>
    <div class="py-3">
      <table class="table table-responsive align-middle no-bottom-border">
        <thead> 
          <tr>
            <th v-for="key, index in Object.keys(adminStore.tableItem[0])" :key="index">{{ key }}</th>
          </tr>
        </thead>
        <tbody v-if="adminStore.tableItem">
          <tr>
            <td :colspan="adminStore.tableItem.length+2">
              <table v-for="row, index in adminStore.tableItem" :key="index" 
                  class="table table-responsive table-hover align-middle">
                <tbody>
                  <tr v-if="adminStore.itemId !== row['id']">
                    <td>{{ Object.values(row) }}</td>
                    <td width="5%">
                      <a class="btn btn-link" title="Изменить"
                          @click="adminStore.itemAction='edit'; 
                                  adminStore.itemId=row['id'];
                                  adminStore.itemForm=row">
                        <i class="bi bi-pencil-square"></i>
                      </a>
                    </td>
                    <td width="5%">
                      <a href="#" @click="adminStore.deleteItem(row['id'])" title="Удалить">
                        <i class="bi bi-trash"></i>
                      </a>
                    </td>
                  </tr>
                  <tr v-if="adminStore.itemAction === 'edit' &&  adminStore.itemId === row['id']" >
                    <td colspan="9">
                      <form @submit.prevent="adminStore.updateItem" class="form form-check">
                        <div class="row">
                          <div class="col" v-for="key, index in Object.keys(adminStore.tableItem[0])" :key="index">
                            <input class="form-control form-control-sm" :id="key" :name="key" type="text" v-model="adminStore.itemForm[key]">
                          </div>
                          <div class="col-md-1">
                            <button class="btn btn-outline-primary btn-sm" type="submit">Принять</button>
                          </div>
                          <div class="col-md-1">
                            <button class="btn btn-outline-primary btn-sm" @click="adminStore.itemAction = '';
                                                                                        adminStore.itemId= ''">Отмена
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
      <nav v-if="adminStore.hasPrev || adminStore.hasNext">
        <ul class="pagination justify-content-center">
          <li v-bind:class="{ 'page-item': true, disabled: !adminStore.hasPrev }">
            <a class="page-link" href="#" v-on:click.prevent="adminStore.prevPage">Предыдущая</a>
          </li>
          <li v-bind:class="{ 'page-item': true, disabled: !adminStore.hasNext }">
            <a class="page-link" href="#" v-on:click.prevent="adminStore.nextPage">Следующая</a>
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