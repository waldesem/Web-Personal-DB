<script setup lang="ts">

import { contactStore } from '@/store/contacts';
import { alertStore } from '@store/alert';
import { authStore } from '@/store/token';
import { loginStore } from '@store/login';
import { server, clearItem } from '@share/utilities';

const storeAlert = alertStore();
const storeContact = contactStore();
const storeAuth = authStore();
const storeLogin = loginStore();

  /**
   * Updates a contact based on the provided flag and contact ID.
   *
   * @param {Event} _event - The event triggering the update.
   * @param {string} flag - The flag indicating the action to perform (default: "itemAction.value").
   * @param {string} contactId - The ID of the contact to update (default: "itemId.value").
   * @return {Promise<void>} - A promise that resolves when the update is complete.
   */
   async function updateContact(
      event: Event, 
      flag: string=storeContact.contactsData.itemAction, 
      contactId: string=storeContact.contactsData.itemId
    ): Promise<void> {
    
    event.preventDefault();
    try {
      const response = flag === 'create'
        ? await storeAuth.axiosInstance.post(
          `${server}/connect/${storeLogin.pageIdentity}`, storeContact.itemForm
          )
        : await storeAuth.axiosInstance.patch(
          `${server}/connect/${contactId}`, storeContact.itemForm
          );
      const { item_id } = response.data;

      const alert = {
        'create': ['alert-success', `Создан контакт ID ${item_id}`],
        'edit': ['alert-info', `Контакт ID ${item_id} обновлен`]
      };
      storeAlert.setAlert(alert[flag as keyof typeof alert][0], 
                                alert[flag as keyof typeof alert][1]);
      
      storeContact.getContacts();
      storeContact.contactsData.itemAction = '';
      storeContact.contactsData.itemId = '';
      clearItem(storeContact.itemForm);

    } catch (error) {
      console.log(error)
    }
  };

</script>

<template>
  <form @submit.prevent="updateContact" class="form form-check">
    <div class="row">
      <div class="col-md-2">
        <input class="form-control form-control-sm" list="companies" id="company" 
               maxlength="250" name="company" placeholder="Название" type="text" 
               v-model="storeContact.itemForm['company']" required>
        <datalist id="companies">
          <option v-for="company in storeContact.responseData.companies" :value="company"></option>
        </datalist>
      </div>
      <div class="col-md-2">
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
        <input class="form-control form-control-sm" id="contact" maxlength="255" 
               name="contact" placeholder="Контакт" type="text" 
               v-model="storeContact.itemForm['contact']" required>
      </div>
      <div class="col-md-2">
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
              
              