<script setup lang="ts">

import { onBeforeMount } from 'vue';
import { storeContact } from '@/store/contacts';

const contactStore = storeContact();

onBeforeMount(() => {
  contactStore.getContacts();
});

</script>

<template>
  <div class="container py-5">
    <div class="py-5"><h4>Контакты</h4></div>
    <form @submit.prevent="contactStore.getContacts('search')" class="form form-check" role="form">
      <div class="row py-3">
        <label class="visually-hidden" for="name">name</label>
        <input class="form-control" id="name" maxlength="250" minlength="3" name="name" placeholder="Название организации" type="text" v-model="contactStore.searchData">
      </div>
    </form>
    <div class="py-3">
      <table class="table table-hover table-responsive align-middle">
        <thead> 
          <tr>
            <th width="5%">#</th>
            <th width="15%">Организация</th>
            <th width="15%">Город</th>
            <th width="15%">Имя</th>
            <th width="15%">Контакт</th>
            <th width="15%">Комментарий</th>
            <th width="10%">Дата</th>
            <th colspan="2">
              <a class="btn btn-link" type="button" title="Добавить контакт"
                            @click="contactStore.itemAction='create'; contactStore.itemId='0'"><i class="bi bi-plus-circle"></i></a>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <form v-if="contactStore.itemAction === 'create'" class="form-control form-control-sm">
              <td colspan="2">
                <input class="form-control" id="company" maxlength="250" name="company" placeholder="Название" type="text" v-model="contactStore.itemForm['company']">
              </td>
              <td>
                <input class="form-control" id="city" maxlength="250" name="city" placeholder="Город" type="text" v-model="contactStore.itemForm['city']">
              </td>
              <td>
                <input class="form-control" id="fullname" maxlength="250" name="fullname" placeholder="Имя" type="text" v-model="contactStore.itemForm['fullname']">
              </td>
              <td>
                <input class="form-control" id="contact" maxlength="250" name="contact" placeholder="Контакт" type="text" v-model="contactStore.itemForm['contact']">
              </td>
              <td colspan="2">
                <input class="form-control" id="comment" maxlength="250" name="comment" placeholder="Комментарий" type="text" v-model="contactStore.itemForm['comment']">
              </td>
              <td colspan="2">
                <button class="btn btn-outline-primary btn-sm" type="button" @click="contactStore.updateItem">Принять</button>
              </td>
            </form>
          </tr>
          <table v-for="contact in contactStore.data.сontacts" :key="contact['id']">
            <tbody>
              <tr v-if="contactStore.itemAction !== 'edit' && contactStore.itemId !== contact['id']">
                <td>{{ contact["id"] }}</td>
                <td>{{ contact["company"] }}</td>
                <td>{{ contact["city"] }}</td>
                <td>{{ contact["fullname"] }}</td>
                <td>{{ contact["contact"] }}</td>
                <td>{{ contact["comment"] }}</td>
                <td>{{ contact["data"] }}</td>
                <td><a class="btn btn-link" data-bs-toggle="tooltip" data-bs-placement="right" title="Изменить"
                            @click="contactStore.itemAction='edit'; 
                                    contactStore.itemId=contact['id'];
                                    contactStore.itemForm=contact">
                      <i class="bi bi-pencil-square"></i>
                    </a>
                </td>
                <td><a href="#" @click="contactStore.updateItem('delete', contact['id'])"
                                data-bs-toggle="tooltip" data-bs-placement="right" title="Удалить">
                      <i class="bi bi-trash"></i>
                    </a>
                </td>
              </tr>
              <tr>
                <form v-if="contactStore.itemAction === 'edit' && contactStore.itemId === contact['id']" class="form-control form-control-sm">
                  <td colspan="2">
                    <input class="form-control" id="company" maxlength="250" name="company" placeholder="Название" type="text" v-model="contactStore.itemForm['company']">
                  </td>
                  <td>
                    <input class="form-control" id="city" maxlength="250" name="city" placeholder="Город" type="text" v-model="contactStore.itemForm['city']">
                  </td>
                  <td>
                    <input class="form-control" id="fullname" maxlength="250" name="fullname" placeholder="Имя" type="text" v-model="contactStore.itemForm['fullname']">
                  </td>
                  <td>
                    <input class="form-control" id="contact" maxlength="250" name="contact" placeholder="Контакт" type="text" v-model="contactStore.itemForm['contact']">
                  </td>
                  <td colspan="2">
                    <input class="form-control" id="comment" maxlength="250" name="comment" placeholder="Комментарий" type="text" v-model="contactStore.itemForm['comment']">
                  </td>
                  <td colspan="2">
                    <button class="btn btn-outline-primary btn-sm" type="button" @click="contactStore.updateItem">Принять</button>
                  </td>
                </form>
              </tr>
            </tbody>
          </table>
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