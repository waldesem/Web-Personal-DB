import { defineStore } from 'pinia'
import axios from 'axios';
import server from '../store/server';
import { ref, Ref } from 'vue';

interface Region {
  [key: string]: string;
}

export const appLocation = defineStore('appLocation', () => {
  
  const regionsObject: Ref<Region> = ref({});

  async function getRegions() {
    const resp = await axios.get(`${server}/locations`);
    regionsObject.value = resp.data
  };

  return { regionsObject, getRegions }
})
