<template>
  <NavBar />
  <div class="container py-5">
    <div class="py-5">
      <h4>Cтатистика за период c {{ data.start }} по {{ data.end }}</h4>
    </div>
    <div class="py-1">
      <table class="table table-hover align-middle">
        <caption>Статистика по кандидатам</caption>
        <thead><tr><th>Решение</th><th>Количество</th></tr></thead>
        <tbody>
          <tr height="50px" v-for="(value, name, index) in data.checks" :key="index">
            <td >{{value}}</td><td>{{name}}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="py-1">
      <table class="table table-hover align-middle">
        <caption>Статистика по ПФО</caption>
        <thead><tr><th>Решение</th><th>Количество</th></tr></thead>
        <tbody>
          <tr height="50px" v-for="(value, name, index) in data.pfo" :key="index">
            <td >{{value}}</td><td>{{name}}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="py-5">
      <form @submit.prevent="submitData" class="form form-check" role="form">
          <div class="mb-3 row required">
            <label class="col-form-label col-md-1" for="start">Период:</label>
            <div class="col-md-2">
                <input class="form-control" id="start" name="start" required type="date" v-model="data.start">
            </div> _
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
  <FooterDiv />
</template>


<script setup lang="ts">

import { ref,  onBeforeMount } from 'vue';
import axios from 'axios';
import config from '@/config';
import NavBar from '@/components/NavBar.vue';
import FooterDiv from './FooterDiv.vue';

const date = new Date();

const data = ref({
  checks: [], 
  pfo: [],
  start: convertDate(new Date(date.getFullYear(), date.getMonth(), 1).toLocaleDateString()),
  end: convertDate(date.toLocaleDateString())
});

async function submitData() {
  const formData = {'start': data.value.start, 'end': data.value.end};
  const response = await axios.post(`${config.appUrl}/information`, formData, {
    headers: {'Authorization': `Bearer ${config.token}`}
  });
  const { candidates, poligraf, title } = response.data;
  Object.assign(data.value, {
    checks: candidates, 
    pfo: poligraf
  })
}

function convertDate(value: string): string {
  const date = new Date(Date.parse(value));
  const day = date.getDate().toString().padStart(2, '0');
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const year = date.getFullYear().toString();
  return `${year}-${month}-${day}`;
}

onBeforeMount(async () => {
  submitData()
});

</script>