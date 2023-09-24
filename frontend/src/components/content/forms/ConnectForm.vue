<script setup lang="ts">

import { storeContact } from '@/store/contacts';

const contactStore = storeContact();

</script>

<template>
  <form @submit.prevent="contactStore.updateContact" class="form form-check">
    <div class="row">
      <div class="col-md-2">
        <input class="form-control form-control-sm" list="companies" id="company" maxlength="250" name="company" placeholder="Название" type="text" v-model="contactStore.itemForm['company']" required>
        <datalist id="companies">
          <option v-for="company in contactStore.data.companies" :value="company"></option>
        </datalist>
      </div>
      <div class="col-md-2">
        <input class="form-control form-control-sm" id="city" list="cities" maxlength="255" name="city" placeholder="Город" type="text" v-model="contactStore.itemForm['city']" required>
        <datalist id="cities">
          <option v-for="city in contactStore.data.cities" :value="city"></option>
        </datalist>
      </div>
      <div class="col-md-2">
        <input class="form-control form-control-sm" id="fullname" maxlength="250" name="fullname" placeholder="Имя" type="text" v-model="contactStore.itemForm['fullname']" required>
      </div>
      <div class="col-md-2">
        <input class="form-control form-control-sm" id="contact" maxlength="250" name="contact" placeholder="Контакт" type="text" v-model="contactStore.itemForm['contact']" required>
      </div>
      <div class="col-md-2">
        <input class="form-control form-control-sm" id="comment" maxlength="250" name="comment" placeholder="Комментарий" type="text" v-model="contactStore.itemForm['comment']">
      </div>
      <div class="col-md-1">
        <button class="btn btn-outline-primary btn-sm" type="submit">Принять</button>
      </div>
      <div class="col-md-1">
        <button class="btn btn-outline-primary btn-sm" @click="contactStore.itemAction = '';
                                                                     contactStore.itemId= ''">Отмена
                      </button>
      </div>
    </div>
  </form>
</template>
              
              