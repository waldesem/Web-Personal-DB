<script setup lang="ts">

import { adminStore } from '@store/admin';
import { classifyStore } from '@/store/classify';
import { alertStore } from '@store/alert';
import { authStore } from '@/store/token';
import { server } from '@share/utilities';

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
  try {  
    const response = storeAdmin.userData.userAct === 'edit' 
      ? await storeAuth.axiosInstance.patch(`${server}/user`, storeAdmin.formData)
      : await storeAuth.axiosInstance.post(`${server}/user`, storeAdmin.formData);
    const { message } = response.data;

    const resp = {
      'Created': ['alert-success', 'Пользователь успешно создан'],
      'Patched': ['alert-success', 'Пользователь успешно изменен'],
    };
    storeAlert.setAlert(resp[message as keyof typeof resp][0],
                        resp[message as keyof typeof resp][1]);

    storeAdmin.userData.userAct === 'edit' 
      ? storeAdmin.userAction('view', storeAdmin.userData.userId) 
      : storeAdmin.getUsers();

  } catch (error) {
    console.error(error);
    storeAlert.setAlert('alert-danger', 'Ошибка сохранения данных');
  };
};

</script>

<template>
  <div class="modal fade" id="modalUser" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered modal-xl" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="modaUserLabel">
            {{ storeAdmin.userData.userAct === 'edit' ? 'Изменить пользователя' : 'Создать пользователя'}}
          </h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">

          <form @submit.prevent="submitUser" class="form form-check" role="form">
            <div class="mb-3 row">
              <label class="col-form-label col-lg-2" for="fullname">Имя пользователя:</label>
              <div class="col-lg-10">
                <input autocomplete="fullname" class="form-control" minlength="1" maxlength="250" 
                      name="fullname" required type="text" placeholder="Петров Петр Петрович" 
                      pattern="[a-zA-Zа-яА-Я ]+"
                      v-model="storeAdmin.formData.fullname">
              </div>
            </div>
            <div class="mb-3 row">
              <label class="col-form-label col-lg-2" for="username">Учетная запись:</label>
              <div class="col-lg-10">
                <input :disabled="storeAdmin.userData.userAct === 'edit'" 
                        autocomplete="username" class="form-control" minlength="1" maxlength="250" 
                        name="username" required type="text" placeholder="PPetrov" pattern="[a-zA-Z]+"
                        v-model="storeAdmin.formData.username">
              </div>
            </div>
            <div class="mb-3 row">
              <label class="col-form-label col-lg-2" for="email">Электронная почта:</label>
              <div class="col-lg-10">
                <input autocomplete="email" class="form-control" name="email" 
                    required type="email" placeholder="petrov@petrov.ru" 
                    v-model="storeAdmin.formData.email">
              </div>
            </div>
            <div class="mb-3 row">
              <label class="col-form-label col-lg-2" for="region">Регион</label>
              <div class="col-lg-10">
                <select class="form-select" id="region" name="region" 
                        v-model="storeAdmin.formData.region_id" required>
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

        </div>
      </div>
    </div>
  </div>
</template>