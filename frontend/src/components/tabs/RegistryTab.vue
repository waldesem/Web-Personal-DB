<script setup lang="ts">
 
import { profileStore } from '@/store/profile';
import { classifyStore } from '@/store/classify';
import { loginStore } from '@/store/login';
import RegistryForm from '@components/forms/RegistryForm.vue';

const storeProfile = profileStore();
const classifyApp = classifyStore();
const storeLogin = loginStore();

</script>

<template>
  <div class="py-3">

    <RegistryForm v-if="storeProfile.action === 'create' 
                     && storeProfile.flag === 'registry'" />
      
    <div v-else>
      <table v-if="storeProfile.profile.register.length" 
             v-for="tbl in storeProfile.profile.register" 
              :key="tbl['id']" class="table table-responsive">
        <thead>
          <tr><th width="25%">{{ tbl['id'] }}</th><th></th></tr>
        </thead>
        <tbody>
          <tr v-if="tbl['comments']">
            <td>Комментарий</td>
            <td>{{ tbl['comments'] }}</td>
          </tr>
          <tr v-if="tbl['decision']">
            <td>Решение</td>
            <td>{{ tbl['decision'] }}</td>
          </tr>
          <tr v-if="tbl['supervisor']">
            <td>Согласующий</td>
            <td>{{ tbl['supervisor'] }}</td>
          </tr>
          <tr>
            <td>Дата</td>
            <td>{{ tbl['deadline'] ? new Date(tbl['deadline']).toLocaleDateString('ru-RU') : '' }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
      <button class="btn btn-outline-primary" type="button"
              :disabled="storeProfile.profile.resume['status'] !== 
                          classifyApp.classifyItems.status['result']
                         || !storeLogin.hasRole('superuser')" 
              @click="storeProfile.action = 'create'; 
                      storeProfile.flag = 'registry';
                      storeProfile.itemForm = {}">Добавить запись
      </button>
    </div>
  
  </div>
</template>