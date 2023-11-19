<script setup lang="ts">

import { onBeforeMount, defineAsyncComponent } from 'vue';
import { onBeforeRouteLeave } from 'vue-router';
import { contactStore } from '@/store/contacts';
import { debounce, clearItem } from '@share/utilities';

const HeaderDiv = defineAsyncComponent(() => import('@components/layouts/HeaderDiv.vue'));
const ConnectForm = defineAsyncComponent(() => import('@components/forms/ConnectForm.vue'));
const PageSwitcher = defineAsyncComponent(() => import('@components/layouts/PageSwitcher.vue'));

const storeContact = contactStore();

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

</script>

<template>
  <div class="container py-3">
    <HeaderDiv :page-header="'Контакты'" />
    <form @input="searchContacts" class="form form-check" role="form">
      <div class="row py-3">
        <input class="form-control" id="search" name="search" type="search"
               placeholder="Поиск по организации, имени, номеру мобильного телефона" 
               v-model="storeContact.contactsData.searchData">
      </div>
    </form>
    <div class="py-3">
      <table class="table align-middle text-center no-bottom-border">
        <thead> 
          <tr>
            <th width="5%">#</th>
            <th width="10%">Компания</th>
            <th width="10%">Город</th>
            <th width="10%">Имя</th>
            <th width="10%">Телефон</th>
            <th width="10%">Добавочный</th>
            <th width="10%">Мобильный</th>
            <th width="10%">E-mail</th>
            <th width="10%">Примечание</th>
            <th width="5%">Дата</th>
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
            <td colspan="12">
              <table v-for="contact in storeContact.responseData.contacts" :key="contact['id']" 
                     class="table table-hover align-middle text-center">
                <tbody>
                  <tr v-if="storeContact.contactsData.itemId !== contact['id']">
                    <td width="5%">{{ contact["id"] }}</td>
                    <td width="10%">{{ contact["company"] }}</td>
                    <td width="10%">{{ contact["city"] }}</td>
                    <td width="10%">{{ contact["fullname"] }}</td>
                    <td width="10%">{{ contact["phone"] }}</td>
                    <td width="10%">{{ contact["adding"] }}</td>
                    <td width="10%">{{ contact["mobile"] }}</td>
                    <td width="10%">{{ contact["mail"] }}</td>
                    <td width="10%">{{ contact["comment"] }}</td>
                    <td width="5%">{{ contact["data"] }}</td>
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
                          @click="storeContact.deleteContact(contact['id'])">
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
    <PageSwitcher :has_prev = "storeContact.responseData.hasNext"
                  :has_next = "storeContact.responseData.hasPrev"
                  :switchPrev = "storeContact.contactsData.currentPage -1"
                  :switchNext = "storeContact.contactsData.currentPage +1"
                  :switchPage = "storeContact.getContacts" />
  </div>
</template>

<style scoped>
.no-bottom-border td {
  border-bottom: none;
}
</style>
