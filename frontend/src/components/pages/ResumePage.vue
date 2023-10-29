<script setup lang="ts">

import { onBeforeRouteLeave } from 'vue-router';
import { profileStore } from '@/store/profile';
import { clearItem } from '@share/utilities'
import ResumeForm from '@components/forms/ResumeForm.vue';
import HeaderDiv from '@components/layouts/HeaderDiv.vue';

const storeProfile = profileStore();
storeProfile.action = 'create';

onBeforeRouteLeave((_to: any, _from: any, next: () => void) => {
  clearItem(storeProfile.itemForm);
  next()
});

</script>

<template>
  <div class="container py-3">
    <HeaderDiv :page-header="'Создать анкету'" />
    <form class="form form-check" enctype="multipart/form-data" role="form" 
            @change="storeProfile.submitFile($event, 'anketa')">
        <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="file">Загрузить файл</label>
        <div class="col-lg-10">
            <input class="form-control" id="file" type="file" accept=".xlsx, .csv" ref="file">
        </div>
        </div>
    </form>
    <ResumeForm />
  </div>
</template>