<template>
  <div v-if="url" class="py-3">
    <form @submit.prevent="submitData" class="form form-check" role="form" id="inquiryFormId">
      <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="info">Информация</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="info" name="info" required></textarea>
        </div>
      </div>
      <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="initiator">Инициатор</label>
        <div class="col-lg-10">
          <input class="form-control" id="initiator" maxlength="250" name="initiator" required type="text" value="">
        </div>
      </div>
      <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="source">Источник</label>
        <div class="col-lg-10">
          <input class="form-control" id="source" maxlength="250" name="source" required type="text" value="">
        </div>
      </div>
      <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="deadline">Дата запроса</label>
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
    <a @click="url = 'inquiry'" class="btn btn-outline-primary" type="button">Добавить запись</a>
  </template>
</template>

<script setup lang="ts">

import axios from 'axios';
import { toRefs, ref } from 'vue';
import appUrl from '@/main';

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
    const response = await axios.post(`${appUrl}/${url.value}/${candId?.value}`, formData, {
      headers: {'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`
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
