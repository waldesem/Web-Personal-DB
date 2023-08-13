<script setup lang="ts">
// компонент формы добавления или редактирования резюе

import { toRefs } from 'vue'
import { appAuth } from '@store/auth';
import server from '@store/server';

const storeAuth = appAuth();

const emit = defineEmits (['updateMessage', 'getProfile', 'cancelEdit']);

// объект из родительского компонента
const props = defineProps({
  resume: Object
});

// создаем рективный объект из props или пустой объект
const resume = toRefs(props).resume?.value ?? {};


/**
 * Submits the data to the server to create a new resume.
 *
 * @return {Promise<void>} A promise that resolves when the data has been successfully submitted.
 */
async function submitData(): Promise<void> {
  try {
    const response = await storeAuth.axiosInstance.post(`${server}/resume/create`, resume);
    const { result, person_id } = response.data;
    
    emit('updateMessage', {
      attr: result ? "alert-info" : "alert-success",
      text: result ? 'Анкета уже существует. Данные обновлены' : 'Анкета успешно добавлена'
    });
    
    emit('getProfile', person_id);
  
  } catch (error) {
    console.error(error);
  }
}

</script>
<template>
  <div class="py-3">
    <form @submit.prevent="submitData" class="form form-check" role="form">
      <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="category">Категория</label>
        <div class="col-lg-10">
          <select class="form-select" required v-model="resume.category" id="category" name="category">
            <option value="Кандидат">Кандидат</option>
            <option value="Проверяемое лицо">Проверяемое лицо</option>
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
          <input class="form-control" v-model="resume.birthday" id="birthday" name="birthday" required type="date" :max="new Date().toISOString().split('T')[0]">
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
  </div>
</template>
