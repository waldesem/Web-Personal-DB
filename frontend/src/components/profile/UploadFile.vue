<script setup lang="ts">

import { ref } from 'vue';
import axios from 'axios';
import config from '../../config';

const emit = defineEmits(['updateMessage', 'updateItem'])

const file = ref(null);
    
async function submitFile(event: Event) {
  event.preventDefault();
  const formData = new FormData();
  const fileInput = file.value as HTMLInputElement | null;
  if (fileInput && fileInput.files) formData.append('file', fileInput.files[0]);
  try {
    const response = await axios.post(`${config.appUrl}/resume/upload`, formData, {
      headers: {'Authorization': `Bearer ${localStorage.getItem('access_token')}`}
    });
    const { result, person_id } = response.data;
    emit('updateMessage', {
      attr: result ? "alert-info" : "alert-success",
      text: result ? 'Анкета уже существует. Данные обновлены' : 'Анкета успешно добавлена'
    });
    emit('updateItem', person_id)
  } catch (error) {
    console.error(error);
  }
}

</script>

<template>
  <form class="form form-check" enctype="multipart/form-data" role="form" @change="submitFile">
    <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="file">Загрузить файл</label>
      <div class="col-lg-10">
        <input class="form-control" id="file" type="file" accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" ref="file">
      </div>
    </div>
  </form>
</template>

