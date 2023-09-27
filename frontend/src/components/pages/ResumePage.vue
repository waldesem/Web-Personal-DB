<script setup lang="ts">

import ResumeForm from '@content/forms/ResumeForm.vue';
import { appProfile } from '@/store/profile';


const storeProfile = appProfile();
storeProfile.action = 'update';

</script>

<template>
    <div class="container py-3">
        <div class="py-5"><h4>Создать анкету</h4></div>
        <form class="form form-check" enctype="multipart/form-data" role="form" 
                @change="storeProfile.submitFile($event, 'anketa')">
            <div class="mb-3 row">
            <label class="col-form-label col-lg-2" for="file">Загрузить файл</label>
            <div class="col-lg-10">
                <input class="form-control" id="file" type="file" accept=".xlsx" ref="file">
            </div>
            </div>
        </form>
        <ResumeForm />
    </div>
</template>