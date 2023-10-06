<script setup lang="ts">

import { profileStore } from '@/store/profile';

const storeProfile = profileStore();

</script>

<template>
  <form @submit.prevent="storeProfile.updateItem" class="form form-check" role="form">
    <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="theme">Тема проверки</label>
      <div class="col-lg-10">
        <select class="form-select" id="theme" name="theme" required 
                v-model="storeProfile.itemForm['theme']">
          <option value="Проверка кандидата">Проверка кандидата</option>
          <option value="Служебная проверка">Служебная проверка</option>
          <option value="Служебное расследование">Служебное расследование</option>
          <option value="Другое">Другое</option>
        </select>
      </div>
    </div>
    <div class="mb-3 row required">
      <label class="col-form-label col-lg-2" for="results">Результат</label>
      <div class="col-lg-10">
        <textarea class="form-control" id="results" name="results" required 
                  v-model="storeProfile.itemForm['results']"></textarea>
      </div>
    </div>
    <div class=" row">
      <div class="offset-lg-2 col-lg-10">
        <div class="btn-group" role="group">
          <button class="btn btn-outline-primary" type="submit">Принять</button>
          <button class="btn btn-outline-primary" type="reset">Очистить</button>
          <button class="btn btn-outline-primary" type="button" 
                  @click="storeProfile.cancelEdit">Отмена</button>
        </div>
      </div>
    </div>
  </form>
</template>