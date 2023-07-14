<template>
  <div class="py-3">
    <template v-if="url">
      <form @submit.prevent="submitData" class="form form-check" role="form" id="registryFormId">
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="comments">Комментарий</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="comments" name="comments"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="decision">Решение</label>
          <div class="col-lg-10">
            <select class="form-select" id="decision" name="decision">
              <option value="СОГЛАСОВАНО">СОГЛАСОВАНО</option>
              <option value="СОГЛАСОВАНО С КОММЕНТАРИЕМ">СОГЛАСОВАНО С КОММЕНТАРИЕМ</option>
              <option value="ОТКАЗАНО В СОГЛАСОВАНИИ">ОТКАЗАНО В СОГЛАСОВАНИИ</option>
              <option value="ОТМЕНЕНО">ОТМЕНЕНО</option>
            </select>
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
    </template>

    <template v-else>
      <div v-html="table"></div>
      <button @click="url = 'registry'" class="btn btn-outline-primary" type="button">Добавить запись</button>
    </template>
  </div>
</template>

<script setup lang="ts">

import axios from 'axios';
import { ref } from 'vue';
import config from '@/config';
  
const props = defineProps({
  table: String,
  candId: String
});

const emit = defineEmits(['updateItem','updateMessage']);

const url = ref('');

async function submitData(event: Event) {
  try {
    const formData = new FormData(event.target as HTMLFormElement);
    const response = await axios.post(`${config.appUrl}/registry/${props.candId}`, formData, {
      headers: {'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`}
    });
    const { message } = response.data;
    const alert = {
      'result': ['alert-success', 'Согласование отправлено'],
      'cancel': ['alert-warning', 'Отправка не удалась'],
      'error': ['alert-danger', 'Возникла ошибка']
    }
    emit('updateMessage', {
      attr: alert[message as keyof typeof alert][0],
      text: alert[message as keyof typeof alert][1]
    });
    url.value = '';
    emit('updateItem', props.candId);
  } catch (error) {
    console.error(error);
  }
}

</script>
