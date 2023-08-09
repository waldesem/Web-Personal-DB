<script setup lang="ts">

import { ref } from 'vue';
import { appAuth } from '@store/auth';
import server from '@store/server';

const storeAuth = appAuth();

const props = defineProps({
  path: String,
  candId: String,
});

const file = ref(null);

const emit = defineEmits(['updateMessage', 'updateItem']);

async function submitFile(event: Event) {
  event.preventDefault();
  const formData = new FormData();
  const fileInput = file.value as HTMLInputElement | null;
  if (fileInput && fileInput.files && fileInput.files[0].size < 2097152) {
    formData.append('file', fileInput.files[0]);
    try {
      const response = await storeAuth.axiosInstance.post(`${server}/photo/${props.candId}`, formData);
      const { result } = response.data;
      updateMessage({
        attr: result ? "alert-success" : "alert-warning",
        text: result ? 'Фото добавлено' : 'Ошибка при добавлении фото'
      });
      updateItem(String(props.candId))
    } catch (error) {
      console.error(error);
    } 
  } else {
    updateMessage({
      attr: "alert-warning",
      text: 'Ошибка. Возможно размер файла более 2 МБ'
    });
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
  <div class="py-3">
  <div class="row">
    <div class="col-3">
      <div class="card">
        <img :src="server + '/images' + props.path" class="card-img-top" alt="Нет фото">
        <div class="card-body">
          <form class="form form-check" enctype="multipart/form-data" role="form" @change="submitFile">
            <input class="form-control form-control-sm" id="file" type="file" accept="image/*" ref="file">
          </form>
        </div>
      </div>
    </div>
    <div class="col-9"></div>
  </div>
  </div>
</template>
