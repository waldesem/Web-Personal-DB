<script setup lang="ts">
// Компонент для отображения статистики по региону и полиграфу 

import { ref, onBeforeMount } from 'vue';
import { appClassify } from '@store/classify';
import { appAuth } from '@store/auth';
import { appAlert } from '@/store/alert';
import server from '@store/server';

const storeClassify = appClassify();
const storeAuth = appAuth();
const storeAlert = appAlert();

const todayDate = new Date();
storeAlert.alertAttr = '';
storeAlert.alertText = '';
const header = ref('');

const data = ref({
  region: 1,
  checks: [], 
  pfo: [],
  start: new Date(todayDate.getFullYear(), todayDate.getMonth(), 1).toISOString().slice(0,10),
  end: todayDate.toISOString().slice(0,10)
});

const captions = ['Статистика по кандидатам', 'Статистика по полиграфу'];

// Отправка запроса на сервер перед монтированием компонента
onBeforeMount(async () => {
  submitData()
});

/**
 * Submits data to the server.
 *
 * @return {Promise<void>} A promise that resolves when the data is successfully submitted.
 */

async function submitData(): Promise<void> {
  const response = await storeAuth.axiosInstance.post(`${server}/information`, {
    'start': data.value.start, 'end': data.value.end, 'region': data.value.region 
  });
  const { candidates, poligraf } = response.data;
  header.value = storeClassify.regions[data.value.region];
  
  data.value.checks = candidates;
  data.value.pfo = poligraf
};


</script>

<template>
  <div class="container py-5">
    <div class="py-5">
      <h4>Статистика по региону {{ header }} за период c {{ data.start }} по {{ data.end }}</h4>
    </div>
    <div v-for="(tbl, index) in [data.checks, data.pfo]" :key="index" class="py-3">
      <table class="table table-hover table-responsive align-middle">
        <caption>{{captions[index]}}</caption>
        <thead><tr><th width="45%">Критерий</th><th>Количество</th></tr></thead>
        <tbody>
          <tr height="50px" v-for="(value, name, index) in tbl" :key="index">
            <td >{{value}}</td><td>{{name}}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="py-5">
      <form @submit.prevent="submitData" class="form form-check" role="form">
          <div class="mb-3 row required">
            <label class="col-form-label col-md-2" for="region">Регион</label>
            <div class="col-md-2">
              <select class="form-select" id="region" name="region" v-model="data.region">
                <option value="" selected>Выберите регион</option>
                <option v-for="name, value in storeClassify.regions" :key="value" :value="value">{{name}}</option>                
              </select>
            </div>
            <label class="col-form-label col-md-1" for="start">Период:</label>
            <div class="col-md-2">
                <input class="form-control" id="start" name="start" required type="date" v-model="data.start">
            </div>
            <div class="col-md-2">
                <input class="form-control" name="end" required type="date" v-model=data.end>
            </div>
            <div class="col-md-2">
                <button class="btn btn-primary btn-md" name="submit" type="submit">Принять</button>
            </div>
          </div>
      </form>
    </div>
  </div>
</template>
