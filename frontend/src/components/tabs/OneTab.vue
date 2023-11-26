<script setup lang="ts">

import { defineAsyncComponent } from 'vue';
import { profileStore } from '@/store/profile';

const OneDiv = defineAsyncComponent(() => import('@components/tabs/divs/OneDiv.vue'));
const CollapseDiv = defineAsyncComponent(() => import('@components/elements/CollapseDiv.vue'));

const storeProfile = profileStore();

</script>

<template>
  <div class="py-3">
    <div v-if="storeProfile.dataProfile.ones?.length" >
      <CollapseDiv v-for="item, idx in storeProfile.dataProfile.ones" :key="idx" 
          :id="'ones' + idx" :idx="idx" :label="'1C #' + (idx + 1)">
        <OneDiv :item="item" />
      </CollapseDiv>
    </div>
    <p v-else >Данные отсутствуют</p>
  </div>
</template>