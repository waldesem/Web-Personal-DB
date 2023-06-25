<template>
<div v-if="url" class="py-3">
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
          <option value="СОГЛАСОВАНО С РИСКОМ">СОГЛАСОВАНО С РИСКОМ</option>
          <option value="ОТКАЗАНО В СОГЛАСОВАНИИ">ОТКАЗАНО В СОГЛАСОВАНИИ</option>
          <option value="Отмена">Отмена</option>
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
</div>

  <template v-else>
    <div v-html="table" class="py-3"></div>
    <a @click="url = 'registry'" class="btn btn-outline-primary" type="button">Добавить запись</a>
  </template>
</template>

<script setup lang="ts">

import axios from 'axios';
import { ref, toRefs } from 'vue';
import appUrl from '@/config';
  
const props = defineProps({
  table: String,
  candId: String
});

const {table, candId} = toRefs(props);

const emit = defineEmits(['updateItem','updateMessage']);

const url = ref('');

async function submitData(event: Event) {
  try {
    const formData = new FormData(event.target as HTMLFormElement);
    const response = await axios.post(`${appUrl}/registry/${candId?.value}`, formData, {
      headers: {'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`
      }
    });
    const { message } = response.data;
    emit('updateMessage', {
      attr: "alert-success",
      text: message
    });
    url.value = '';
    emit('updateItem', candId?.value);
  } catch (error) {
    console.error(error);
  }
}

</script>
