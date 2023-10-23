<script setup lang="ts">

import { computed, onBeforeMount, ref } from 'vue';
import { onBeforeRouteLeave } from 'vue-router';
import { Bar, Line } from 'vue-chartjs';
import { authStore } from '@store/token';
import { loginStore } from '@store/login';
import { classifyStore } from '@/store/classify';
import { server } from '@share/utilities';
import { Chart } from '@share/interfaces';
import {
  Chart as ChartJS, 
  Title, 
  Tooltip, 
  Legend, 
  BarElement, 
  CategoryScale, 
  LinearScale,
  PointElement, 
  LineElement
} from 'chart.js';
import HeaderDiv from '@components/layouts/HeaderDiv.vue';

const storeAuth = authStore();
const storeLogin = loginStore();
const storeClassify = classifyStore();

const chartRadio = ref('bar');
const mapped_month = {
  '1': 'Январь',
  '2': 'Февраль',
  '3': 'Март',
  '4': 'Апрель',
  '5': 'Май',
  '6': 'Июнь',
  '7': 'Июль',
  '8': 'Август',
  '9': 'Сентябрь',
  '10': 'Октябрь',
  '11': 'Ноябрь',
  '12': 'Декабрь'
};

onBeforeMount(async () => {
  loaded.value = false;
  submitData()
});

onBeforeRouteLeave((_to: any, _from: any, next: () => void) => {
  loaded.value = false;
  next()
});

computed(() => {
  header.value = storeClassify.classifyItems.regions[stat.value.region];
});

ChartJS.register(
  CategoryScale, 
  LinearScale, 
  BarElement,
  PointElement, 
  LineElement, 
  Title, 
  Tooltip, 
  Legend
);

const todayDate = new Date();
const header = ref('');
const loaded = ref(false);
const stat = ref({
  region: 1,
  checks: [], 
  pfo: [],
  start: new Date(
    todayDate.getFullYear(), 
    todayDate.getMonth(), 1
    ).toISOString().slice(0,10),
  end: todayDate.toISOString().slice(0,10)
});
const barData = ref<Chart>({
  labels: [],
  datasets: []
});
const summedBarData = ref({});
const lineData = ref<Chart>({
  labels: [],
  datasets: []
});
const summedLineData = ref<Array<Record<string, number>>>([{}]);
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false
};

/**
 * Submits data to the server.
 *
 * @return {Promise<void>} A promise that resolves when the data is successfully submitted.
 */

async function submitData(): Promise<void> {
  const response = await storeAuth.axiosInstance.post(`${server}/information`, {
    'start': stat.value.start, 'end': stat.value.end, 'region': stat.value.region 
  });
  const { candidates, poligraf } = response.data;
  header.value = storeClassify.classifyItems.regions[stat.value.region];
  
  stat.value.pfo = poligraf;
  stat.value.checks = candidates;

  summedBarData.value = stat.value.checks
    .filter((result: { [x: string]: any; }) => result['decision'])
    .reduce((acc: { [x: string]: any; }, result: { [x: string]: any; }) => {
      const decision = result['decision'];
      const count = result['count'];
      acc[decision] = (acc[decision] || 0) + count;
      return acc;
    }, {});

  barData.value = {
    labels: Object.keys(summedBarData.value),
    datasets: [
      {
        label: 'Решения по кандидатам',
        backgroundColor: ['#f87979', '#fbc02d', '#2a9d8f', '#e9c46a', '#e76f51'], 
        data: Object.values(summedBarData.value),
      }
    ]
  };

  //summedCountsByMonth: { [key: string]: number }[] = [];

  stat.value.checks.forEach(result => {
    const month = result['month'];
    const count = result['count'];

    const monthObj = summedLineData.value.find(obj => obj.hasOwnProperty(month));

    if (monthObj) {
      monthObj[month] += count;
    } else {
      summedLineData.value.push({ [month]: count });
    }
  });

  lineData.value = {
    labels: summedLineData.value.map(obj => Object.keys(obj)[0]),
    datasets: [
      {
        label: 'Статистика по кандидатам',
        data: summedLineData.value.map(obj => Object.values(obj)[0]),
        backgroundColor: ['#f87979', '#fbc02d', '#2a9d8f', '#e9c46a', '#e76f51'],
      }
    ]
  };

  loaded.value = true;
};

</script>

<template>
    <HeaderDiv :page-header="`Статистика по региону ${header} c ${stat.start} по ${stat.end}`" />
    <div class="form form-check" role="form">
      <input class="form-check-input" type="radio" id="bar" name="bar"
        v-model="chartRadio" value="bar">
      <label class="form-check-label" for="chart">Гистограмма</label>
    </div>
    <div class="form form-check" role="form">
      <input class="form-check-input" type="radio" id="line" name="line"
        v-model="chartRadio" value="line">
      <label class="form-check-label" for="table">Линейный график</label>
    </div>

    <div v-if="chartRadio === 'bar'">
      <Bar v-if="loaded" :data="barData" :options="chartOptions" />
    </div>
    
    <div v-if="chartRadio === 'line'">
      <Line v-if="loaded" :data="lineData" :options="chartOptions" />
    </div>

    <div v-if="chartRadio === 'bar'" class="py-3">
      <table class="table table-hover table-responsive align-middle">
        <caption>Решения по кандидатам</caption>
        <thead><tr><th width="45%">Решение</th><th>Количество</th></tr></thead>
        <tbody>
          <tr height="50px" v-for="(value, index) in Object.keys(summedBarData)" 
              :key="index">
            <td >{{ value }}</td><td>{{Object.values(summedBarData)[index]}}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="chartRadio === 'line'" class="py-3">
      <table class="table table-hover table-responsive align-middle">
        <caption>Статистика по кандидатам</caption>
        <thead>
          <tr>
            <th v-for="label, index in lineData.labels" :key="index">
              {{ mapped_month[label as keyof typeof mapped_month] }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td v-for="check, index in summedLineData.map(obj => Object.values(obj)[0])" :key="index">
              {{ check }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="storeLogin.userData.region_id == '1'" class="py-3">
      <table class="table table-hover table-responsive align-middle">
        <caption>Статистика по полиграфу</caption>
        <thead><tr><th width="45%">Критерий</th><th>Количество</th></tr></thead>
        <tbody>
          <tr height="50px" v-for="(value, name, index) in stat.pfo" :key="index">
            <td >{{name}}</td><td>{{value}}</td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div class="py-3">
      <form @submit.prevent="submitData" class="form form-check" role="form">
          <div class="mb-3 row required">
            <label class="col-form-label col-md-2" for="region">Регион</label>
            <div class="col-md-2">
              <select :disabled="storeLogin.userData.region_id != '1'"
                      @change="submitData" 
                      class="form-select" id="region" name="region" 
                      v-model="stat.region">
                <option :value="storeLogin.userData.region_id" selected>
                  {{ storeClassify.classifyItems.regions[storeLogin.userData.region_id] }}</option>
                <option v-for="name, value in storeClassify.classifyItems.regions" 
                        :key="value" :value="value">{{name}}</option>                
              </select>
            </div>
            <label class="col-form-label col-md-1" for="start">Период:</label>
            <div class="col-md-2">
              <input class="form-control" id="start" name="start" required type="date" 
                  v-model="stat.start">
            </div>
            <div class="col-md-2">
              <input class="form-control" name="end" required type="date" 
                  v-model=stat.end>
            </div>
            <div class="col-md-2">
              <button class="btn btn-primary btn-md" name="submit" type="submit">
                  Принять</button>
            </div>
          </div>
      </form>
    </div>

</template>
