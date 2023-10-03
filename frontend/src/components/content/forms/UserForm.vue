<script setup lang="ts">

import { storeAdmin } from '@store/admin';
import { classifyStore } from '@/store/classify';

const adminStore = storeAdmin();
const storeClassify = classifyStore();

</script>

<template>
  <div class="py-2">
    <form @submit.prevent="adminStore.submitUserData" class="form form-check" role="form">
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="fullname">Имя пользователя:</label>
        <div class="col-lg-10">
          <input autocomplete="fullname" class="form-control" minlength="" maxlength="250" name="fullname" 
              required type="text" v-model="adminStore.profileData.fullname" placeholder="Петров Петр Петрович" pattern="[a-zA-Zа-яА-Я ]+">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="username">Учетная запись:</label>
        <div class="col-lg-10">
          <input :disabled="adminStore.userData.userAct === 'edit'" autocomplete="username" class="form-control" minlength="8" maxlength="250" name="username" 
              required type="text" v-model="adminStore.profileData.username" placeholder="a-z, A-Z" pattern="[a-z]+">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="email">Электронная почта:</label>
        <div class="col-lg-10">
          <input autocomplete="email" class="form-control" name="email" 
              required type="email" placeholder="petrov@petrov.ru" v-model="adminStore.profileData.email">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="region">Регион</label>
        <div class="col-lg-10">
          <select class="form-select" id="region" name="region" v-model="adminStore.profileData.region_id" required>
            <option v-for="name, value in storeClassify.regions" :key="value" :value="value">{{name}}</option>                
          </select>
        </div>
      </div>
      <div class=" row">
        <div class="offset-lg-2 col-lg-10">
          <div class="btn-group">
            <button class="btn btn-outline-primary" name="submit" type="submit">{{adminStore.userData.userAct === 'create' ? 'Создать' : 'Изменить'}}</button>
            <button class="btn btn-outline-primary" name="reset" type="reset">Очистить</button>
            <button class="btn btn-outline-primary" name="cancel" type="button" @click="adminStore.userData.userAct = ''">Отмена</button>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>