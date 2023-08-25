<script setup lang="ts">
// Компонент для отображения списка регионов

import { appLocation } from '@store/location';
import { storeAdmin } from '@store/admin';

const adminStore = storeAdmin();
const storeLocation = appLocation();

</script>

<template>
  <div class="container py-3">
  <div class="py-5"><h4>Список регионов</h4></div>
    <form @submit.prevent="adminStore.addRegion" class="form form-check" role="form"> 
      <div class="row mb-3">
        <div class="row">
          <label class="col-form-label col-lg-1" for="region">Регион: </label>
          <div class="col-lg-9">
              <input autocomplete="region" class="form-control" minlength="3" maxlength="25" name="region" 
                    placeholder="Регион" required type="text" v-model="adminStore.region">
          </div>
          <div class="col-lg-2">
              <button class="btn btn-outline-primary" name="submit" type="submit">Добавить регион</button>
          </div>
        </div>
      </div>
    </form>
    <div class="py-3">
      <table class="table table-hover table-responsive align-middle">
        <thead>
          <tr height="50px">
            <th width="15%">#</th>
            <th>Регион</th>
            <th width="25%">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr height="50px" v-for="name, value in storeLocation.regionsObject" :key="value">
            <td>{{ value }}</td>
            <td>{{ name }}</td>
            <td><a class="link-opacity-50" href="#" @click="adminStore.delRegion(value.toString())">Удалить</a></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>