<script setup lang="ts">

import { profileStore } from '@/store/profile';

const storeProfile = profileStore();

</script>

<template v-if="(storeProfile.action === 'update'
              || storeProfile.action === 'create') 
              && storeProfile.flag === 'inquiry'">
  <form @submit.prevent="storeProfile.updateItem" class="form form-check" role="form">
    <div class="mb-3 row required">
      <label class="col-form-label col-lg-2" for="info">Информация</label>
      <div class="col-lg-10">
        <textarea class="form-control" id="info" name="info" required 
          v-model="storeProfile.dataProfile.itemForm['info']"></textarea>
      </div>
    </div>
    <div class="mb-3 row required">
      <label class="col-form-label col-lg-2" for="initiator">Инициатор</label>
      <div class="col-lg-10">
        <input class="form-control" id="initiator" maxlength="250" name="initiator" required type="text"  
          v-model="storeProfile.dataProfile.itemForm['initiator']">
      </div>
    </div>
    <div class="mb-3 row required">
      <label class="col-form-label col-lg-2" for="source">Источник</label>
      <div class="col-lg-10">
        <input class="form-control" id="source" maxlength="250" name="source" required type="text" 
          v-model="storeProfile.dataProfile.itemForm['source']">
      </div>
    </div>
    <div class=" row">
      <div class="offset-lg-2 col-lg-10">
        <div class="btn-group" role="group">
            <button class="btn btn-outline-primary" type="submit">Принять</button>
            <button class="btn btn-outline-primary" type="reset">Очистить</button>
            <button class="btn btn-outline-primary" type="button" 
                    @click="storeProfile.cancelEdit">Отмена</button>
          </div>
        </div>
    </div>
  </form>
</template>