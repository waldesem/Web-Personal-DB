<script setup lang="ts">

import { appProfile } from '@/store/profile';

const storeProfile = appProfile();


</script>

<template>
  <form class="form form-check" enctype="multipart/form-data" role="form" @change="storeProfile.submitFile($event)">
    <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="file">Загрузить файл</label>
      <div class="col-lg-10">
        <input class="form-control" id="file" type="file" accept=".xlsx" ref="file">
      </div>
    </div>
  </form>
</template>
