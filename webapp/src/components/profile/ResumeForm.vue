<template>
    <form @submit.prevent="submitData" class="form form-check" role="form">
      <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="region">Регион</label>
        <div class="col-lg-10">
          <select class="form-select" required v-model="resume.region" id="region" name="region">
            <option value="ГО">ГО</option>
            <option value="Томск">Томск</option>
            <option value="РЦ Запад">РЦ Запад</option>
            <option value="РЦ Юг">РЦ Юг</option>
            <option value="РЦ Запад">РЦ Запад</option>
            <option value="РЦ Урал">РЦ Урал</option>
          </select>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="fullname">Полное ФИО</label>
        <div class="col-lg-10">
            <input class="form-control" maxlength="250" v-model="resume.fullname" id="fullname" name="fullname" required type="text">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="previous">Изменение имени</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="250" v-model="resume.previous" id="previous" name="previous" type="text">
        </div>
        </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="birthday">Дата рождения</label>
        <div class="col-lg-10">
          <input class="form-control" v-model="resume.birthday" id="birthday" name="birthday" required type="date">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="birthplace">Место рождения</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="250" v-model="resume.birthplace" id="birthplace" name="birthplace" type="text">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="country">Гражданство</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="50" v-model="resume.country" id="country" name="country" type="text">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="snils">СНИЛС</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="11" minlength="11" v-model="resume.snils" id="snils" name="snils" type="text">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="inn">ИНН</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="12" minlength="12" v-model="resume.inn" id="inn" name="inn" type="text">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="education">Образование</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="250" v-model="resume.education" id="education" name="education" type="text">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="addition">Дополнительно</label>
        <div class="col-lg-10">
          <textarea class="form-control" v-model="resume.addition" id="addition" name="addition"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="recruiter">Рекрутер</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="250" v-model="resume.recruiter" id="recruiter" name="recruiter" type="text">
        </div>
      </div>
      <div class=" row">
        <div class="offset-lg-2 col-lg-10">
          <div class="btn-group" role="group">
            <button class="btn btn-outline-primary" type="submit">Принять</button>
            <button class="btn btn-outline-primary" type="reset">Очистить</button>
            <button class="btn btn-outline-primary" type="button" @click="emit('cancelEdit')">Отмена</button>
          </div>
        </div>
      </div>
    </form>
</template>

<script setup lang="ts">

import { toRefs } from 'vue'
import axios from 'axios';
import config from '@/config';
import { onBeforeRouteLeave } from 'vue-router';

const emit = defineEmits (['updateMessage', 'updateItem', 'cancelEdit']);

const props = defineProps({
  resume: Object
});

const resume = toRefs(props).resume?.value ?? {};

async function submitData(event: Event) {
  try {
    const response = await axios.post(`${config.appUrl}/resume/create`, resume, {
      headers: {'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`}
    });
    const { result, cand_id } = response.data;
    emit('updateMessage', {
      attr: result ? "alert-info" : "alert-success",
      text: result ? 'Анкета уже существует. Данные обновлены' : 'Анкета успешно добавлена'
    });
    emit('updateItem', String(cand_id));
  } catch (error) {
    console.error(error);
  }
}

onBeforeRouteLeave((to, from) => {
  const answer = window.confirm('Вы действительно хотите покинуть страницу?');
  if (!answer) return false
})

</script>