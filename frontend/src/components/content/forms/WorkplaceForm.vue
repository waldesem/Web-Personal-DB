<script setup lang="ts">
// компонент для отображения формы добавления и редактирования данных 
 
import { appProfile } from '@/store/profile';

const storeProfile = appProfile();

</script>

<template>
   <form @submit.prevent="storeProfile.updateItem" class="form form-check" role="form">
    <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="start_date">Период работы</label>
        <div class="col-lg-2">
            <input class="form-control" id="start_date" name="start_date" type="date" v-model="storeProfile.itemForm['start_date']">
        </div> - 
        <div class="col-lg-2">
            <input class="form-control" id="end_date" name="end_date" type="date" v-model="storeProfile.itemForm['end_date']">
        </div>
    </div>
    <div class="row">
        <div class="offset-lg-2 col-lg-10">
            <div class="mb-3 form-check">
                <input class="form-check-input" id="now_work" name="now_work" v-model="storeProfile.itemForm['now_work']" type="checkbox" value="y">
                <label class="form-check-label" for="now_work">Работает по н.в.</label>
            </div>
        </div>
    </div>
    <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="workplace">Место работы</label>
        <div class="col-lg-10">
        <input class="form-control" id="workplace" maxlength="250" name="workplace" required type="text" v-model="storeProfile.itemForm['workplace']">
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="address">Адрес организации</label>
        <div class="col-lg-10">
        <input class="form-control" id="address" maxlength="250" name="address" type="text" v-model="storeProfile.itemForm['address']">
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="position">Должность</label>
        <div class="col-lg-10">
        <input class="form-control" id="position" maxlength="250" name="position" type="text" v-model="storeProfile.itemForm['position']">
        </div>
    </div>
    <div class=" row">
        <div class="offset-lg-2 col-lg-10">
            <button class="btn btn-outline-primary btn-md" name="submit" type="submit">Принять</button>
        </div>
    </div>
    </form>
</template>
