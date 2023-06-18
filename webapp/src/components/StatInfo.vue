<template>
  <NavBar />
  <div class="container">
    <div class="py-5">
      <h5>{{header}}</h5>
    </div>
    <div class="py-1">
      <table class="table table-hover align-middle">
        <caption>Статистика по кандидатам</caption>
        <thead><tr><th>Решение</th><th>Количество</th></tr></thead>
        <tbody>
          <tr height="50px" v-for="(value, name, index) in checks" :key="index">
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
          <tr height="50px" v-for="(value, name, index) in pfo" :key="index">
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
import NavBar from '@/components/NavBar.vue';

const header = ref('');
const checks = ref([]);
const pfo = ref([]);

async function submitData(event: any) {
  const response = await axios.post(`http://localhost:5000/information`, {
    method: 'POST',
    body: new FormData(event.target)
  });
  const { candidates, poligraf, title } = response.data;
  checks.value = candidates;
  pfo.value = poligraf;
  header.value = title;
}

(async (): Promise<void> => {
  const response = await axios.get(`http://localhost:5000/information`);
  const { candidates, poligraf, title } = response.data;
  checks.value = candidates;
  pfo.value = poligraf;
  header.value = title;
})();

</script>