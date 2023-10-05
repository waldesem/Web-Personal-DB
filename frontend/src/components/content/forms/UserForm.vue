<script setup lang="ts">

import { adminStore } from '@store/admin';
import { classifyStore } from '@/store/classify';
import { alertStore } from '@store/alert';
import { authStore } from '@/store/token';
import server from '@store/server';

const storeAdmin = adminStore();
const storeClassify = classifyStore();
const storeAuth = authStore();
const storeAlert = alertStore();

/**
 * Submits data to the server.
 *
 * @return {Promise<void>} A promise that resolves when the data is 
 * successfully submitted.
 */
async function submitUser(): Promise<void>{
  const formData = {
    'fullname': storeAdmin.profileData.fullname,
    'username': storeAdmin.profileData.username,
    'email': storeAdmin.profileData.email,
    'region_id': storeAdmin.profileData.region_id,
  };
  try {  
    const response = storeAdmin.userData.userAct === 'edit' 
      ? await storeAuth.axiosInstance.patch(`${server}/user`, formData)
      : await storeAuth.axiosInstance.post(`${server}/user`, formData);
    const { message } = response.data;

    const resp = {
      'Created': ['alert-success', 'Пользователь успешно создан'],
      'Patched': ['alert-success', 'Пользователь успешно изменен'],
    }
    storeAlert.setAlert(resp[message as keyof typeof resp][0],
                        resp[message as keyof typeof resp][1]);

    storeAdmin.userData.userAct === 'edit' 
      ? storeAdmin.userAction('view', storeAdmin.userData.userId) 
      : storeAdmin.getUsers();

    storeAdmin.userData.userId = '';

  } catch (error) {
    console.error(error);
    storeAlert.setAlert('alert-danger', 'Ошибка сохранения данных');
  };

  storeAdmin.userData.userAct = '';
  Object.assign(storeAdmin.profileData, {
    fullname: '',
    username: '',
    email: '',
    region_id: '',
  });
};

</script>

<template>
  <form @submit.prevent="submitUser" class="form form-check" role="form">
    <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="fullname">Имя пользователя:</label>
      <div class="col-lg-10">
        <input autocomplete="fullname" class="form-control" minlength="" maxlength="250" 
               name="fullname" required type="text" placeholder="Петров Петр Петрович" 
               pattern="[a-zA-Zа-яА-Я ]+"
               v-model="storeAdmin.profileData.fullname">
      </div>
    </div>
    <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="username">Учетная запись:</label>
      <div class="col-lg-10">
        <input :disabled="storeAdmin.userData.userAct === 'edit'" 
                autocomplete="username" class="form-control" minlength="8" maxlength="250" 
                name="username" required type="text" placeholder="a-z, A-Z" pattern="[a-z]+"
                v-model="storeAdmin.profileData.username">
      </div>
    </div>
    <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="email">Электронная почта:</label>
      <div class="col-lg-10">
        <input autocomplete="email" class="form-control" name="email" 
            required type="email" placeholder="petrov@petrov.ru" 
            v-model="storeAdmin.profileData.email">
      </div>
    </div>
    <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="region">Регион</label>
      <div class="col-lg-10">
        <select class="form-select" id="region" name="region" 
                v-model="storeAdmin.profileData.region_id" required>
          <option v-for="name, value in storeClassify.classifyItems.regions" 
                  :key="value" :value="value">
            {{name}}
          </option>                
        </select>
      </div>
    </div>
    <div class=" row">
      <div class="offset-lg-2 col-lg-10">
        <div class="btn-group">
          <button class="btn btn-outline-primary" name="submit" type="submit" data-bs-dismiss="modal">
            {{storeAdmin.userData.userAct === 'create' ? 'Создать' : 'Изменить'}}
          </button>
          <button class="btn btn-outline-primary" name="reset" type="reset">Очистить</button>
          <button class="btn btn-outline-primary" name="cancel" type="button" 
                  @click="storeAdmin.userData.userAct = ''" data-bs-dismiss="modal" >Отмена</button>
        </div>
      </div>
    </div>
  </form>
</template>