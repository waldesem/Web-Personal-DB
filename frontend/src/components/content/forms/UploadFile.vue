<script setup lang="ts">

import { ref } from 'vue';
import { appAuth } from '@store/auth';
import { appAlert } from '@store/alert';
import server from '@store/server';

const storeAuth = appAuth();

const storeAlert = appAlert();

const emit = defineEmits(['updateItem'])

// Переменная для загрузки файла
const file = ref(null);
    

/**
 * Submits a file for upload.
 *
 * @param {Event} event - The event object.
 * @return {Promise<void>} A promise that resolves when the file is successfully uploaded.
 */
async function submitFile(event: Event): Promise<void> {
  event.preventDefault();
  
  const formData = new FormData();
  const fileInput = file.value as HTMLInputElement | null;
  if (fileInput && fileInput.files) {
    formData.append('file', fileInput.files[0]);
    
    try {
      const response = await storeAuth.axiosInstance.post(`${server}/resume/upload`, formData);
      const { result, person_id } = response.data;
      // Обновляем сообщение
      storeAlert.alertAttr = result ? "alert-info" : "alert-success";
      storeAlert.alertText = result ? 'Анкета уже существует. Данные обновлены' : 'Анкета успешно добавлена';
      // Отправка события в родительский компонент для обновления карточки 
      emit('updateItem', person_id)
    
    } catch (error) {
      console.error(error);
    }
  
  } else {
    storeAlert.alertAttr = "alert-warning";
    storeAlert.alertText = "Ошибка при загрузке файла";
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
