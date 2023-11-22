<script setup lang="ts">
 
import { ref } from 'vue';
import { profileStore } from '@/store/profile';
import { classifyStore } from '@/store/classify';
import { loginStore } from '@/store/login';
import RegistryForm from '@components/forms/RegistryForm.vue';
import RegistryAccord from '@components/tabs/accordions/RegistryAccord.vue';

const storeProfile = profileStore();
const classifyApp = classifyStore();
const storeLogin = loginStore();

const disableRegBtn = ref(false);
disableRegBtn.value = (storeProfile.dataProfile.resume['status'] 
                      !== classifyApp.classData.status['result'])
                    || !storeLogin.userData.hasRole('superuser')
</script>

<template>
  <div class="py-3">

    <RegistryForm v-if="storeProfile.dataProfile.action === 'create' 
                     && storeProfile.dataProfile.flag === 'registry'" />
    
    <div v-else>
      <RegistryAccord :store="storeProfile.dataProfile"></RegistryAccord>
      <div class="py-3">
        <button class="btn btn-outline-primary" type="button"
                :disabled="disableRegBtn" 
                @click="storeProfile.dataProfile.openForm('registry', 'create')">Добавить запись
        </button>
      </div>
    </div>
  </div>
</template>