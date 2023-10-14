<script setup lang="ts">

import { onBeforeMount } from 'vue';
import { onBeforeRouteLeave } from 'vue-router';
import { contactStore } from '@/store/contacts';
import { alertStore } from '@store/alert';
import { authStore } from '@/store/token';
import { server, debounce, clearItem } from '@share/utilities';
import ConnectForm from '@components/forms/ConnectForm.vue';

const storeAlert = alertStore();
const storeContact = contactStore();
const storeAuth = authStore();

const searchContacts = debounce(storeContact.getContacts, 500);

onBeforeMount(() => {
  storeContact.getContacts()
});

onBeforeRouteLeave((_to: any, _from: any, next: () => void) => {
  Object.assign(storeContact.contactsData, {
    itemAction: '',
    itemId: '',
    searchData: '',
    currentPage: 1
  })
  clearItem(storeContact.itemForm);
  next()
});

/**
 * Deletes a contact.
 *
 * @param {string} contactId - the ID of the contact to delete
 * @return {Promise<void>} a Promise that resolves when the contact is deleted
 */
async function deleteContact(contactId: string=storeContact.contactsData.itemId): Promise<void> {
  if (confirm("Вы действительно хотите удалить контакт?")) {
    try {
      const response = await storeAuth.axiosInstance.delete(`${server}/connect/${contactId}`);
      console.log(response.status);
      storeAlert.setAlert('alert-success', `Контакт с ID ${contactId} удален`);
      storeContact.contactsData.currentPage = 1; // reset page
      storeContact.getContacts();

    } catch (error) {
      console.log(error)
      
      storeAlert.setAlert('alert-danger', `Ошибка при удалении контакта с ID ${contactId}`);
    }
  }
};

</script>

<template>
  <div class="container py-3">
    <div class="py-5">
      <h4>Контакты</h4>
    </div>
    <form @input="searchContacts" class="form form-check" role="form">
      <div class="row py-3">
        <input class="form-control" id="company" name="company" type="text"
               placeholder="Поиск контактов" v-model="storeContact.contactsData.searchData">
      </div>
    </form>
    <div class="py-3">
      <table class="table table-responsive align-middle no-bottom-border">
        <thead> 
          <tr>
            <th width="5%">#</th>
            <th width="15%">Компания</th>
            <th width="15%">Город</th>
            <th width="15%">Имя</th>
            <th width="15%">Контакт</th>
            <th width="15%">Примечание</th>
            <th width="10%">Дата</th>
            <th width="5%">
              <a role="button" @click="storeContact.contactsData.itemAction === 'create' 
                                      ? storeContact.contactsData.itemAction = '' 
                                      : storeContact.contactsData.itemAction = 'create'" 
                               :title="storeContact.contactsData.itemAction === 'create' 
                                      ? 'Отмена' : 'Добавить контакт'">
                <i :class="storeContact.contactsData.itemAction === 'create' 
                          ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"></i>
              </a>
            </th>
            <th width="5%"></th>
          </tr>
        </thead>
        <tbody v-if="storeContact.responseData.contacts">
          <tr v-if="storeContact.contactsData.itemAction === 'create'">
            <td colspan="9"><ConnectForm/></td>
          </tr>
          <tr>
            <td colspan="9">
              <table v-for="contact in storeContact.responseData.contacts" :key="contact['id']" 
                  class="table table-responsive table-hover align-middle">
                <tbody>
                  <tr v-if="storeContact.contactsData.itemId !== contact['id']">
                    <td width="5%">{{ contact["id"] }}</td>
                    <td width="15%">{{ contact["company"] }}</td>
                    <td width="15%">{{ contact["city"] }}</td>
                    <td width="15%">{{ contact["fullname"] }}</td>
                    <td width="15%">{{ contact["contact"] }}</td>
                    <td width="15%">{{ contact["comment"] }}</td>
                    <td width="10%">{{ contact["data"] }}</td>
                    <td width="5%">
                      <a class="btn btn-link" title="Изменить"
                          @click="storeContact.contactsData.itemAction='edit'; 
                                  storeContact.contactsData.itemId=contact['id'];
                                  storeContact.itemForm=contact">
                        <i class="bi bi-pencil-square"></i>
                      </a>
                    </td>
                    <td width="5%">
                      <a href="#" title="Удалить" 
                          @click="deleteContact(contact['id'])">
                        <i class="bi bi-trash"></i>
                      </a>
                    </td>
                  </tr>
                  <tr v-if="storeContact.contactsData.itemAction === 'edit' 
                      && storeContact.contactsData.itemId === contact['id']" >
                    <td colspan="9"><ConnectForm /></td>
                  </tr>
                </tbody>
              </table>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="py-3">
      <nav v-if="storeContact.responseData.hasPrev || storeContact.responseData.hasNext">
        <ul class="pagination justify-content-center">
          <li v-bind:class="{ 'page-item': true, disabled: !storeContact.responseData.hasPrev }">
            <a class="page-link" href="#" 
              @click.prevent="storeContact.contactsData.currentPage -= 1;
                              storeContact.getContacts">
                Предыдущая</a>
          </li>
          <li v-bind:class="{ 'page-item': true, disabled: !storeContact.responseData.hasNext }">
            <a class="page-link" href="#" 
              @click.prevent="storeContact.contactsData.currentPage += 1;
                              storeContact.getContacts">
                Следующая</a>
          </li>
        </ul>
      </nav>
    </div>
  </div>
</template>

<style scoped>
table td
{
  border-bottom: none;
}
</style>