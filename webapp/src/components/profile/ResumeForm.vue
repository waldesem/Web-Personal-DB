<template>
    <form @submit.prevent="submitData" class="form form-check" role="form">
      <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="region">Регион</label>
        <div class="col-lg-10">
          <select class="form-select" v-model="region" name="region">
            <option value="ГО">ГО</option>
            <option value="Томск">Томск</option>
            <option value="РЦ Запад">РЦ Запад</option>
            <option value="РЦ Юг">РЦ Юг</option>
            <option value="РЦ Запад">РЦ Запад</option>
            <option value="РЦ Урал">РЦ Урал</option>
          </select>
        </div>
      </div>
      <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="fullname">Полное ФИО</label>
        <div class="col-lg-10">
            <input class="form-control" maxlength="250" v-model="fullname" name="fullname" required type="text">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="previous">Изменение имени</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="250" v-model="previous" name="previous" type="text">
        </div>
        </div>
      <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="birthday">Дата рождения</label>
        <div class="col-lg-10">
          <input class="form-control" v-model="birthday" name="birthday" required type="date">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="birthplace">Место рождения</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="250" v-model="birthplace" name="birthplace" type="text">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="country">Гражданство</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="50" v-model="country" name="country" type="text">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="snils">СНИЛС</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="11" minlength="11" v-model="snils" name="snils" type="text">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="inn">ИНН</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="12" minlength="12" v-model="inn" name="inn" type="text">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="education">Образование</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="250" v-model="education" name="education" type="text">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="addition">Дополнительно</label>
        <div class="col-lg-10">
          <textarea class="form-control" v-model="addition" name="addition"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="recruiter">Рекрутер</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="250" v-model="recruiter" name="recruiter" type="text">
        </div>
      </div>
      <div class=" row">
        <div class="offset-lg-2 col-lg-10">
          <div class="btn-group" role="group">
            <button class="btn btn-outline-primary" type="submit">Принять</button>
            <button class="btn btn-outline-primary" type="reset">Очистить</button>
            <button class="btn btn-outline-primary" type="button" @click="$emit('cancelEdit')">Отмена</button>
          </div>
        </div>
      </div>
    </form>
</template>

<script setup lang="ts">

import { ref, toRefs } from 'vue'
import axios from 'axios';
import appUrl from '@/main';

const emit = defineEmits (['updateMessage', 'updateItem', 'cancelEdit']);

const props = defineProps({
  resume: Object
});

const resume  = toRefs(props).resume;

let region: string;
let fullname: string;
let previous: string;
let birthday: string;
let birthplace: string;
let country: string;
let snils: string;
let inn: string;
let education: string;
let addition: string;
let recruiter: string;

if (resume) {
  const resumeValue = resume.value;
  if (resumeValue) {
    region = ref(resumeValue.region);
    fullname = ref(resumeValue.fullname);
    previous = ref(resumeValue.previous);
    birthday = ref(resumeValue.birthday);
    birthplace = ref(resumeValue.birthplace);
    country = ref(resumeValue.country);
    snils = ref(resumeValue.snils);
    inn = ref(resumeValue.inn);
    education = ref(resumeValue.education);
    addition = ref(resumeValue.addition);
    recruiter = ref(resumeValue.recruiter)
  }
}

async function submitData(event: Event) {
  try {
    const formData = new FormData(event.target as HTMLFormElement);
    const response = await axios.post(`${appUrl}/resume/create`, formData, {
      headers: {'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`}
    });
    const { message, cand_id } = response.data;
    emit('updateMessage', {
      attr: "alert-success",
      text: message
    });
    emit('updateItem', {candId: cand_id});
  } catch (error) {
    console.error(error);
  }
}

</script>

