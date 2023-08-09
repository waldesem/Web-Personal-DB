<script setup lang="ts">

import { onBeforeMount, ref } from 'vue'
import { locationStore } from '../../store/location';
import { appAuth } from '../../store/auth';
import server from '../../store/server';

const emit = defineEmits(['updateMessage']);

const storeAuth = appAuth()

const storeLocation = locationStore();

const region = ref('');


onBeforeMount(async () => {
  storeLocation.getRegions();
});


function updateMessage(alert: Object) {
  emit('updateMessage', alert)
};


async function addRegion() {
  const response = await storeAuth.axiosInstance.post(`${server}/region/add`, {
    'region': region.value
  });
  const  { location } = response.data;
  updateMessage({
    attr: location ? 'alert-warning' : 'alert-success',
    text: location 
    ? 'При добавлении записи возникла ошибка'
    : 'Запись добавлена'
  })
  storeLocation.getRegions();
};


async function delRegion(id: String) {
  if (id === '1') {
    updateMessage({
      attr: 'alert-info',
      text: 'Нельзя удалить регион "Главный офис"'
    })
    return
  }
  if (confirm(`Вы действительно хотите удалить регион?`)) {
    const response = await storeAuth.axiosInstance.get(`${server}/region/delete/${id}`);
    const  { location } = response.data;
    updateMessage({
      attr: 'alert-success',
      text: `Регион ${location} удален`
    })
    storeLocation.getRegions();
  }
};

</script>

<template>
  <div class="container py-3">
  <div class="py-5"><h4>Список регионов</h4></div>
    <form @submit.prevent="addRegion" class="form form-check" role="form"> 
      <div class="row mb-3">
        <div class="row">
          <label class="col-form-label col-lg-1" for="region">Регион: </label>
          <div class="col-lg-9">
              <input autocomplete="region" class="form-control" minlength="3" maxlength="25" name="region" 
                    placeholder="Регион" required type="text" v-model="region">
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
          <tr height="50px" v-for="name, value in storeLocation.regionsObject">
            <td>{{ value }}</td>
            <td>{{ name }}</td>
            <td><a class="link-opacity-50" href="#" @click="delRegion(value.toString())">Удалить</a></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>