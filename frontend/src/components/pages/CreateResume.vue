<script setup lang="ts">

import router from '@/router/router';
import UploadFile from '@content/UploadFile.vue';
import ResumeForm from '@content/ResumeForm.vue';

const emit = defineEmits(['updateMessage', 'updateItem']);


/**
 * Updates an item based on the given response ID.
 *
 * @param {string} resp_id - The ID of the response.
 * @return {undefined} This function does not return a value.
 */
function updateProfile(resp_id: string): undefined {
  // редирект на страницу профиля после успешного создания анкеты
  router.push({ name: 'profile', params: { id: resp_id } });
};

</script>

<template>
    <div class="container py-3">
        <div class="py-5"><h4>Создать анкету</h4></div>
        <UploadFile @updateMessage="emit('updateMessage')" 
                    @updateItem="updateProfile"/>
        <ResumeForm @cancelEdit="router.push({ name: 'persons' })" 
                    @updateMessage="emit('updateMessage')" 
                    @updateItem="updateProfile" />
    </div>
</template>