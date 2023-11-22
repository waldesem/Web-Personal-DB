<script setup lang="ts">

import { profileStore } from '@/store/profile';

const storeProfile = profileStore();

</script>


<template>
  <div class="py-3">
    <form @submit.prevent="storeProfile.dataProfile.submitResume" class="form form-check" role="form">
      <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="category">Категория</label>
        <div class="col-lg-10">
          <select class="form-select" required id="category" name="category" 
                  v-model="storeProfile.dataProfile.form['category']">
            <option value="Кандидат">Кандидат</option>
            <option value="Проверяемое лицо">Проверяемое лицо</option>
          </select>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="fullname">Полное ФИО*</label>
        <div class="col-lg-10">
            <input class="form-control" maxlength="250" id="fullname" name="fullname" type="text"
                   v-model="storeProfile.dataProfile.form['fullname']" required>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="previous">Изменение имени</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="250" id="previous" name="previous" type="text"
                 v-model="storeProfile.dataProfile.form['previous']">
        </div>
        </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="birthday">Дата рождения*</label>
        <div class="col-lg-10">
          <input class="form-control" id="birthday" name="birthday" required type="date"
                 v-model="storeProfile.dataProfile.form['birthday']" 
                 :max="new Date().toISOString().split('T')[0]">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="birthplace">Место рождения</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="250" id="birthplace" name="birthplace" type="text"
                 v-model="storeProfile.dataProfile.form['birthplace']" >
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="country">Гражданство</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="50" id="country" name="country" type="text"
                 v-model="storeProfile.dataProfile.form['country']" >
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="ext_country">Двойное гражданство</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="50" id="ext_country" name="ext_country" type="text"
                 v-model="storeProfile.dataProfile.form['ext_country']" >
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="snils">СНИЛС</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="11" minlength="11" id="snils" name="snils" type="text"
                 v-model="storeProfile.dataProfile.form['snils']" pattern="\d{11}">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="inn">ИНН</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="12" minlength="12" id="inn" name="inn" type="text"
                 v-model="storeProfile.dataProfile.form['inn']" pattern="\d{12}">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="education">Образование</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="250" id="education" name="education" type="text"
                 v-model="storeProfile.dataProfile.form['education']" >
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="marital">Семенное положение</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="250" id="marital" name="marital" type="text"
                 v-model="storeProfile.dataProfile.form['marital']" >
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="addition">Дополнительно</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="addition" name="addition"
                    v-model="storeProfile.dataProfile.form['addition']" ></textarea>
        </div>
      </div>
      <div class=" row">
        <div class="offset-lg-2 col-lg-10">
          <div class="btn-group" role="group">
            <button class="btn btn-outline-primary" type="submit">Принять</button>
            <button class="btn btn-outline-primary" type="reset">Очистить</button>
            <router-link v-if="storeProfile.dataProfile.action !== 'update'" 
                    class="btn btn-outline-primary" type="button"
                    :to="{ name: 'persons', params: { group: 'staffsec' }}">
                    Отмена
            </router-link>
            <button v-else class="btn btn-outline-primary" type="button" 
                    @click="storeProfile.dataProfile.cancelEdit">Отмена</button>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>
