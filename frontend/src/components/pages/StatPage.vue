<script setup lang="ts">

import { computed, onBeforeMount, ref } from 'vue';
import { Bar, Line } from 'vue-chartjs';
import { storeStatinfo } from '@/store/statinfo';
import { appClassify } from '@/store/classify';

const storeStat = storeStatinfo();
const storeClassify = appClassify();

const captions = ['Статистика по кандидатам', 'Статистика по полиграфу'];
const chartRadio = ref('bar');

// Отправка запроса на сервер перед монтированием компонента
onBeforeMount(async () => {
  storeStat.loaded = false;
  storeStat.submitData()
});

computed(() => {
  storeStat.header = storeClassify.regions[storeStat.stat.region];
});

</script>

<template>
  <div class="container py-5">
    <div class="py-5">
      <h4>Статистика по региону {{ storeStat.header }} за период c {{ storeStat.stat.start }} по {{ storeStat.stat.end }}</h4>
    </div>
    
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
      <Bar v-if="storeStat.loaded" :data="storeStat.chartData" :options="storeStat.chartOptions" />
    </div>
    
    <div v-if="chartRadio === 'line'">
      <Line v-if="storeStat.loaded" :data="storeStat.chartData" :options="storeStat.chartOptions" />
    </div>
    
    <div v-for="(tbl, index) in [storeStat.stat.checks, storeStat.stat.pfo]" :key="index" class="py-3">
      <table class="table table-hover table-responsive align-middle">
        <caption>{{captions[index]}}</caption>
        <thead><tr><th width="45%">Критерий</th><th>Количество</th></tr></thead>
        <tbody>
          <tr height="50px" v-for="(value, name, index) in tbl" :key="index">
            <td >{{name}}</td><td>{{value}}</td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div class="py-3">
      <form @submit.prevent="storeStat.submitData" class="form form-check" role="form">
          <div class="mb-3 row required">
            <label class="col-form-label col-md-2" for="region">Регион</label>
            <div class="col-md-2">
              <select class="form-select" id="region" name="region" v-model="storeStat.stat.region">
                <option value="" selected>Выберите регион</option>
                <option v-for="name, value in storeClassify.regions" :key="value" 
                    :value="value">{{name}}</option>                
              </select>
            </div>
            <label class="col-form-label col-md-1" for="start">Период:</label>
            <div class="col-md-2">
              <input class="form-control" id="start" name="start" required type="date" 
                  v-model="storeStat.stat.start">
            </div>
            <div class="col-md-2">
              <input class="form-control" name="end" required type="date" 
                  v-model=storeStat.stat.end>
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
