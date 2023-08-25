<script setup lang="ts">
// компонент формы добавления или редактирования резюе

import { appProfile } from '@/store/profile';

const storeProfile = appProfile();


</script>
<template>
  <div class="py-3">
    <form @submit.prevent="storeProfile.submitResume" class="form form-check" role="form">
      <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="category">Категория</label>
        <div class="col-lg-10">
          <select class="form-select" required v-model="storeProfile.itemForm['category']" id="category" name="category">
            <option value="Кандидат">Кандидат</option>
            <option value="Проверяемое лицо">Проверяемое лицо</option>
          </select>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="fullname">Полное ФИО*</label>
        <div class="col-lg-10">
            <input class="form-control" maxlength="250" v-model="storeProfile.itemForm['fullname']" id="fullname" name="fullname" required type="text">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="previous">Изменение имени</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="250" v-model="storeProfile.itemForm['previous']" id="previous" name="previous" type="text">
        </div>
        </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="birthday">Дата рождения*</label>
        <div class="col-lg-10">
          <input class="form-control" v-model="storeProfile.itemForm['birthday']" id="birthday" name="birthday" required type="date" :max="new Date().toISOString().split('T')[0]">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="birthplace">Место рождения</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="250" v-model="storeProfile.itemForm['birthplace']" id="birthplace" name="birthplace" type="text">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="country">Гражданство</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="50" v-model="storeProfile.itemForm['country']" id="country" name="country" type="text">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="snils">СНИЛС</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="11" minlength="11" v-model="storeProfile.itemForm['snils']" id="snils" name="snils" type="text">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="inn">ИНН</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="12" minlength="12" v-model="storeProfile.itemForm['inn']" id="inn" name="inn" type="text">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="education">Образование</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="250" v-model="storeProfile.itemForm['education']" id="education" name="education" type="text">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="addition">Дополнительно</label>
        <div class="col-lg-10">
          <textarea class="form-control" v-model="storeProfile.itemForm['addition']" id="addition" name="addition"></textarea>
        </div>
      </div>
      <div class=" row">
        <div class="offset-lg-2 col-lg-10">
          <div class="btn-group" role="group">
            <button class="btn btn-outline-primary" type="submit">Принять</button>
            <button class="btn btn-outline-primary" type="reset">Очистить</button>
            <button v-if="storeProfile.action !== 'update'" class="btn btn-outline-primary" type="button" @click="storeProfile.redirectMain">Отмена</button>
            <button v-else class="btn btn-outline-primary" type="button" @click="storeProfile.cancelEdit">Отмена</button>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>
