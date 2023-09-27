<script setup lang="ts">

import { onBeforeMount } from 'vue';
import { storeContact } from '@/store/contacts';
import ConnectForm from '@content/forms/ConnectForm.vue';

const contactStore = storeContact();

onBeforeMount(() => {
  contactStore.getContacts()
});

</script>

<template>
  <div class="container py-3">
    <div class="py-3">
      <h4>Контакты</h4>
    </div>
    <form @input="contactStore.searchContacts" class="form form-check" role="form">
      <div class="row py-3">
        <input class="form-control" id="name" name="name" placeholder="Поиск контактов" type="text" v-model="contactStore.searchData">
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
              <a role="button" @click="contactStore.itemAction === 'create' 
                                      ? contactStore.itemAction = '' 
                                      : contactStore.itemAction = 'create'" 
                               :title="contactStore.itemAction === 'create' 
                                      ? 'Отмена' : 'Добавить контакт'">
                <i :class="contactStore.itemAction === 'create' 
                          ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"></i>
              </a>
            </th>
            <th width="5%"></th>
          </tr>
        </thead>
        <tbody v-if="contactStore.data.contacts">
          <tr v-if="contactStore.itemAction === 'create'">
            <td colspan="9"><ConnectForm/></td>
          </tr>
          <tr>
            <td colspan="9">
              <table v-for="contact in contactStore.data.contacts" :key="contact['id']" 
                  class="table table-responsive table-hover align-middle">
                <tbody>
                  <tr v-if="contactStore.itemId !== contact['id']">
                    <td width="5%">{{ contact["id"] }}</td>
                    <td width="15%">{{ contact["company"] }}</td>
                    <td width="15%">{{ contact["city"] }}</td>
                    <td width="15%">{{ contact["fullname"] }}</td>
                    <td width="15%">{{ contact["contact"] }}</td>
                    <td width="15%">{{ contact["comment"] }}</td>
                    <td width="10%">{{ contact["data"] }}</td>
                    <td width="5%">
                      <a class="btn btn-link" title="Изменить"
                          @click="contactStore.itemAction='edit'; 
                                  contactStore.itemId=contact['id'];
                                  contactStore.itemForm=contact">
                        <i class="bi bi-pencil-square"></i>
                      </a>
                    </td>
                    <td width="5%">
                      <a href="#" @click="contactStore.deleteContact($event, contact['id'])" 
                          title="Удалить">
                        <i class="bi bi-trash"></i>
                      </a>
                    </td>
                  </tr>
                  <tr v-if="contactStore.itemAction === 'edit' 
                      && contactStore.itemId === contact['id']" >
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
      <nav v-if="contactStore.data.hasPrev || contactStore.data.hasNext">
        <ul class="pagination justify-content-center">
          <li v-bind:class="{ 'page-item': true, disabled: !contactStore.data.hasPrev }">
            <a class="page-link" href="#" v-on:click.prevent="contactStore.prevPage">
                Предыдущая</a>
          </li>
          <li v-bind:class="{ 'page-item': true, disabled: !contactStore.data.hasNext }">
            <a class="page-link" href="#" v-on:click.prevent="contactStore.nextPage">
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