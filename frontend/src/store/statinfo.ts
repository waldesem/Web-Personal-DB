import { defineStore } from 'pinia';
import { ref } from 'vue';
import { appClassify } from '@store/classify';
import { appAuth } from '@store/token';
import server from '@store/server';
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

export const storeStatinfo = defineStore('storeStatinfo', () => {
  
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

  const storeClassify = appClassify();
  const storeAuth = appAuth();

  interface ChartInterface {
    labels: string[];
    datasets: {
      label: string;
      backgroundColor: string[];
      data: number[];
    }[];
  };

  const todayDate = new Date();
  const header = ref('');
  const loaded = ref(false);
  const chartData = ref<ChartInterface>({
    labels: [],
    datasets: []
  });
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false
  };


  const stat = ref({
    region: 1,
    checks: {}, 
    pfo: {},
    start: new Date(todayDate.getFullYear(), todayDate.getMonth(), 1).toISOString().slice(0,10),
    end: todayDate.toISOString().slice(0,10)
  });

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
    header.value = storeClassify.regions[stat.value.region];
    
    stat.value.checks = candidates;
    stat.value.pfo = poligraf;

    chartData.value = {
      labels: Object.keys(stat.value.checks) as string[],
      datasets: [
        {
          label: 'Статистика по кандидатам',
          backgroundColor: ['#f87979', '#fbc02d', '#2a9d8f', '#e9c46a', '#e76f51'], 
          data: Object.values(stat.value.checks) as number[]
        }
      ]
    };

    loaded.value = true;
  };

    return {loaded, stat, chartData, chartOptions, header, submitData }
  });