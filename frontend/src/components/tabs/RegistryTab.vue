<script setup lang="ts">
 
import { ref, defineAsyncComponent } from 'vue';
import { profileStore } from '@/store/profile';
import { classifyStore } from '@/store/classify';
import { loginStore } from '@/store/login';

const RegistryForm = defineAsyncComponent(() => import('@components/forms/RegistryForm.vue'));
const CollapseDiv = defineAsyncComponent(() => import('@components/elements/CollapseDiv.vue'));
const RegistryDiv = defineAsyncComponent(() => import('@components/tabs/divs/RegistryDiv.vue'));

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
      <div v-if="storeProfile.dataProfile.register.length">
        <CollapseDiv v-for="item, idx in storeProfile.dataProfile.register" :key="idx" 
            :id="'registry' + idx" :idx="idx" :label="'Согласование #' + (idx + 1)">
          <RegistryDiv :item="item" />
        </CollapseDiv>
      </div>
      <p v-else >Данные отсутствуют</p>
      <div class="d-print-none py-3">
        <a class="btn btn-outline-primary" type="button"
          @click="storeProfile.dataProfile.openForm('registry', 'create')">Добавить запись
        </a>
      </div>
    </div>
  </div>
</template>