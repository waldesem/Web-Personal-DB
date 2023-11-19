<script setup lang="ts">

import { loginStore } from '@/store/login';

const storeLogin = loginStore();

</script>

<template>
  <div class="border border-primary rounded p-5 ">
  <h5>{{ storeLogin.formData.action === 'login' ? 'Вход в систему' : 'Изменить пароль' }}</h5>
  <div class="py-3">
    <form @submit.prevent="storeLogin.submitLogin" class="form form-check" role="form">
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="username">Логин: </label>
        <div class="col-lg-6">
          <input autocomplete="username" class="form-control" required 
                id="username" name="username" type="text" minlength="4" maxlength="16" 
                placeholder="Логин пользователя" pattern="[a-zA-Z]+"
                v-model.trim="storeLogin.formData.data['username']">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="password">Пароль: </label>
        <div class="col-lg-6">
          <div class="input-group">
            <input autocomplete="current-password" class="form-control" required 
                  id="password" name="password" minlength="8" maxlength="16" 
                  placeholder="Пароль пользователя" pattern="[0-9a-zA-Z]+"
                  :type="storeLogin.formData.password ? 'password' : 'text'" 
                  v-model.trim="storeLogin.formData.data['password']" >
            <span class="input-group-text">
              <a role="button" @click="storeLogin.formData.password = !storeLogin.formData.password">
                <i :class="storeLogin.formData.password ? 'bi bi-eye' : 'bi bi-eye-slash'"></i>
              </a>
            </span>
          </div>
          <div v-show="storeLogin.formData.action === 'login'" class="py-2">
            <a @click="storeLogin.formData.action = 'password'" href="#">Изменить пароль</a>
          </div>
        </div>
      </div>
      <div v-if="storeLogin.formData.action === 'password'">
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="new_pswd">Новый: </label>
          <div class="col-lg-6">
            <input autocomplete="current-password" class="form-control" required 
                  name="new_pswd" minlength="8" maxlength="16"
                  placeholder="От 8 до 16 символов: a-z, A-Z" pattern="[0-9a-zA-Z]+"
                  :type="storeLogin.formData.password ? 'password' : 'text'"
                  v-model.trim="storeLogin.formData.data['new_pswd']">
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="conf_pswd">Повтор: </label>
          <div class="col-lg-6">
            <input autocomplete="current-password" class="form-control" required 
                  name="conf_pswd" minlength="8" maxlength="16" 
                  placeholder="Повторите новый пароль" pattern="[0-9a-zA-Z]+"
                  :type="storeLogin.formData.password ? 'password' : 'text'"
                  v-model.trim="storeLogin.formData.data['conf_pswd']">
          </div>
        </div>
      </div>
      <div class="row mb-3">
        <div class="offset-lg-2 col-lg-10">
            <button class="btn btn-primary btn-md" name="submit" type="submit">
              {{ storeLogin.formData.action === 'login' ? 'Войти' : 'Изменить' }}
            </button>              
              &nbsp;
            <button v-show="storeLogin.formData.action === 'password'" class="btn btn-secondary btn-md" 
                    type="button" @click="storeLogin.formData.action = 'login'">Отменить
            </button>
        </div>
      </div>
    </form>
  </div>
  </div>
</template>