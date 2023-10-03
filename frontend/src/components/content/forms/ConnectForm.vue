<script setup lang="ts">

import { contactStore } from '@/store/contacts';

const storeContact = contactStore();

</script>

<template>
  <form @submit.prevent="storeContact.updateContact" class="form form-check">
    <div class="row">
      <div class="col-md-2">
        <input class="form-control form-control-sm" list="companies" id="company" maxlength="250" name="company" placeholder="Название" type="text" 
               v-model="storeContact.itemForm['company']" required>
        <datalist id="companies">
          <option v-for="company in storeContact.data.companies" :value="company"></option>
        </datalist>
      </div>
      <div class="col-md-2">
        <input class="form-control form-control-sm" id="city" list="cities" maxlength="255" name="city" placeholder="Город" type="text" 
               v-model="storeContact.itemForm['city']" required>
        <datalist id="cities">
          <option v-for="city in storeContact.data.cities" :value="city"></option>
        </datalist>
      </div>
      <div class="col-md-2">
        <input class="form-control form-control-sm" id="fullname" maxlength="250" name="fullname" placeholder="Имя" type="text" 
               v-model="storeContact.itemForm['fullname']" required>
      </div>
      <div class="col-md-2">
        <input class="form-control form-control-sm" id="contact" maxlength="250" name="contact" placeholder="Контакт" type="text" 
               v-model="storeContact.itemForm['contact']" required>
      </div>
      <div class="col-md-2">
        <input class="form-control form-control-sm" id="comment" maxlength="250" name="comment" placeholder="Комментарий" type="text" 
               v-model="storeContact.itemForm['comment']">
      </div>
      <div class="col-md-1">
        <button class="btn btn-outline-primary btn-sm" type="submit">Принять</button>
      </div>
      <div class="col-md-1">
        <button class="btn btn-outline-primary btn-sm" @click="storeContact.itemAction = '';
                                                               storeContact.itemId= ''">
          Отмена
        </button>
      </div>
    </div>
  </form>
</template>
              
              