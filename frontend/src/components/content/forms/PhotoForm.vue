<script setup lang="ts">
// компонент для загрузки и отображения фото пользователя

import { ref } from 'vue';
import { appAuth } from '@store/auth';
import { appAlert } from '@/store/alert';
import { appProfile } from '@/store/profile';
import server from '@store/server';

const storeAuth = appAuth();
const storeAlert = appAlert();
const storeProfile = appProfile();

// Файл с изображением
const file = ref(null);

/**
 * Submits a file to the server.
 *
 * @param {Event} event - The event triggering the file submission.
 * @return {Promise<void>} A promise that resolves when the file is successfully submitted.
 */
async function submitPhoto(event: Event): Promise<void> {
  event.preventDefault();
  const formData = new FormData();
  const fileInput = file.value as HTMLInputElement | null;
  // Если файл выбран и размер не превышает 2 МБ
  if (fileInput && fileInput.files && fileInput.files[0].size < 2097152) {
    formData.append('file', fileInput.files[0]);
    
    try {
      const response = await storeAuth.axiosInstance.post(`${server}/photo/upload/${storeProfile.candId}`, formData);
      const { result } = response.data;
      // Обновляем сообщение
      storeAlert.alertAttr = result ? "alert-success" : "alert-warning";
      storeAlert.alertText = result ? 'Фото добавлено' : 'Ошибка при добавлении фото';
      // Отправка события в родительский компонент для обновления карточки
      storeProfile.getProfile();

    } catch (error) {
      console.error(error);
    } 
  
  } else {
    // Обновляем сообщение, если размер файла превышает 2 МБ
    storeAlert.alertAttr = "alert-warning";
    storeAlert.alertText = 'Ошибка. Возможно размер файла более 2 МБ';
  }
};

</script>

<template>
  <div class="py-3">
    <div class="card" style="width: 18rem;">
      <img :src="storeProfile.anketa.resume.path + '/photos/image.jpg'" class="card-img-top" alt="...">
        <div class="card-body">
      </div>
      <form class="form form-check" enctype="multipart/form-data" role="form" @change="submitPhoto">
        <input class="form-control form-control-sm" id="file" type="file" accept="image/*" ref="file">
      </form>
    </div>
  </div>
</template>
