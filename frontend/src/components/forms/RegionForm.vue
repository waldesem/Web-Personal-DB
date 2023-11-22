<script setup lang="ts">

import { defineAsyncComponent } from 'vue';
import { classifyStore } from '@/store/classify';
import { profileStore } from '@/store/profile';

const ModalWin = defineAsyncComponent(() => import('@components/layouts/ModalWin.vue'));

const storeClassify = classifyStore();

const storeProfile = profileStore();

</script>

<template>
  <ModalWin :id="'modalRegion'" :title ="'Изменить регион'" :size="'modal-md'">
    <form @submit.prevent="storeProfile.dataProfile.updateItem" class="form form-check" role="form">
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="region_id" >Регион</label>
        <div class="col-lg-10">
          <select class="form-select" required id="region_id" name="region_id" 
                  v-model="storeProfile.dataProfile.form['region_id']">
            <option v-for="name, value in storeClassify.classData.regions" 
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
  </ModalWin>
</template>

<style>
  html,
  body {
      scrollbar-gutter: stable;
  }
</style>