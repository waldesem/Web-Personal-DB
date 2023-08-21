<script setup lang="ts">
// компонент для отображения списка кандидатов для пользователя 
import { computed, onBeforeMount } from 'vue';
import { appLocation } from '@store/location';
import { appLogin } from '@/store/login';
import { appPersons } from '@/store/persons';

const storeLocation = appLocation();

const storeUsers = appLogin();

const storePersons = appPersons();

// Инициализация списка кандидатов
onBeforeMount(async () => {
  storePersons.getCandidates(storePersons.currenData.currentPath);
});

// матчинг заголовков страниц
const header = computed(() => {
  const name = {
    'search': "Результаты поиска", 
    'officer': "Страница пользователя",
    'main': "Главная страница",
    'new': "Новые кандидаты"
  }
  return name[storePersons.currenData.currentPath as keyof typeof name]
});

</script>

<template>
  <div class="container py-3">
    <div class="py-5"><h4>{{ header }}</h4></div>
    <div class="row py-3">
      <div class="col-md-3">
        <form class="form form-check" role="form">
          <label class="visually-hidden" for="action">Действия</label>
          <select class="form-select" id="region" name="region" v-model="storePersons.currenData.currentPath" @change="storePersons.getCandidates(storePersons.currenData.currentPath); storePersons.dropData">
            <option value="" selected>Выберите действие</option>
            <option value="new">Новые кандидаты</option>
            <option value="main">Все кандидаты</option>
            <option value="officer">Мои анкеты</option>
          </select>
        </form>
      </div>
      <div class="col-md-9">
        <form @submit.prevent="storePersons.getCandidates('search')" class="form form-check" role="form">
          <div class="row">
            <div class="col-md-7">
                <label class="visually-hidden" for="fullname">Fullname</label>
                <input class="form-control" id="fullname" maxlength="250" minlength="3" v-model="storePersons.searchData.fullname" name="fullname" placeholder="поиск по ФИО" type="text">
            </div>
            <div class="col-md-3">
                <label class="visually-hidden" for="birthday">Birthday</label>
                <input class="form-control" id="birthday" v-model="storePersons.searchData.birthday" name="birthday" placeholder="по дате рождения" type="date">
            </div>
            <div class="col-md-1">
              <button class="btn btn-outline-primary btn-md" type="submit">Найти</button>
            </div>
          </div>
        </form>
      </div>
    </div>
    <div class="py-3">
      <table class="table table-hover table-responsive align-middle">
        <thead> 
          <tr height="50px">
            <th width="5%">#</th>
            <th width="15%">Регион</th>
            <th>Фамилия Имя Отчество</th>
            <th width="20%">Дата рождения</th>
            <th width="10%">Статус</th>
            <th width="10%">Дата</th>
            <th v-if="storeUsers.userRole === 'admin'" width="10%">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr height="50px" v-for="candidate in storePersons.data.candidates" :key="candidate">
            <td>{{ candidate["id" as keyof typeof candidate] }}</td>
            <td>{{ storeLocation.regionsObject[candidate["region_id" as keyof typeof candidate]] }}</td>
            <td>
              <router-link :to="{ name: 'profile', params: {
                id: candidate['id' as keyof typeof candidate]
                } }">{{ candidate["fullname" as keyof typeof candidate] }}
              </router-link>
            </td>
            <td>{{ new Date(candidate["birthday" as keyof typeof candidate]).toLocaleDateString('ru-RU')  }}</td>
            <td>{{ candidate["status" as keyof typeof candidate] }}</td>
            <td>{{ new Date(candidate["create" as keyof typeof candidate]).toLocaleDateString('ru-RU')  }}</td>
            <td v-if="storeUsers.userRole === 'admin'">
              <a class="link-opacity-50" href="#" @click="storePersons.delPerson(candidate['id' as keyof typeof candidate])">Удалить</a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="py-3">
      <nav v-if="storePersons.data.hasPrev || storePersons.data.hasNext">
        <ul class="pagination justify-content-center">
          <li v-bind:class="{ 'page-item': true, disabled: !storePersons.data.hasPrev }">
            <a class="page-link" href="#" v-on:click.prevent="storePersons.prevPage">Предыдущая</a>
          </li>
          <li v-bind:class="{ 'page-item': true, disabled: !storePersons.data.hasNext }">
            <a class="page-link" href="#" v-on:click.prevent="storePersons.nextPage">Следующая</a>
          </li>
        </ul>
      </nav>
    </div>
  </div>
</template></template>