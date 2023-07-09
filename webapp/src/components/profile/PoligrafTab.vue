<template>
  <div v-if="url" class="py-3">
    <form @submit.prevent="submitData" class="form form-check" role="form"  id="poligrafFormId">
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="theme">Тема проверки</label>
        <div class="col-lg-10">
          <select class="form-select" id="theme" name="theme">
            <option value="Проверка кандидата">Проверка кандидата</option>
            <option value="Служебная проверка">Служебная проверка</option>
            <option value="Служебное расследование">Служебное расследование</option>
            <option value="Другое">Другое</option>
          </select>
        </div>
      </div>
      <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="results">Информация</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="results" name="results" required></textarea>
        </div>
      </div>
      <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="deadline">Дата проведения</label>
        <div class="col-lg-10">
          <input class="form-control" id="deadline" name="deadline" required type="date" value="">
        </div>
      </div>
      <div class=" row">
        <div class="offset-lg-2 col-lg-10">
          <div class="btn-group" role="group">
            <button class="btn btn-outline-primary" type="submit">Принять</button>
            <button class="btn btn-outline-primary" type="reset">Очистить</button>
            <button class="btn btn-outline-primary" type="button" @click="url = ''">Отмена</button>
          </div>
        </div>
      </div>
    </form>
  </div>

  <template v-else>
    <div v-html="table" class="py-3"></div>
    <a @click="url = 'poligraf'" class="btn btn-outline-primary" type="button">Добавить запись</a>
  </template>
</template>

<script setup lang="ts">

import axios from 'axios';
import { ref, toRefs } from 'vue';
import config from '@/config';

const props = defineProps({
  table: String,
  candId: String
});

const { table, candId } = toRefs(props);
  
const emit = defineEmits(['updateMessage', 'updateItem']);

const url = ref('');


async function submitData(event: Event) {
  try {
    const formData = new FormData(event.target as HTMLFormElement);
    const response = await axios.post(`${config.appUrl}/${url.value}/${candId?.value}`, formData, {
      headers: {'Authorization': `Bearer ${config.token}` 
      }
    });
    const { message } = response.data;
    emit('updateMessage', {
      attr: "alert-primary",
      text: message
    });
    emit('updateItem', candId?.value);
    url.value = ''
  } catch (error) {
    console.error(error);
  }
}

</script>
