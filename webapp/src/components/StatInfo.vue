<script setup lang="ts">

import { ref, onBeforeMount } from 'vue';
import axios from 'axios';
import config from '@/config';
import NavBar from '@/components/NavBar.vue';
import FooterDiv from './FooterDiv.vue';

const todayDate = new Date();

const data = ref({
  checks: [], 
  pfo: [],
  start: new Date(todayDate.getFullYear(), todayDate.getMonth(), 1).toISOString().slice(0,10),
  end: todayDate.toISOString().slice(0,10)
});

const captions = ['Статистика по кандидатам', 'Статистика по полиграфу'];

async function submitData() {
  const formData = {'start': data.value.start, 'end': data.value.end};
  const response = await axios.post(`${config.appUrl}/information`, formData, {
    headers: {'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`}
  });
  const { candidates, poligraf } = response.data;
  data.value.checks = candidates;
  data.value.pfo = poligraf
};

onBeforeMount(async () => {
  submitData()
});

</script>

<template>
  <NavBar />
  <div class="container py-5">
    <div class="py-5">
      <h4>Cтатистика за период c {{ data.start }} по {{ data.end }}</h4>
    </div>
    <div v-for="(tbl, index) in [data.checks, data.pfo]" class="py-2">
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
