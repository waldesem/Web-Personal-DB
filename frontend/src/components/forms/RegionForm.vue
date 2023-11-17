<script setup lang="ts">
// компонент для отображения модального окна

import { classifyStore } from '@/store/classify';
import { profileStore } from '@/store/profile';

const ModalWin = () => import('@components/layouts/ModalWin.vue');

const storeClassify = classifyStore();

const storeProfile = profileStore();

</script>

<template>
  <modal-win :id="'modalRegion'" :title ="'Изменить регион'" :size="'modal-md'">
    <template v-slot:body>
      <form @submit.prevent="storeProfile.updateItem" class="form form-check" role="form">
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="region_id" >Регион</label>
          <div class="col-lg-10">
            <select class="form-select" required id="region_id" name="region_id" 
                    v-model="storeProfile.dataProfile.itemForm['region_id']">
              <option v-for="name, value in storeClassify.classifyItems.regions" 
                    :key="value" :value="value">{{name}}</option>                
            </select>
          </div>
        </div>
        <div class=" row">
          <div class="offset-lg-2 col-lg-10">
            <button class="btn btn-primary btn-md" data-bs-dismiss="modal" name="submit" type="submit">
              Принять
            </button>
          </div>
        </div>
      </form>
    </template>
  </modal-win>
</template>

<style>
  html,
  body {
      scrollbar-gutter: stable;
  }
</style>