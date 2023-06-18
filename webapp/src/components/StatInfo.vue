<template>
  <NavBar />
  <div class="container">
    <div class="py-5">
      <h5>{{data.header}}</h5>
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
    <div class="py-2">
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
    <div class="py-4">
      <form @submit.prevent="submitData" class="form form-check" role="form">
          <div class="mb-3 row required">
              <label class="col-form-label col-md-2" for="start">Начало периода</label>
              <div class="col-md-2">
                  <input class="form-control" name="start" required type="date" value="">
              </div>
          </div>
          <div class="mb-3 row required">
              <label class="col-form-label col-md-2" for="end">Конец периода</label>
              <div class="col-md-2">
                  <input class="form-control" name="end" required type="date" value="">
              </div>
          </div>
          <div class=" row">
              <div class="offset-md-2 col-md-2">
                  <input class="btn btn-primary btn-md" name="submit" type="submit" value="Принять">
              </div>
          </div>
      </form>
    </div>
  </div>
</template>


<script setup lang="ts">

import axios from 'axios';
import { ref } from 'vue';
import appUrl from '../main.js';
import NavBar from '@/components/NavBar.vue';

const data = ref({header: '', checks: [], pfo: []});

async function submitData(event: any) {
  const formData = new FormData(event.target);
  const response = await axios.post(`${appUrl}/information`, formData, {headers: {
    'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`
  }});
  const { candidates, poligraf, title } = response.data;
  Object.assign(data.value, { checks: candidates, pfo: poligraf, header: title });
}

(async (): Promise<void> => {
  const response = await axios.get(`${appUrl}/information`, {headers: {
    'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`
  }});
  const { candidates, poligraf, title } = response.data;
  Object.assign(data.value, { checks: candidates, pfo: poligraf, header: title });
})();

</script>