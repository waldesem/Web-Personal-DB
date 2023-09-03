<script setup lang="ts">
// компонент для отображения модального окна

import { appClassify } from '@/store/classify';
import { appProfile } from '@/store/profile';

const storeClassify = appClassify();

const storeProfile = appProfile();

</script>

<template>
  <div class="modal fade" id="modalWin" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="modalWinLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="modalWinLabel">Изменить регион</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          
          <form @submit.prevent="storeProfile.updateItem" class="form form-check" role="form">
            <div class="mb-3 row">
              <label class="col-form-label col-lg-2" for="region_id" >Регион</label>
              <div class="col-lg-10">
                <select class="form-select" required id="region_id" name="region_id" v-model="storeProfile.itemForm['region_id']">
                  <option v-for="name, value in storeClassify.regions" :key="value" :value="value">{{name}}</option>                
                </select>
              </div>
            </div>
            <div class=" row">
              <div class="offset-lg-2 col-lg-10">
                <button class="btn btn-primary btn-md" data-bs-dismiss="modal" name="submit" type="submit">Принять</button>
              </div>
            </div>
          </form>
    
        </div>
      </div>
    </div>
  </div>
</template>

<style>
  html,
  body {
      scrollbar-gutter: stable;
  }
</style>