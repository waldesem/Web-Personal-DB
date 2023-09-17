<template>
  <div class="py-3">
    <div class="card" style="width: 18rem;">
      <img class="card-img-top" :src="imgUrl">
    </div>
    <form enctype="multipart/form-data" @change="submitPhoto">
      <div class="py-1">
        <input id="file" name="file" type="file" accept="image/*" ref="file">
      </div>
    </form>
  </div>
</template>

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

const file = ref(null);
const imgUrl = ref(new URL(`${storeProfile.anketa.resume.path}/images/person.jpg`, import.meta.url).href);

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

  if (fileInput && fileInput.files && fileInput.files[0].size < 2097152) {
    formData.append('file', fileInput.files[0]);
    
    try {
      const response = await storeAuth.axiosInstance.post(`${server}/photo/upload/${storeProfile.candId}`, formData);
      const { result } = response.data;

      storeAlert.alertAttr = result ? "alert-success" : "alert-warning";
      storeAlert.alertText = result ? 'Фото добавлено' : 'Ошибка при добавлении фото';

      storeProfile.getProfile();

    } catch (error) {
      console.error(error);
    } 
  
  } else {
    storeAlert.alertAttr = "alert-warning";
    storeAlert.alertText = 'Ошибка. Возможно размер файла более 2 МБ';
  }
};

</script>
