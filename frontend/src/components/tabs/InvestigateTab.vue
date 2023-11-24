<script setup lang="ts">

import { defineAsyncComponent } from 'vue';
import { profileStore } from '@/store/profile';

const InvestigationForm = defineAsyncComponent(() => import('@components/forms/InvestigationForm.vue'));
const CollapseDiv = defineAsyncComponent(() => import('@components/elements/CollapseDiv.vue'));
const InvestigateDiv = defineAsyncComponent(() => import('@components/tabs/divs/InvestigateDiv.vue'));

const storeProfile = profileStore();

</script>


<template>
  <div class="py-3">
    <InvestigationForm v-if="(storeProfile.dataProfile.action === 'update' 
                            || storeProfile.dataProfile.action === 'create') 
                          && storeProfile.dataProfile.flag === 'investigation'" />
    <div v-else>
      <div v-if="storeProfile.dataProfile.inquisition.length">
        <CollapseDiv v-for="item, idx in storeProfile.dataProfile.inquisition" :key="idx" 
                          :id="item['id']" :idx="idx">
          <InvestigateDiv :item="item" 
                          :deleteItem="storeProfile.dataProfile.deleteItem"
                          :openForm="storeProfile.dataProfile.openForm"
                          :submitFile="storeProfile.dataProfile.submitFile"/>
        </CollapseDiv>
      </div>
      <p v-else >Данные отсутствуют</p>
      <div class="py-3">
        <a class="btn btn-outline-primary" type="button"
          @click="storeProfile.dataProfile.openForm('investigation', 'create')">Добавить запись
        </a>
      </div>
    </div>
  </div>
</template>