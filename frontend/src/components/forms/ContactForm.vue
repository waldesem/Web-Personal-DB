<script setup lang="ts">

import { computed } from 'vue';
import { profileStore } from '@/store/profile';

const storeProfile = profileStore();

const view = computed(() => {
  if (storeProfile.dataProfile.itemForm['view'] === 'Телефон') {
    return 'tel';

  } else if (storeProfile.dataProfile.itemForm['view'] === 'E-mail') {
    return 'email';

  } else {
    return 'text';
  }
});

</script>

<template>
  <form @submit.prevent="storeProfile.updateItem" class="form form-check" role="form">
    <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="view">Выбрать</label>
      <div class="col-lg-10">
        <select class="form-select" id="view" name="view" 
                v-model="storeProfile.dataProfile.itemForm['view']">
          <option value="Телефон">Телефон</option>
          <option value="E-mail">E-mail</option>
          <option value="Другое">Другое</option>
        </select>
      </div>
    </div>
    <div class="mb-3 row required">
      <label class="col-form-label col-lg-2" for="contact">Контакт</label>
      <div class="col-lg-10">
        <input class="form-control" id="contact" maxlength="250" name="contact" 
              required :type="view" v-model="storeProfile.dataProfile.itemForm['contact']">
      </div>
    </div>
    <div class=" row">
      <div class="offset-lg-2 col-lg-10">
        <button class="btn btn-outline-primary btn-md" name="submit" type="submit">Принять</button>
      </div>
    </div>
  </form>
</template>