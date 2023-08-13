<script setup lang="ts">

import { toRefs } from 'vue'
import { locationStore } from '@store/location';
import { appClassify } from '@store/classify';
import { appAuth } from '@store/auth';
import server from '@store/server';

const storeAuth = appAuth()

const storeLocation = locationStore();

const classifyApp = appClassify();

const emit = defineEmits(['updateMessage', 'updateAction']);

const props = defineProps({
  profile: Object,
  action: String
})

// Данные пользователя из родительского компонента или пустой объект
const profile = toRefs(props).profile?.value ?? {};

/**
 * Submits data to the server.
 *
 * @return {Promise<void>} A promise that resolves when the data is successfully submitted.
 */
async function submitData(): Promise<void>{
  try {  
    const response = await storeAuth.axiosInstance.post(`${server}/user/${props.action}`, {
      'fullname': profile.fullname,
      'username': profile.username,
      'email': profile.email,
      'region_id': profile.region_id,
      'role': profile.role
    });
    const  { user } = response.data;
    // Матчинг атрибута и текста сообщения
    const resp = {
      'create': ['alert-success', 'Пользователь успешно создан'],
      'edit': ['alert-success', 'Пользователь успешно изменен'],
      'none': ['alert-danger', 'Ошибка создания (пользователь существует)/редактирования']
    }
    emit('updateMessage', { 
      attr: resp[user as keyof typeof resp][0],
      text: resp[user as keyof typeof resp][1] 
    });
    emit('updateAction');

  } catch (error) {
    console.error(error);
  }
};


</script>

<template>
  <div class="py-2">
    <form @submit.prevent="submitData()" class="form form-check" role="form">
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="fullname">Имя пользователя:</label>
        <div class="col-lg-10">
          <input autocomplete="fullname" class="form-control" minlength="3" maxlength="25" name="fullname" 
              required type="text" v-model="profile.fullname" pattern="[a-zA-Zа-яА-Я ]+">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="username">Учетная запись:</label>
        <div class="col-lg-10">
          <input :disabled="props.action === 'edit'" autocomplete="username" class="form-control" minlength="3" maxlength="25" name="username" 
              required type="text" v-model="profile.username" pattern="[a-zA-Z]+">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="email">Электронная почта:</label>
        <div class="col-lg-10">
          <input autocomplete="email" class="form-control" minlength="3" maxlength="25" name="email" 
              required type="email" v-model="profile.email">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="role">Роль</label>
        <div class="col-lg-10">
          <select class="form-select" id="role" name="role" v-model="profile.role" required>
              <option v-for="(value, name) in classifyApp.role" :value=value :key="name">{{name}}</option>                
              </select>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="region">Регион</label>
        <div class="col-lg-10">
          <select class="form-select" id="region" name="region" v-model="profile.region_id" required>
              <option v-for="name, value in storeLocation.regionsObject" :value="value">{{name}}</option>                
              </select>
        </div>
      </div>
      <div class=" row">
        <div class="offset-lg-2 col-lg-10">
          <div class="btn-group">
            <button class="btn btn-outline-primary" name="submit" type="submit">{{props.action === 'create' ? 'Создать' : 'Изменить'}}</button>
            <button class="btn btn-outline-primary" name="cancel" type="button" @click="$emit('updateAction')">Отмена</button>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>