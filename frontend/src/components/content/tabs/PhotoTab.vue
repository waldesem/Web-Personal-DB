<script setup lang="ts">
// компонент для загрузки и отображения фото пользователя

import { ref } from 'vue';
import { appAuth } from '@store/auth';
import { appAlert } from '@/store/alert';
import server from '@store/server';

const storeAuth = appAuth();

const storeAlert = appAlert();

const emit = defineEmits(['updateItem', 'getProfile']);

// Данные из родительского компонента: путь к файлу и ID кандидата
const props = defineProps({
  path: String,
  candId: String,
});

// Файл с изображением
const file = ref(null);


/**
 * Submits a file to the server.
 *
 * @param {Event} event - The event triggering the file submission.
 * @return {Promise<void>} A promise that resolves when the file is successfully submitted.
 */
async function submitFile(event: Event): Promise<void> {
  event.preventDefault();
  const formData = new FormData();
  const fileInput = file.value as HTMLInputElement | null;
  // Если файл выбран и размер не превышает 2 МБ
  if (fileInput && fileInput.files && fileInput.files[0].size < 2097152) {
    formData.append('file', fileInput.files[0]);
    
    try {
      const response = await storeAuth.axiosInstance.post(`${server}/photo/${props.candId}`, formData);
      const { result } = response.data;
      // Обновляем сообщение
      storeAlert.alertAttr = result ? "alert-success" : "alert-warning";
      storeAlert.alertText = result ? 'Фото добавлено' : 'Ошибка при добавлении фото';
      // Отправка события в родительский компонент для обновления карточки
      emit('getProfile', String(props.candId))

    } catch (error) {
      console.error(error);
    } 
  
  } else {
    // Обновляем сообщение, если размер файла превышает 2 МБ
    storeAlert.alertAttr = "alert-warning";
    storeAlert.alertText = 'Ошибка. Возможно размер файла более 2 МБ';
  }
}

</script>

<template>
  <div class="py-3">
    <div class="row">
      <div class="carousel slide" id="carouselPhoto" data-bs-ride="carousel">
        <div class="carousel-inner">
          <div class="carousel-item active" v-for="(photo, index) in props.path" :key="index">
            <img :src="server + '/images' + photo" class="d-block w-100" alt="...">
          </div>
        </div>
        <button class="carousel-control-prev" type="button" data-bs-target="#carouselPhoto" data-bs-slide="prev">
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Previous</span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#carouselPhoto" data-bs-slide="next">
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Next</span>
        </button>
      </div>
      <form class="form form-check" enctype="multipart/form-data" role="form" @change="submitFile">
        <input class="form-control form-control-sm" id="file" type="file" accept="image/*" ref="file">
      </form>
    </div>
  </div>
</template>
