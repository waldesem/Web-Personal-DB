<script setup lang="ts">

import { computed, onBeforeMount, ref, defineAsyncComponent } from 'vue';
import { onBeforeRouteLeave } from 'vue-router';
import { Bar, Line } from 'vue-chartjs';
import { loginStore } from '@store/login';
import { classifyStore } from '@/store/classify';
import { informationStore } from '@/store/information';
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

const HeaderDiv = defineAsyncComponent(() => import('@components/layouts/HeaderDiv.vue'));

const storeLogin = loginStore();
const storeClassify = classifyStore();
const storeInformation = informationStore();

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
  storeInformation.loaded = false;
  storeInformation.submitData()
});

onBeforeRouteLeave((_to: any, _from: any, next: () => void) => {
  storeInformation.loaded = false;
  next()
});

computed(() => {
  storeInformation.header = storeClassify.classifyItems.regions[storeInformation.stat.region];
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

</script>

<template>
  <div class="container py-3">
    <HeaderDiv :page-header="`Статистика по региону ${storeInformation.header} c ${storeInformation.stat.start} по ${storeInformation.stat.end}`" />
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
      <Bar v-if="storeInformation.loaded" 
                :data="storeInformation.barData" 
                :options="storeInformation.chartOptions" />
    </div>
    
    <div v-if="chartRadio === 'line'">
      <Line v-if="storeInformation.loaded" 
                   :data="storeInformation.lineData" 
                   :options="storeInformation.chartOptions" />
    </div>

    <div v-if="chartRadio === 'bar'" class="py-3">
      <table class="table table-hover table-responsive align-middle">
        <caption>Решения по кандидатам</caption>
        <thead><tr><th width="45%">Решение</th><th>Количество</th></tr></thead>
        <tbody>
          <tr height="50px" v-for="(value, index) in Object.keys(storeInformation.summedBarData)" 
              :key="index">
            <td >{{ value }}</td><td>{{Object.values(storeInformation.summedBarData)[index]}}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="chartRadio === 'line'" class="py-3">
      <table class="table table-hover table-responsive align-middle">
        <caption>Статистика по кандидатам</caption>
        <thead>
          <tr>
            <th v-for="label, index in storeInformation.lineData.labels" :key="index">
              {{ mapped_month[label as keyof typeof mapped_month] }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td v-for="check, index in storeInformation.summedLineData.map(obj => Object.values(obj)[0])" :key="index">
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
          <tr height="50px" v-for="(value, name, index) in storeInformation.stat.pfo" :key="index">
            <td >{{name}}</td><td>{{value}}</td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div class="py-3">
      <form @submit.prevent="storeInformation.submitData" class="form form-check" role="form">
          <div class="mb-3 row required">
            <label class="col-form-label col-md-2" for="region">Регион</label>
            <div class="col-md-2">
              <select :disabled="storeLogin.userData.region_id != '1'"
                      @change="storeInformation.submitData" 
                      class="form-select" id="region" name="region" 
                      v-model="storeInformation.stat.region">
                <option :value="storeLogin.userData.region_id" selected>
                  {{ storeClassify.classifyItems.regions[storeLogin.userData.region_id] }}</option>
                <option v-for="name, value in storeClassify.classifyItems.regions" 
                        :key="value" :value="value">{{name}}</option>                
              </select>
            </div>
            <label class="col-form-label col-md-1" for="start">Период:</label>
            <div class="col-md-2">
              <input class="form-control" id="start" name="start" required type="date" 
                  v-model="storeInformation.stat.start">
            </div>
            <div class="col-md-2">
              <input class="form-control" name="end" required type="date" 
                  v-model=storeInformation.stat.end>
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
