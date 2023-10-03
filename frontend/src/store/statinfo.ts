import { defineStore } from 'pinia';
import { ref } from 'vue';
import { classifyStore } from '@store/classify';
import { authStore } from '@store/token';
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

export const statStore = defineStore('statStore', () => {
  
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

  const storeClassify = classifyStore();
  const storeAuth = authStore();

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
  const barData = ref<ChartInterface>({
    labels: [],
    datasets: []
  });
  const lineData = ref<ChartInterface>({
    labels: [],
    datasets: []
  });
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false
  };


  const stat = ref({
    region: 1,
    checks: [], 
    pfo: [],
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
    
    stat.value.pfo = poligraf;
    stat.value.checks = candidates;

    const decisions = [...new Set(stat.value.checks.map(result => result['decision']))];

    barData.value = {
      labels: decisions,
      datasets: [
        {
          label: 'Решения по кандидатам',
          backgroundColor: ['#f87979', '#fbc02d', '#2a9d8f', '#e9c46a', '#e76f51'], 
          data: stat.value.checks.filter(result => 
            result['decision']).map(result => result['count'])
        }
      ]
    };

    lineData.value = {
      labels: stat.value.checks.map(result => result['month']),
      datasets: decisions.map((decision) => {
        return {
          label: decision,
          data: stat.value.checks.filter(result => 
            result['decision'] === decision).map(result => result['count']),
          borderColor: ['#f87979', '#fbc02d', '#2a9d8f', '#e9c46a', '#e76f51'],
          backgroundColor: ['#f87979', '#fbc02d', '#2a9d8f', '#e9c46a', '#e76f51'],
          fill: false
        };
      })
    };

    loaded.value = true;
  };

    return {loaded, stat, barData, lineData, chartOptions, header, submitData }
  });