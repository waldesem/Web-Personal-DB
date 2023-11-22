<script setup lang="ts">
// компонент для отображения формы добавления и редактирования данных 
 
import { profileStore } from '@/store/profile';

const storeProfile = profileStore();

</script>

<template>
   <form @submit.prevent="storeProfile.dataProfile.updateItem" class="form form-check" role="form">
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="view">Выбрать</label>
        <div class="col-lg-10">
        <select class="form-select" id="view" name="view" v-model="storeProfile.dataProfile.form['view']">
            <option value="Паспорт гражданина России">Паспорт гражданина России</option>
            <option value="Иностранный документ">Иностранный документ</option>
            <option value="Другое">Другое</option>
        </select>
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="series">Серия документа</label>
        <div class="col-lg-10">
        <input class="form-control" id="series" maxlength="25" name="series" type="text" v-model="storeProfile.dataProfile.form['series']">
        </div>
    </div>
    <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="number">Номер документа</label>
        <div class="col-lg-10">
        <input class="form-control" id="number" maxlength="25" name="number" required type="text" v-model="storeProfile.dataProfile.form['number']">
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="agency">Орган выдавший</label>
        <div class="col-lg-10">
        <input class="form-control" id="agency" maxlength="250" name="agency" type="text" v-model="storeProfile.dataProfile.form['agency']">
        </div>
    </div>
    <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="issue">Дата выдачи</label>
        <div class="col-lg-10">
        <input class="form-control" id="issue" name="issue" required type="date" v-model="storeProfile.dataProfile.form['issue']" :max="new Date().toISOString().split('T')[0]">
        </div>
    </div>
    <div class=" row">
        <div class="offset-lg-2 col-lg-10">
            <button class="btn btn-outline-primary btn-md" name="submit" type="submit">Принять</button>
        </div>
    </div>
    </form>
</template>
