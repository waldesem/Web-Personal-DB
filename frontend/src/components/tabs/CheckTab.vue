<script setup lang="ts">

import { ref } from 'vue';
import { classifyStore } from '@store/classify';
import { profileStore } from '@/store/profile';
import  CheckForm from '@components/forms/CheckForm.vue';
import  CheckAccord from '@components/tabs/accordions/CheckAccord.vue';

const storeClassify = classifyStore();
const storeProfile = profileStore();

const hiddenAddBtn = ref(false);
const hiddenDelBtn = ref(false);
const hiddenEditBtn = ref(false);

hiddenDelBtn.value = storeProfile.dataProfile.resume['status'] 
                    === storeClassify.classData.status['finish'] 
                  || storeProfile.dataProfile.resume['status'] 
                    === storeClassify.classData.status['robot'];

hiddenEditBtn.value = storeProfile.dataProfile.resume['status'] 
                      !== storeClassify.classData.status['save'] 
                    && storeProfile.dataProfile.resume['status'] 
                      !== storeClassify.classData.status['cancel'] 
                    && storeProfile.dataProfile.resume['status'] 
                      !== storeClassify.classData.status['manual']

hiddenAddBtn.value = ![storeClassify.classData.status['new'], 
                      storeClassify.classData.status['update'], 
                      storeClassify.classData.status['save'], 
                      storeClassify.classData.status['repeat']].
                        includes(storeProfile.dataProfile.resume['status'])
</script>

<template>
  <div class="py-3">

    <CheckForm v-if="storeProfile.dataProfile.action === 'update' 
                    && storeProfile.dataProfile.flag === 'check'" />

    <div v-else>
      <CheckAccord :store="storeProfile.dataProfile" 
                   :hiddenDelBtn="hiddenDelBtn" 
                   :hiddeEditBtn="hiddenEditBtn"/>
      <div class="py-3">
        <button class="btn btn-outline-primary" 
                @click="storeProfile.dataProfile.getItem('check', 'add', storeProfile.dataProfile.candId)" 
                :disabled="hiddenAddBtn">Добавить проверку
        </button>
      </div>
    </div>
  </div>
</template>