<template>
  <NavBar />
  <div class="container py-5">
    <div class="py-5"><h4>{{ header }}</h4></div>
    <div v-if="data.currentPath != 'officer'">
      <form @submit.prevent="getCandidates('search')" class="form form-check" role="form">
        <div class="row">
          <div class="col-md-7">
            <div class="mb-3">
              <label class="visually-hidden" for="fullname">Fullname</label>
              <input class="form-control mb-2 mr-sm-2 mb-sm-0" id="fullname" maxlength="250" minlength="3" v-model="data.fullname" name="fullname" placeholder="поиск по ФИО" type="text">
            </div>
          </div>
          <div class="col-md-3">
            <div class="mb-3">
              <label class="visually-hidden" for="birthday">Birthday</label>
              <input class="form-control mb-2 mr-sm-2 mb-sm-0" id="birthday" v-model="data.birthday" name="birthday" placeholder="по дате рождения" type="date">
            </div>
          </div>
          <div class="col-md-1">
            <button class="btn btn-outline-primary btn-md" type="submit">Найти</button>
          </div>
          <div class="col-md-1">
            <button @click="getCandidates('main')" class="btn btn-outline-primary btn-md" data-bs-toggle="tooltip" data-bs-placement="top" title="Очистить поиск"><i class="bi bi-trash"></i></button>
          </div>
        </div>
      </form>
    </div>
    <div class="py-3">
      <table class="table table-hover table-responsive align-middle">
        <thead>
          <tr height="50px">
            <th width="10%">#</th>
            <th width="15%">Регион</th>
            <th>Фамилия Имя Отчество</th>
            <th width="15%">Дата рождения</th>
            <th width="15%">Статус</th>
            <th width="15%">Дата</th>
          </tr>
        </thead>
        <tbody>
          <tr height="50px" v-for="candidate in data.candidates" :key="candidate">
            <td>{{ candidate["id" as keyof typeof candidate] }}</td>
            <td>{{ candidate["region" as keyof typeof candidate] }}</td>
            <td>
              <router-link :to="{ name: 'profile', params: {
                id: candidate['id' as keyof typeof candidate]
                } }">{{ candidate["fullname" as keyof typeof candidate] }}
              </router-link>
            </td>
            <td>{{ new Date(candidate["birthday" as keyof typeof candidate]).toLocaleDateString('ru-RU')  }}</td>
            <td>{{ candidate["status" as keyof typeof candidate] }}</td>
            <td>{{ new Date(candidate["create" as keyof typeof candidate]).toLocaleDateString('ru-RU')  }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="py-3">
      <nav v-if="data.hasPrev || data.hasNext">
        <ul class="pagination justify-content-center">
          <li v-bind:class="{ 'page-item': true, disabled: !data.hasPrev }">
            <a class="page-link" href="#" v-on:click.prevent="prevPage">Предыдущая</a>
          </li>
          <li v-bind:class="{ 'page-item': true, disabled: !data.hasNext }">
            <a class="page-link" href="#" v-on:click.prevent="nextPage">Следующая</a>
          </li>
        </ul>
      </nav>
    </div>
  </div>
  <FooterDiv />
</template>

<script setup lang="ts">

import { ref, onBeforeMount, computed, watch } from 'vue';
import { useRoute } from 'vue-router' ;
import axios from 'axios';
import config from '@/config';
import NavBar from './NavBar.vue';
import FooterDiv from './FooterDiv.vue';

const route = useRoute();

const data = ref({
  fullname: '',
  birthday: '',
  candidates: [],
  hasPrev: false,
  hasNext: false,
  currentPage: 1,
  currentPath: String(route.params.flag)
});

async function getCandidates(url: string, page=1) {
  data.value.currentPage = page;
  data.value.currentPath = url;
  let response
  try {
    if (url !== 'search') {
      data.value.fullname = '';
      data.value.birthday = '';
      response = await axios.get(`${config.appUrl}/index/${url}/${page}`, {
        headers: {'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`}
      });
    } else {
      response = await axios.post(`${config.appUrl}/index/search/${page}`, 
      {
        "fullname": data.value.fullname, 
        "birthday": data.value.birthday
      }, {
        headers: {'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`}
      })
    }
    const [ datas, metadata ] = response.data;
    Object.assign(data.value, {
      candidates: datas,
      hasPrev: metadata.has_prev,
      hasNext: metadata.has_next
    })
  } catch (error) {
    console.error(error);
  }
};

async function prevPage() {
  if (data.value.hasPrev) {
    data.value.currentPage -= 1;
    await getCandidates(data.value.currentPath, data.value.currentPage);
  }
};

async function nextPage() {
  if (data.value.hasNext) {
    data.value.currentPage += 1;
    await getCandidates(data.value.currentPath, data.value.currentPage);
  }
};

const header = computed(() => {
  const name = {
    'search': "Результаты поиска", 
    'officer': "Страница пользователя", 
    'main': "Главная страница",
    'new': "Новые кандидаты"
  }
  return name[data.value.currentPath as keyof typeof name]
});

watch(() => route.params.flag,
  (pathURL) => {
    getCandidates(String(pathURL))
  }
);

onBeforeMount(async () => {
  getCandidates(data.value.currentPath)
});

</script>
