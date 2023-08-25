<script setup lang="ts">
// компонент для отображения формы добавления и редактирования данных 
 
import { appProfile } from '@/store/profile';

const storeProfile = appProfile();

</script>

<template>
   <form @submit.prevent="storeProfile.updateItem" class="form form-check" role="form">
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="view">Выбрать</label>
        <div class="col-lg-10">
        <select class="form-select" id="view" name="view" v-model="storeProfile.itemForm['view']">
            <option value="Адрес регистрации">Адрес регистрации</option>
            <option value="Адрес проживания">Адрес проживания</option>
            <option value="Другое">Другое</option>
        </select>
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="region">Регион</label>
        <div class="col-lg-10">
        <input class="form-control" id="region" maxlength="250" name="region" type="text" v-model="storeProfile.itemForm['region']">
        </div>
    </div>
    <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="address">Полный адрес</label>
        <div class="col-lg-10">
        <input class="form-control" id="address" maxlength="250" name="address" required type="text" v-model="storeProfile.itemForm['address']">
        </div>
    </div>
    <div class=" row">
        <div class="offset-lg-2 col-lg-10">
            <button class="btn btn-outline-primary btn-md" name="submit" type="submit">Принять</button>
        </div>
    </div>
  </form>
</template>
