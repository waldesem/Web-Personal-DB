<script setup lang="ts">

import { onBeforeMount, ref } from 'vue'
import axios from 'axios';
import config from '../../config';
import NavbarAdmin from './NavbarAdmin.vue'
import AlertMessage from '../AlertMessage.vue';
import FooterDiv from '../FooterDiv.vue';


const data = ref({
  regions: [],
  location: '',
  attr: '',
  text: ''
});


onBeforeMount(async () => {
  regionList();
});


async function regionList(){
    const response = await axios.get(`${config.appUrl}/locations`);
    const locations  = response.data;
    data.value.regions = locations.reduce(
    (acc: {[key: number]: string}, obj: {id: number, region: string}) => {
    acc[obj.id] = obj.region;
    return acc;
    }, {}
  );
};

  
async function addRegion() {
  const response = await axios.post(`${config.appUrl}/admin/region/add`, {
    'region': data.value.location
  }, {
    headers: {'Authorization': `Bearer ${localStorage.getItem('access_token')}`}
  });
  const  { location } = response.data;
  data.value.attr = location ? 'alert-warning' : 'alert-success' ;
  data.value.text = location 
    ? 'При добавлении записи возникла ошибка'
    : 'Запись добавлена. Для применения изменений необходим перезапуск приложения';
  regionList();
};


async function delRegion(id: String) {
  if (confirm(`Вы действительно хотите удалить регион?`)) {
    const response = await axios.get(`${config.appUrl}/admin/region/delete/${id}`, {
    headers: {'Authorization': `Bearer ${localStorage.getItem('access_token')}`}
  });
    const  { location } = response.data;
    data.value.attr = 'alert-success';
    data.value.text = `Регион ${location} удален. Перезапустите приложение`;
    regionList()
  }
};

</script>

<template>
<NavbarAdmin />
  <div class="container py-5">
  <AlertMessage v-if="data.attr" :attr="data.attr" :text="data.text" />
  <div class="py-5"><h4>Список регионов</h4></div>
    <form @submit.prevent="addRegion" class="form form-check" role="form"> 
      <div class="row mb-3">
        <div class="row">
          <label class="col-form-label col-lg-1" for="region">Регион: </label>
          <div class="col-lg-9">
              <input autocomplete="region" class="form-control" minlength="3" maxlength="25" name="region" 
                    placeholder="Регион" required type="text" v-model="data.location">
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
          <tr height="50px" v-for="name, value in data.regions">
            <td>{{ value }}</td>
            <td>{{ name }}</td>
            <td><a class="link-opacity-50" href="#" @click="delRegion(value.toString())">Удалить</a></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <FooterDiv />
</template>