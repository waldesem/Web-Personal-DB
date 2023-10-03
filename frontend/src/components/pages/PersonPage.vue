<script setup lang="ts">

import { computed, onBeforeMount } from 'vue';
import { personStore } from '@/store/persons';
import { classifyStore } from '@store/classify';
import router from '@/router/router';

const storePersons = personStore();
const storeClassify = classifyStore();

onBeforeMount(() => {
  storePersons.getCandidates();
})

const header = computed(() => {
  const name = {
    'search': "Результаты поиска", 
    'officer': "Страница пользователя",
    'main': "Главная страница",
    'new': "Новые кандидаты"
  }
  return name[storePersons.personData.currentPath as keyof typeof name]
});

function openLink(cand_id: number){
  router.push({ name: 'profile', params: { group: 'staffsec', id: cand_id }})
};

</script>

<template>
  <div class="container py-3">
    <div class="py-5"><h4>{{ header }}</h4></div>
    <div class="row">
      <div class="col-md-3">
        <form class="form form-check" role="form">
          <label class="visually-hidden" for="action">Действия</label>
          <select class="form-select" id="region" name="region" 
                  v-model="storePersons.personData.currentPath" 
                  @change="storePersons.getCandidates(storePersons.personData.currentPath)">
            <option value="" selected>Выберите действие</option>
            <option value="new">Новые кандидаты</option>
            <option value="main">Все кандидаты</option>
            <option value="officer">Мои анкеты</option>
          </select>
        </form>
      </div>
      <div class="col-md-9">
        <form @input="storePersons.searchPerson('search')" class="form form-check" role="form">
          <div class="row">
            <input class="form-control" id="fullname" maxlength="250" minlength="3" 
                  v-model="storePersons.personData.searchData" 
                  name="fullname" placeholder="поиск по ФИО" type="text">
          </div>
        </form>
      </div>
    </div>
    <div class="py-3">
      <table class="table table-hover table-responsive align-middle">
        <thead> 
          <tr height="50px">
            <th width="5%">#</th>
            <th width="25%">Регион</th>
            <th>Фамилия Имя Отчество</th>
            <th width="15%">Дата рождения</th>
            <th width="10%">Статус</th>
            <th width="10%">Дата</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="candidate in storePersons.personData.candidates" 
              :key="candidate.id" @click="openLink(candidate.id)" 
              data-href='#' height="50px">
            <td>{{ candidate["id"] }}</td>
            <td>{{ storeClassify.regions[candidate.region_id] }}</td>
            <td>{{ candidate.fullname }}</td>
            <td>{{ new Date(candidate.birthday).toLocaleDateString('ru-RU') }}</td>
            <td>{{ candidate.status }}</td>
            <td>{{ new Date(candidate.create).toLocaleDateString('ru-RU') }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="py-3">
      <nav v-if="storePersons.personData.has_prev || storePersons.personData.has_next">
        <ul class="pagination justify-content-center">
          <li v-bind:class="{ 'page-item': true, disabled: !storePersons.personData.has_prev }">
            <a class="page-link" href="#" v-on:click.prevent="storePersons.prevPage">
              Предыдущая
            </a>
          </li>
          <li v-bind:class="{ 'page-item': true, disabled: !storePersons.personData.has_next }">
            <a class="page-link" href="#" v-on:click.prevent="storePersons.nextPage">
              Следующая
            </a>
          </li>
        </ul>
      </nav>
    </div>
  </div>
</template>

<style>
.data-href {
  cursor: pointer;
}
</style>