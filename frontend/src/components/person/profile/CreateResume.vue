<script setup lang="ts">

import router from '@/router/router';
import UploadFile from './UploadFile.vue';
import ResumeForm from './ResumeForm.vue';

const emit = defineEmits(['updateMessage', 'updateItem']);


function updateItem(resp_id: string) {
  router.push({ name: 'profile', params: { id: resp_id } });
};

function updateMessage(alert: Object) {
  emit('updateMessage', alert)
};

</script>

<template>
    <div class="container py-3">
        <div class="py-5"><h4>Создать анкету</h4></div>
        <UploadFile @updateMessage="updateMessage" 
                    @updateItem="updateItem"/>
        <ResumeForm @cancelEdit="router.push({ name: 'persons' })" 
                    @updateMessage="updateMessage" 
                    @updateItem="updateItem" />
    </div>
</template>