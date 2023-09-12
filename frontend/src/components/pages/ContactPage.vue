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
      </div>
    </form>
    <div class="py-3">
      <table class="table table-hover table-responsive align-middle">
        <thead> 
          <tr height="50px">
            <th width="5%">#</th>
            <th width="15">Организация</th>
            <th width="15">Город</th>
            <th width="15">Имя</th>
            <th width="15">Контакт</th>
            <th width="15">Комментарий</th>
            <th width="10">Дата</th>
            <th width="5">Дата</th>
            <th width="5">Дата</th>
          </tr>
        </thead>
        <tbody>
          <tr height="50px" v-for="contact in contactStore.data.сontacts" :key="contact['id']">
            <td>{{ contact["id"] }}</td>
            <td>{{ contact["company"] }}</td>
            <td>{{ contact["city"] }}</td>
            <td>{{ contact["fullname"] }}</td>
            <td>{{ contact["contact"] }}</td>
            <td>{{ contact["comment"] }}</td>
            <td>{{ contact["data"] }}</td>
            <td><a class="btn btn-link" data-bs-toggle="tooltip" data-bs-placement="right" title="Изменить">
                  <i class="bi bi-pencil-square"></i>
                </a>
            </td>
            <td><a href="#" @click="contactStore.updateItem('delete', contact['id'])"
                            data-bs-toggle="tooltip" data-bs-placement="right" title="Удалить">
                  <i class="bi bi-trash"></i>
                </a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <button class="btn btn-outline-primary" type="button">Добавить контакт</button>
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