import { defineStore } from 'pinia';
import { ref } from 'vue';
import { authStore } from '@/store/token';
import { classifyStore } from './classify';
import { Chart } from '@/share/interfaces';
import { server } from '@/share/utilities';

export const informationStore = defineStore('informationStore', () => {

  const storeAuth = authStore();
  const storeClassify = classifyStore();
    
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
  return {   
    header,
    loaded,
    stat,
    barData,
    lineData,
    chartOptions,
    summedBarData,
    summedLineData,
    submitData
  };
});