<script setup lang="ts">

import { onBeforeMount, ref, toRefs } from 'vue'
import axios from 'axios';
import config from '../../config';
import router from '../../router';


const props = defineProps({
  actions: String,
  userId: String,
  profile: Object
})

const profile = toRefs(props).profile?.value ?? {};

const data = ref({
  attr: '',
  text: '',
});

const regions = ref({});


onBeforeMount(async () => {
    const response = await axios.get(`${config.appUrl}/locations`);
    const locations  = response.data;
    regions.value = locations.reduce(
    (acc: {[key: number]: string}, obj: {id: number, region: string}) => {
    acc[obj.id] = obj.region;
    return acc;
    }, {}
  );
});


async function submitData(){
  try {  
    const response = await axios.post(`${config.appUrl}/admin/user/${props.userId}/post/${props.actions}`, {
      'fullname': profile.value.fullname, 
      'username': profile.value.username,
      'email': profile.value.email,
      'region_id': profile.value.region_id,
      'role': profile.value.role
      }, {
      headers: {'Authorization': `Bearer ${localStorage.getItem('access_token')}`}
    });
    const  { user } = response.data;
    
    const resp = {
      'create': ['alert-success', 'Пользователь успешно создан'],
      'edit': ['alert-success', 'Пользователь успешно изменен'],
      'none': ['alert-danger', 'Ошибка создания (пользователь существует)/редактирования']
    }
    data.value.attr = resp[user as keyof typeof resp][0];
    data.value.text = resp[user as keyof typeof resp][1];
    
    router.push({ name: 'users' })
  
  } catch (error) {
    console.error(error);
  }
};
  
</script>

<template>
  <div class="py-2">
    <form @submit.prevent="submitData()" class="form form-check" role="form">
      <div class="row mb-3">
      <div class="col-md-4">
          <div class="row">
          <label class="col-form-label col-lg-4" for="fullname">Имя пользователя:</label>
          <div class="col-lg-8">
              <input autocomplete="fullname" class="form-control" minlength="3" maxlength="25" name="fullname" 
              required type="text" v-model="profile.fullname" pattern="[a-zA-Z ]+">
          </div>
          </div>
      </div>
      <div class="col-md-4">
          <div class="row">
          <label class="col-form-label col-lg-4" for="username">Учетная запись:</label>
          <div class="col-lg-8">
              <input :disabled="props.actions === 'edit'" autocomplete="username" class="form-control" minlength="3" maxlength="25" name="username" 
              required type="text" v-model="profile.username" pattern="[a-zA-Z]+">
          </div>
          </div>
      </div>
      <div class="col-md-4">
          <div class="row">
          <label class="col-form-label col-lg-4" for="email">Электронная почта:</label>
          <div class="col-lg-8">
              <input autocomplete="email" class="form-control" minlength="3" maxlength="25" name="email" 
              required type="text" v-model="profile.email" pattern="[a-zA-Z]+">
          </div>
          </div>
      </div>
      </div>
      <div class="row mb-3">
      <div class="col-md-6">
          <div class="row">
          <label class="col-form-label col-lg-4" for="role">Роль:</label>
          <div class="col-lg-8">
              <select class="form-select" id="role" name="role" v-model="profile.role" required>
              <option v-for="(value, name) in config.roles" :value=value :key="name">{{name}}</option>                
              </select>
          </div>
          </div>
      </div>
      <div class="col-md-5">
          <div class="row">
          <label class="col-form-label col-lg-4" for="region">Регион:</label>
          <div class="col-lg-8">
              <select class="form-select" id="region" name="region" v-model="profile.region_id" required>
              <option v-for="name, value in regions" :value="value">{{name}}</option>                
              </select>
          </div>
          </div>
      </div>
      <div class="col-md-1">
          <button class="btn btn-outline-primary" name="submit" type="submit">{{props.actions === 'create' ? 'Создать' : 'Изменить'}}</button>
      </div>
      </div>
    </form>
  </div>
</template>../../router/router