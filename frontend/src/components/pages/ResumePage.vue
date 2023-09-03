<script setup lang="ts">

import UploadFile from '@content/forms/UploadFile.vue';
import ResumeForm from '@content/forms/ResumeForm.vue';
import { appProfile } from '@/store/profile';


const storeProfile = appProfile();
storeProfile.action = 'update';

</script>

<template>
    <div class="container py-5">
        <div class="py-5"><h4>Создать анкету</h4></div>
        <UploadFile />
        <ResumeForm />
    </div>
</template>