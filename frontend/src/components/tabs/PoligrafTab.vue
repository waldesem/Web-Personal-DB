<script setup lang="ts">

import { profileStore } from '@/store/profile';
import PoligrafForm from '@components/forms/PoligrafForm.vue';
import PoligrafAccord from '@components/tabs/accordions/PoligrafAccord.vue';

const storeProfile = profileStore();

</script>

<template>
  <div class="py-3">
    
    <PoligrafForm v-if="(storeProfile.dataProfile.action === 'update' 
                  || storeProfile.dataProfile.action === 'create') 
                  && storeProfile.dataProfile.flag === 'poligraf'"/>
    
    <div v-else>
      <PoligrafAccord :store="storeProfile.dataProfile"></PoligrafAccord>
      <div class="py-3">
        <button class="btn btn-outline-primary" type="button"
                @click="storeProfile.dataProfile.openForm('poligraf', 'create')">Добавить запись
        </button>
      </div>
    </div>
  </div>
  
</template>