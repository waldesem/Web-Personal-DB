<script setup lang="ts">

import { ref } from 'vue';
import { appAuth } from '@store/auth';
import server from '@store/server';

const storeAuth = appAuth();

const emit = defineEmits(['updateMessage', 'updateItem'])

const file = ref(null);
    

async function submitFile(event: Event) {
  event.preventDefault();
  
  const formData = new FormData();
  const fileInput = file.value as HTMLInputElement | null;
  if (fileInput && fileInput.files) {
    formData.append('file', fileInput.files[0]);
    
    try {
      const response = await storeAuth.axiosInstance.post(`${server}/resume/upload`, formData);
      const { result, person_id } = response.data;
      
      emit('updateMessage', {
        attr: result ? "alert-info" : "alert-success",
        text: result ? 'Анкета уже существует. Данные обновлены' : 'Анкета успешно добавлена'
      });
      
      emit('updateItem', person_id)
    
    } catch (error) {
      console.error(error);
    }
  
  } else {
    emit('updateMessage', {
      attr: "alert-warning",
      text: "Загрузите файл"
    });
  }
}

</script>

<template>
  <form class="form form-check" enctype="multipart/form-data" role="form" @change="submitFile">
    <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="file">Загрузить файл</label>
      <div class="col-lg-10">
        <input class="form-control" id="file" type="file" accept=".xlsx" ref="file">
      </div>
    </div>
  </form>
</template>
