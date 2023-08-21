<script setup lang="ts">

import { appUsers } from '@store/users';
import { appClassify } from '@/store/classify';
import { appLocation } from '@/store/location';

const storeUsers = appUsers();

const storeLocation = appLocation();

const classifyApp = appClassify();

</script>

<template>
  <div class="py-2">
    <form @submit.prevent="storeUsers.submitData" class="form form-check" role="form">
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="fullname">Имя пользователя:</label>
        <div class="col-lg-10">
          <input autocomplete="fullname" class="form-control" minlength="3" maxlength="25" name="fullname" 
              required type="text" v-model="storeUsers.profile.fullname" pattern="[a-zA-Zа-яА-Я ]+">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="username">Учетная запись:</label>
        <div class="col-lg-10">
          <input :disabled="storeUsers.action === 'edit'" autocomplete="username" class="form-control" minlength="3" maxlength="25" name="username" 
              required type="text" v-model="storeUsers.profile.username" pattern="[a-zA-Z]+">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="email">Электронная почта:</label>
        <div class="col-lg-10">
          <input autocomplete="email" class="form-control" minlength="3" maxlength="25" name="email" 
              required type="email" v-model="storeUsers.profile.email">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="role">Роль</label>
        <div class="col-lg-10">
          <select class="form-select" id="role" name="role" v-model="storeUsers.profile.role" required>
              <option v-for="(value, name) in classifyApp.role" :value=value :key="name">{{name}}</option>                
              </select>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="region">Регион</label>
        <div class="col-lg-10">
          <select class="form-select" id="region" name="region" v-model="storeUsers.profile.region_id" required>
              <option v-for="name, value in storeLocation.regionsObject" :key="value" :value="value">{{name}}</option>                
              </select>
        </div>
      </div>
      <div class=" row">
        <div class="offset-lg-2 col-lg-10">
          <div class="btn-group">
            <button class="btn btn-outline-primary" name="submit" type="submit">{{storeUsers.action === 'create' ? 'Создать' : 'Изменить'}}</button>
            <button class="btn btn-outline-primary" name="cancel" type="button" @click="$emit('updateAction')">Отмена</button>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>