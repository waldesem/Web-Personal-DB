<script setup lang="ts">

import axios from 'axios';
import config from '@/config';
import { ref } from 'vue';

const props = defineProps({
  photo: String,
  candId: String,
});

const file = ref(null);

const emit = defineEmits(['updateMessage', 'updateItem']);

async function submitFile(event: Event) {
  event.preventDefault();
  const formData = new FormData();
  const fileInput = file.value as HTMLInputElement | null;
  if (fileInput && fileInput.files) formData.append('file', fileInput.files[0]);
  try {
    const response = await axios.post(`${config.appUrl}/photo/upload/${props.candId}`, formData, {
      headers: {'Authorization': `Bearer ${localStorage.getItem('access_token')}`}
    });
    const { result } = response.data;
    updateMessage({
      attr: result ? "alert-success" : "alert-warning",
      text: result ? 'Фото добавлено' : 'Ошибка при добавлении фото'
    });
    updateItem(String(props.candId))
  } catch (error) {
    console.error(error);
  }
}

function updateMessage(alert: Object) {
  emit('updateMessage', alert)
};

function updateItem(resp_id: string) {
  emit('updateItem', resp_id);
};

</script>

<template>
  <div class="row py-3">
    <div class="col-3">
      <div class="card">
        <img :src="config.appUrl + props.photo" class="card-img-top" alt="Нет фото">
        <div class="card-body">
          <form class="form form-check" enctype="multipart/form-data" role="form" @change="submitFile">
            <input class="form-control form-control-sm" id="file" type="file" accept="image/*" ref="file">
          </form>
        </div>
      </div>
    </div>
    <div class="col-9"></div>
  </div>
</template>
