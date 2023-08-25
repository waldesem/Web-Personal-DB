import { defineStore } from 'pinia'
import axios from 'axios';
import server from '../store/server';
import { ref, Ref } from 'vue';


export const appLocation = defineStore('appLocation', () => {
  
  interface Region {
    [key: string]: string;
  };
  
  const regionsObject: Ref<Region> = ref({});

  async function getRegions() {
    const resp = await axios.get(`${server}/locations`);
    regionsObject.value = resp.data
  };

  return { regionsObject, getRegions }
})
