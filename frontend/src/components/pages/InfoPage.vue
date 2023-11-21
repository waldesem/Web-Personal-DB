<script setup lang="ts">

import { computed, onBeforeMount, ref, defineAsyncComponent } from 'vue';
import { onBeforeRouteLeave } from 'vue-router';
import { loginStore } from '@store/login';
import { classifyStore } from '@/store/classify';
import { authStore } from '@/store/token';
import { server } from '@/utilities/utils';
import { Bar, Line } from 'vue-chartjs';
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

const HeaderDiv = defineAsyncComponent(() => import('@components/layouts/HeaderDiv.vue'));

const storeAuth = authStore();
const storeLogin = loginStore();
const storeClassify = classifyStore();

interface Chart {
  labels: string[];
  datasets: {
    label: string;
    backgroundColor: string[];
    data: number[];
  }[],
};

const todayDate = new Date();
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

const chartData = ref({
  radio: 'bar',
  header: '',
  loaded: false,
  bar: <Chart>({}),
  barSummed: <Record<string, number>>({}),
  line: <Chart>({}),
  lineSummed: <Array<Record<string, number>>>([{}]),
  stat: {
    region: 1,
    checks: [], 
    pfo: [],
    start: new Date(
      todayDate.getFullYear(), 
      todayDate.getMonth(), 1).toISOString().slice(0,10),
    end: todayDate.toISOString().slice(0,10)
  },
  options:  {
    responsive: true,
    maintainAspectRatio: false
  },
  
  submitData: async function (): Promise<void> {
    const response = await storeAuth.axiosInstance.post(`${server}/information`, {
      'start': this.stat.start, 'end': this.stat.end, 'region': this.stat.region 
    });
    const { candidates, poligraf } = response.data;
    this.header = storeClassify.classData.regions[this.stat.region];
    
    this.stat.pfo = poligraf;
    this.stat.checks = candidates;

    this.barSummed = this.stat.checks
      .filter((result: { [x: string]: any; }) => result['decision'])
      .reduce((acc: { [x: string]: any; }, result: { [x: string]: any; }) => {
        const decision = result['decision'];
        const count = result['count'];
        acc[decision] = (acc[decision] || 0) + count;
        return acc;
      }, {});

    this.bar = {
      labels: Object.keys(this.barSummed),
      datasets: [
        {
          label: 'Решения по кандидатам',
          backgroundColor: ['#f87979', '#fbc02d', '#2a9d8f', '#e9c46a', '#e76f51'], 
          data: Object.values(this.barSummed),
        }
      ]
    };
    

    this.stat.checks.forEach(result => {
      const month = result['month'];
      const count = result['count'];

      const monthObj = this.lineSummed.find(obj => obj.hasOwnProperty(month));

      if (monthObj) {
        monthObj[month] += count;
      } else {
        this.lineSummed.push({ [month]: count });
      }
    });

    this.line = {
      labels: this.lineSummed.map(obj => Object.keys(obj)[0]),
      datasets: [
        {
          label: 'Статистика по кандидатам',
          data: this.lineSummed.map(obj => Object.values(obj)[0]),
          backgroundColor: ['#f87979', '#fbc02d', '#2a9d8f', '#e9c46a', '#e76f51'],
        }
      ],
    };
    this.loaded = true;
  }
});

onBeforeMount(async () => {
  chartData.value.loaded = false;
  chartData.value.submitData()
});

onBeforeRouteLeave((_to: any, _from: any, next: () => void) => {
  chartData.value.loaded = false;
  next()
});

computed(() => {
  chartData.value.header = storeClassify.classData.regions[chartData.value.stat.region];
});

</script>

<template>
  <div class="container py-3">
    <HeaderDiv :page-header="`Статистика по региону ${chartData.header} c ${chartData.stat.start} по ${chartData.stat.end}`" />
    <div class="form form-check" role="form">
      <input class="form-check-input" type="radio" id="bar" name="bar"
        v-model="chartData.radio" value="bar">
      <label class="form-check-label" for="chart">Гистограмма</label>
    </div>
    <div class="form form-check" role="form">
      <input class="form-check-input" type="radio" id="line" name="line"
        v-model="chartData.radio" value="line">
      <label class="form-check-label" for="table">Линейный график</label>
    </div>

    <div v-if="chartData.radio === 'bar'">
      <Bar v-if="chartData.loaded" 
                :data="chartData.bar" 
                :options="chartData.options" />
    </div>
    
    <div v-if="chartData.radio === 'line'">
      <Line v-if="chartData.loaded" 
                   :data="chartData.line" 
                   :options="chartData.options" />
    </div>

    <div v-if="chartData.radio === 'bar'" class="py-3">
      <table class="table table-hover table-responsive align-middle">
        <caption>Решения по кандидатам</caption>
        <thead><tr><th width="45%">Решение</th><th>Количество</th></tr></thead>
        <tbody>
          <tr height="50px" v-for="(value, index) in Object.keys(chartData.barSummed)" 
              :key="index">
            <td >{{ value }}</td><td>{{Object.values(chartData.barSummed)[index]}}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="chartData.radio === 'line'" class="py-3">
      <table class="table table-hover table-responsive align-middle">
        <caption>Статистика по кандидатам</caption>
        <thead>
          <tr>
            <th v-for="label, index in chartData.line.labels" :key="index">
              {{ mapped_month[label as keyof typeof mapped_month] }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td v-for="check, index in chartData.lineSummed.map(obj => 
                        Object.values(obj)[0])" 
                      :key="index">
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
          <tr height="50px" v-for="(value, name, index) in chartData.stat.pfo" :key="index">
            <td >{{name}}</td><td>{{value}}</td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div class="py-3">
      <form @submit.prevent="chartData.submitData" class="form form-check" role="form">
          <div class="mb-3 row required">
            <label class="col-form-label col-md-2" for="region">Регион</label>
            <div class="col-md-2">
              <select :disabled="storeLogin.userData.region_id != '1'"
                      @change="chartData.submitData" 
                      class="form-select" id="region" name="region" 
                      v-model="chartData.stat.region">
                <option :value="storeLogin.userData.region_id" selected>
                  {{ storeClassify.classData.regions[storeLogin.userData.region_id] }}</option>
                <option v-for="name, value in storeClassify.classData.regions" 
                        :key="value" :value="value">{{name}}</option>                
              </select>
            </div>
            <label class="col-form-label col-md-1" for="start">Период:</label>
            <div class="col-md-2">
              <input class="form-control" id="start" name="start" required type="date" 
                  v-model="chartData.stat.start">
            </div>
            <div class="col-md-2">
              <input class="form-control" name="end" required type="date" 
                  v-model=chartData.stat.end>
            </div>
            <div class="col-md-2">
              <button class="btn btn-primary btn-md" name="submit" type="submit">
                  Принять</button>
            </div>
          </div>
      </form>
    </div>
  </div>
</template>
