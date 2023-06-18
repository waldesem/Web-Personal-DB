<template>
  <form class="form form-check" enctype="multipart/form-data" role="form" @change="submitFile">
    <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="file">Загрузить файл</label>
      <div class="col-lg-10">
        <input class="form-control" type="file" ref="file">
      </div>
    </div>
  </form>
</template>


<script setup lang="ts">

import { defineEmits, ref } from 'vue';
import axios from 'axios';

const emit = defineEmits(['updateMessage', 'updateItem'])
const file = ref(null);
    
async function submitFile(event: Event) {
  event.preventDefault();
  const formData = new FormData();
  const fileInput = file.value as HTMLInputElement | null;
  if (fileInput && fileInput.files) {
    formData.append('file', fileInput.files[0]);
  }
  try {
    const response = await axios.post(`http://localhost:5000/resume/upload`, formData, {
      headers: {'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`}
    });
    const { message, cand_id } = response.data;
    emit('updateMessage', {
      attr: "alert-success",
      text: message
    });
    console.log(cand_id);
    emit('updateItem', {candId: cand_id})
  } catch (error) {
    console.error(error);
  }
}

</script>

