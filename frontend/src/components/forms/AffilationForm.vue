<script setup lang="ts">
 
import { profileStore } from '@/store/profile';

const storeProfile = profileStore();


</script>

<template>
  <form @submit.prevent="storeProfile.updateItem" class="form form-check" role="form">
    <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="view" >Тип участия</label>
      <div class="col-lg-10">
        <select class="form-select" required id="view" name="view" 
                v-model="storeProfile.dataProfile.itemForm['view']">
          <option value="Являлся государственным/муниципальным служащим">
            Являлся государственным или муниципальным служащим
          </option>
          <option value="Являлся государственным/муниципальным служащим">
            Являлся государственным должностным лицом
          </option>
          <option value="Связанные лица работают в госудраственных организациях">
            Связанные лица работают в госудраственных организациях
          </option>
          <option value="Участвует в деятельности коммерческих организаций">
            Участвует в деятельности коммерческих организаций"
          </option>
        </select>
      </div>
    </div>
    <div class="mb-3 row required">
      <label class="col-form-label col-lg-2" for="position">Организация</label>
      <div class="col-lg-10">
        <input class="form-control" id="name" name="name" required type="text"  
              v-model="storeProfile.dataProfile.itemForm['name']">
      </div>
    </div>
    <div class="mb-3 row required">
      <label class="col-form-label col-lg-2" for="position">Позиция</label>
      <div class="col-lg-10">
        <input class="form-control" id="position" name="position"  type="text"  
              v-model="storeProfile.dataProfile.itemForm['position']">
      </div>
    </div>
    <div class="mb-3 row required">
      <label class="col-form-label col-lg-2" for="inn">ИНН</label>
      <div class="col-lg-10">
        <input class="form-control" id="inn" maxlength="12" name="inn" type="text" 
              v-model="storeProfile.dataProfile.itemForm['inn']">
      </div>
    </div>
    <div class=" row">
      <div class="offset-lg-2 col-lg-10">
        <button class="btn btn-outline-primary btn-md" name="submit" type="submit">Принять</button>
      </div>
    </div>
  </form>
</template>
