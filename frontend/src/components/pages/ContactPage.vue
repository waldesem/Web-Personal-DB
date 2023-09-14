<script setup lang="ts">

import { onBeforeMount } from 'vue';
import { storeContact } from '@/store/contacts';

const contactStore = storeContact();

onBeforeMount(() => {
  contactStore.getContacts()
});
</script>

<template>
  <div class="container py-5">
    <div class="py-5"><h4>Контакты</h4></div>
    <form @change="contactStore.getContacts('search')" class="form form-check" role="form">
      <div class="row py-3">
        <input class="form-control" id="name" maxlength="255" minlength="2" name="name" placeholder="Название организации" type="text" v-model="contactStore.searchData">
      </div>
    </form>
    <div class="py-3">
      <table class="table table-hover table-responsive align-middle">
        <thead> 
          <tr>
            <th width="5%">#</th>
            <th width="15%">Компания</th>
            <th width="15%">Город</th>
            <th width="15%">Имя</th>
            <th width="15%">Контакт</th>
            <th width="15%">Примечение</th>
            <th width="10%">Дата</th>
            <th></th>
            <th>
              <a role="button" title="Добавить контакт" @click="contactStore.itemAction='create'; contactStore.itemId='0'">
                <i class="bi bi-plus-circle"></i>
              </a>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="contactStore.itemAction === 'create' || contactStore.itemAction === 'edit'">
            <td colspan="9">
              <form @submit.prevent="contactStore.updateItem" class="form form-check">
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
                    <p>{{ new Date().toLocaleDateString('ru-RU') }}</p>
                  </div>
                  <div class="col-md-1">
                    <button class="btn btn-outline-primary btn-sm" type="submit">Добавить</button>
                  </div>
                </div>
              </form>
            </td>
          </tr>
          <tr v-for="contact in contactStore.data.contacts" :key="contact['id']">
            <td>{{ contact["id"] }}</td>
            <td>{{ contact["company"] }}</td>
            <td>{{ contact["city"] }}</td>
            <td>{{ contact["fullname"] }}</td>
            <td>{{ contact["contact"] }}</td>
            <td>{{ contact["comment"] }}</td>
            <td>{{ contact["data"] }}</td>
            <td>
              <a class="btn btn-link" data-bs-toggle="tooltip" data-bs-placement="right" title="Изменить"
                        @click="contactStore.itemAction='edit'; 
                                contactStore.itemId=contact['id'];
                                contactStore.itemForm=contact">
                <i class="bi bi-pencil-square"></i>
              </a>
            </td>
            <td>
              <a href="#" @click="contactStore.updateItem($event, 'delete', contact['id'])"
                            data-bs-toggle="tooltip" data-bs-placement="right" title="Удалить">
                <i class="bi bi-trash"></i>
              </a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="py-3">
      <nav v-if="contactStore.data.hasPrev || contactStore.data.hasNext">
        <ul class="pagination justify-content-center">
          <li v-bind:class="{ 'page-item': true, disabled: !contactStore.data.hasPrev }">
            <a class="page-link" href="#" v-on:click.prevent="contactStore.prevPage">Предыдущая</a>
          </li>
          <li v-bind:class="{ 'page-item': true, disabled: !contactStore.data.hasNext }">
            <a class="page-link" href="#" v-on:click.prevent="contactStore.nextPage">Следующая</a>
          </li>
        </ul>
      </nav>
    </div>
  </div>
</template>