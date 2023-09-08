<script setup lang="ts">

import { appLogin } from '@/store/login';
import { ref } from 'vue';

const storeLogin = appLogin();

const hidePassword = ref(true);


</script>

<template>
  <div class="py-3">
    <form @submit.prevent="storeLogin.submitData" class="form form-check" role="form">
      <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="username">Логин: </label>
        <div class="col-lg-6">
          <input autocomplete="username" class="form-control" required id="username" name="username" type="text"
            v-model.trim="storeLogin.loginData.username" minlength="4" maxlength="16" 
            placeholder="От 8 до 16 символов: a-z, A-Z" pattern="[a-zA-Z]+">
        </div>
      </div>
      <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="password">Пароль: </label>
        <div class="col-lg-6">
          <div class="input-group">
            <input autocomplete="current-password" class="form-control" required id="password" name="password"
              :type="hidePassword ? 'password' : 'text'" v-model.trim="storeLogin.loginData.password" minlength="8" maxlength="16" 
              placeholder="От 8 до 16 символов: 0-9, a-z, A-Z" pattern="[0-9a-zA-Z]+">
            <span class="input-group-text">
                <a role="button" @click="hidePassword = !hidePassword">
                  <i :class="hidePassword ? 'bi bi-eye' : 'bi bi-eye-slash'"></i>
                </a>
            </span>
          </div>
          <div v-if="storeLogin.action === 'login'" class="py-2">
            <a @click="storeLogin.action = 'password'" href="#">Изменить пароль</a>
          </div>
        </div>
      </div>
      <div v-if="storeLogin.action === 'password'">
        <div class="mb-3 row required">
          <label class="col-form-label col-lg-2" for="new_pswd">Новый: </label>
          <div class="col-lg-6">
            <input autocomplete="current-password" class="form-control" required name="new_pswd" :type="hidePassword ? 'password' : 'text'"
              v-model.trim="storeLogin.loginData.new_pswd" minlength="8" maxlength="16" 
              placeholder="Латинские буквы и цифры 8-16 символов" pattern="[0-9a-zA-Z]+">
          </div>
        </div>
        <div class="mb-3 row required">
          <label class="col-form-label col-lg-2" for="conf_pswd">Повтор: </label>
          <div class="col-lg-6">
            <input autocomplete="current-password" class="form-control" required name="conf_pswd" :type="hidePassword ? 'password' : 'text'"
              v-model.trim="storeLogin.loginData.conf_pswd" minlength="8" maxlength="16" 
              placeholder="Латинские буквы и цифры 8-16 символов" pattern="[0-9a-zA-Z]+">
          </div>
        </div>
      </div>
      <div class=" row">
        <div class="offset-lg-2 col-lg-">
          <button class="btn btn-primary btn-md" name="submit" type="submit">{{ storeLogin.action === 'login' ? 'Войти' :
            'Изменить' }}</button>
        </div>
      </div>
    </form>
  </div>
</template>