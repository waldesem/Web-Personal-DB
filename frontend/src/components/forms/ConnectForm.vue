<script setup lang="ts">

import { contactStore } from '@/store/contacts';

const storeContact = contactStore();

</script>

<template>
  <form @submit.prevent="storeContact.updateContact" class="form form-check">
    <div class="row">
      <div class="col-md-3">
        <input class="form-control form-control-sm" list="companies" id="company" 
               maxlength="250" name="company" placeholder="Название" type="text" 
               v-model="storeContact.itemForm['company']" required>
        <datalist id="companies">
          <option v-for="company in storeContact.responseData.companies" :value="company"></option>
        </datalist>
      </div>
      <div class="col-md-3">
        <input class="form-control form-control-sm" id="city" list="cities" 
               maxlength="255" name="city" placeholder="Город" type="text" 
               v-model="storeContact.itemForm['city']" required>
        <datalist id="cities">
          <option v-for="city in storeContact.responseData.cities" :value="city"></option>
        </datalist>
      </div>
      <div class="col-md-2">
        <input class="form-control form-control-sm" id="fullname" maxlength="255" 
               name="fullname" placeholder="Имя" type="text" 
               v-model="storeContact.itemForm['fullname']" required>
      </div>
      <div class="col-md-2">
        <input class="form-control form-control-sm" id="phone" maxlength="255" 
               name="phone" placeholder="Телефон" type="tel" 
               v-model="storeContact.itemForm['phone']">
      </div>
      <div class="col-md-2">
        <input class="form-control form-control-sm" id="adding" maxlength="255" 
               name="adding" placeholder="Добав." type="tel" 
               v-model="storeContact.itemForm['adding']">
      </div>
    </div>
    <div class="row py-2">
      <div class="col-md-3">
        <input class="form-control form-control-sm" id="mobile" maxlength="255" 
               name="mobile" placeholder="Мобильный" type="tel" 
               v-model="storeContact.itemForm['mobile']">
      </div>
      <div class="col-md-3">
        <input class="form-control form-control-sm" id="mail" maxlength="255" 
               name="mail" placeholder="Почта" type="email" 
               v-model="storeContact.itemForm['mail']">
      </div>
      <div class="col-md-3">
        <input class="form-control form-control-sm" id="comment" maxlength="255" 
               name="comment" placeholder="Комментарий" type="text" 
               v-model="storeContact.itemForm['comment']">
      </div>
      <div class="col-md-1">
        <button class="btn btn-outline-primary btn-sm" type="submit">Принять</button>
      </div>
      <div class="col-md-1">
        <button class="btn btn-outline-primary btn-sm" 
                @click="storeContact.contactsData.itemAction = '';
                        storeContact.contactsData.itemId= ''">
            Отмена
        </button>
      </div>
    </div>
  </form>
</template>
              
              