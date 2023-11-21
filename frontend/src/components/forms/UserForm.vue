<script setup lang="ts">

import { defineAsyncComponent } from 'vue';
import { adminStore } from '@store/admins';
import { classifyStore } from '@/store/classify';

const ModalWin = defineAsyncComponent(() => import('@components/layouts/ModalWin.vue'));

const storeAdmin = adminStore();
const storeClassify = classifyStore();

</script>

<template>
  <ModalWin :title ="storeAdmin.dataUsers.action === 'edit'
                ? 'Изменить пользователя' 
                : 'Создать пользователя'" 
              :size="'modal-xl'" :id="'modalUser'">
    <form @submit.prevent="storeAdmin.dataUsers.submitUser" class="form form-check" role="form">
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="fullname">Имя пользователя:</label>
        <div class="col-lg-10">
          <input autocomplete="fullname" class="form-control" minlength="1" maxlength="250" 
                name="fullname" required type="text" placeholder="Петров Петр Петрович" 
                pattern="[a-zA-Zа-яА-Я ]+"
                v-model="storeAdmin.dataUsers.form['fullname']">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="username">Учетная запись:</label>
        <div class="col-lg-10">
          <input :disabled="storeAdmin.dataUsers.action === 'edit'" 
                  autocomplete="username" class="form-control" minlength="1" maxlength="250" 
                  name="username" required type="text" placeholder="PPetrov" pattern="[a-zA-Z]+"
                  v-model="storeAdmin.dataUsers.form['username']">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="email">Электронная почта:</label>
        <div class="col-lg-10">
          <input autocomplete="email" class="form-control" name="email" 
              required type="email" placeholder="petrov@petrov.ru" 
              v-model="storeAdmin.dataUsers.form['email']">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="region">Регион</label>
        <div class="col-lg-10">
          <select class="form-select" id="region" name="region" 
                  v-model="storeAdmin.dataUsers.form['region_id']" required>
            <option v-for="name, value in storeClassify.classData.regions" 
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
              {{storeAdmin.dataUsers.action === 'create' ? 'Создать' : 'Изменить'}}
            </button>
            <button class="btn btn-outline-primary" name="reset" type="reset">
              Очистить
            </button>
            <button class="btn btn-outline-primary" name="cancel" type="button" 
                    @click="storeAdmin.dataUsers.action = ''" data-bs-dismiss="modal" >
              Отмена
            </button>
          </div>
        </div>
      </div>
    </form>
  </ModalWin>
</template>