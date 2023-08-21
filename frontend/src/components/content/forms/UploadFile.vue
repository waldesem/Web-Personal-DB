<script setup lang="ts">

import { appAnketa } from '@/store/anketa';

const storeAnketa = appAnketa();

</script>

<template>
  <form class="form form-check" enctype="multipart/form-data" role="form" @change="storeAnketa.submitFile">
    <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="file">Загрузить файл</label>
      <div class="col-lg-10">
        <input class="form-control" id="file" type="file" accept=".xlsx" storeAnketa.file="file">
      </div>
    </div>
  </form>
</template>
