<template>
  <NavBar />
  <div class="container py-5">
    <AlertMessage v-if="data.attr" :attr="data.attr" :text="data.text" />
    <div class="py-5"><h4>{{data.header}}</h4></div>
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
                <input class="form-control" id="start" name="start" required type="date" value="">
            </div> _
            <div class="col-md-2">
                <input class="form-control" name="end" required type="date" value="">
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
import appUrl from '@/config';
import NavBar from '@/components/NavBar.vue';
import FooterDiv from './FooterDiv.vue';
import AlertMessage from './AlertMessage.vue';

const data = ref({
  header: '', 
  checks: [], 
  pfo: [],
  attr: '',
  text: ''
});

async function submitData(event: any) {
  const formData = new FormData(event.target);
  const response = await axios.post(`${appUrl}/information`, formData, {headers: {
    'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`
  }});
  const { candidates, poligraf, title } = response.data;
  Object.assign(data.value, {
    checks: candidates, 
    pfo: poligraf, 
    header: title 
  })
}

onBeforeMount(async () => {
  const response = await axios.get(`${appUrl}/information`, {headers: {
    'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`
  }});
  const { candidates, poligraf, title } = response.data;
  Object.assign(data.value, {
    checks: candidates, 
    pfo: poligraf, 
    header: title
  })
});

</script>