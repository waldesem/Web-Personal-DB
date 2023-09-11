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
        <div class="col-md-7">
          <label class="visually-hidden" for="name">name</label>
          <input class="form-control" id="name" maxlength="250" minlength="3" name="name" placeholder="Название организации" type="text" v-model="contactStore.searchData">
        </div>
        <div class="col-md-2">
          <button class="btn btn-outline-primary btn-md" type="submit">Найти</button>
        </div>
        <div class="col-md-2">
          <button class="btn btn-outline-info btn-md" type="button"                 data-bs-toggle="modal" data-bs-target="#winModal">>Добавить</button>
        </div>
      </div>
    </form>
    <div class="py-3">
      <table class="table table-hover table-responsive align-middle">
        <thead> 
          <tr height="50px">
            <th width="15%">#</th>
            <th>Организация</th>
          </tr>
        </thead>
        <tbody>
          <tr height="50px" v-for="contact in contactStore.data.сontacts" :key="contact['id']">
            <td>{{ contact["id"] }}</td>
            <td>
              <router-link :to="{ name: 'contacts', params: { id: contact['id'] } }">{{ contact["name"] }}</router-link>
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