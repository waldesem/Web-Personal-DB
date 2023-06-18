<template>
  <NavBar />
  <div class="container py-5">
    <div class="py-5"><h3>{{ head }}</h3></div>
    <div class="py-1">
      <form @submit.prevent="getCandidates('search')" class="form form-check" role="form">
        <div class="row">
          <div class="col-md-2">
            <div class="mb-3">
              <label class="visually-hidden" for="region">Region</label>
              <input autocomplete="on" class="form-control mb-2 mr-sm-2 mb-sm-0" id="region" maxlength="25" minlength="2" v-model="region" name="region" placeholder="поиск по региону" type="text">
            </div>
          </div>
          <div class="col-md-4">
            <div class="mb-3">
              <label class="visually-hidden" for="fullname">Fullname</label>
              <input class="form-control mb-2 mr-sm-2 mb-sm-0" id="fullname" maxlength="250" minlength="3" v-model="fullname" name="fullname" placeholder="поиск по ФИО" type="text">
            </div>
          </div>
          <div class="col-md-2">
            <div class="mb-3">
              <label class="visually-hidden" for="birthday">Birthday</label>
              <input class="form-control mb-2 mr-sm-2 mb-sm-0" id="birthday" v-model="birthday" name="birthday" placeholder="по дате рождения" type="date">
            </div>
          </div>
          <div class="col-md-2">
            <div class="mb-3">
              <label class="visually-hidden" for="status">Status</label>
              <select class="form-select mb-2 mr-sm-2 mb-sm-0" v-model="status" name="status">
                <option value="">По региону</option>
                <option value="Новый">Новый</option>
                <option value="Обновлен">Обновлен</option>
                <option value="Проверка">Проверка</option>
                <option value="Сохранено">Сохранено</option>
                <option value="Автомат">Автомат</option>
                <option value="Робот">Робот</option>
                <option value="Обработано">Обработано</option>
                <option value="ПФО">ПФО</option>
                <option value="Результат">Результат</option>
                <option value="Ошибка">Ошибка</option>
              </select>
            </div>
          </div>
          <div class="col-md-2">
            <button class="btn btn-primary btn-md" type="submit">Найти</button>
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
          <tr height="50px" v-for="candidate in candidates" :key="candidate">
            <td>{{ candidate["id" as keyof typeof candidate] }}</td>
            <td>{{ candidate["region" as keyof typeof candidate] }}</td>
            <td>
              <router-link :to="{ name: 'profile', params: {
                id: candidate['id' as keyof typeof candidate]
                } }">{{ candidate["fullname" as keyof typeof candidate] }}
              </router-link>
            </td>
            <td>{{ convertDate(candidate["birthday" as keyof typeof candidate]) }}</td>
            <td>{{ candidate["status" as keyof typeof candidate] }}</td>
            <td>{{ convertDate(candidate["deadline" as keyof typeof candidate]) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="py-3">
      <nav v-if="hasPagination">
        <ul class="pagination justify-content-center">
          <li v-bind:class="{ 'page-item': true, disabled: !hasPrev }">
            <a class="page-link" href="#" v-on:click.prevent="prevPage">Предыдущая</a>
          </li>
          <li v-bind:class="{ 'page-item': true, disabled: !hasNext }">
            <a class="page-link" href="#" v-on:click.prevent="nextPage">Следующая</a>
          </li>
        </ul>
      </nav>
    </div>
  </div>
  <div>
    <footer class="d-flex flex-wrap justify-content-around align-items-center py-3 my-4 border-top">
      <p><a href="/docs">OpenAPI</a></p>
      <p><a href="/admin">Admin</a></p>
      <p><a href="https://github.com/waldesem/Web-Personal-DB">GitHub</a></p>
    </footer>
  </div>
</template>

<script setup lang="ts">

import { ref, watch } from 'vue'
import { useRoute } from 'vue-router' 
import axios from 'axios';
import NavBar from './NavBar.vue';

const route = useRoute();
const head = ref('Новые кандидаты');
const path = ref(String(route.params.flag));
const region = ref('');
const fullname = ref('');
const birthday = ref('');
const status = ref('');
const candidates = ref([]);
const currentPage = ref(1);
const currentPath = ref('');
const hasPagination = ref(false);
const hasPrev = ref(false);
const hasNext = ref(false);

getCandidates(path.value);
    
async function getCandidates(url: string, page=1) {
  currentPage.value = page;
  currentPath.value = url;
  const header = {
    'search': "Результаты поиска", 
    'officer': "Страница пользователя", 
    'main': "Главная страница",
    'new': "Новые кандидаты"
  }
  head.value = header[url as keyof typeof header]
  let response
  try {
    if (url !== 'search') {
      response = await axios.get(`http://localhost:5000/index/${url}/${page}`, {
        headers: {'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`}
      })
    } else {
      response = await axios.post(`http://localhost:5000/index/${url}/${page}`, 
      {
        "region": region.value, 
        "fullname": fullname.value, 
        "birthday": birthday.value, 
        "status": status.value
      }, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`,
          'Content-Type': 'application/json'
        }
      })
    }
    const [ data, metadata ] = response.data;
    candidates.value = data;
    hasPagination.value = hasNext.value || hasPrev.value;
    hasPrev.value = metadata.has_prev;
    hasNext.value = metadata.has_next;
  } catch (error) {
    console.error(error);
  }
}

function convertDate(value: string): string {
  const date = new Date(Date.parse(value));
  const day = date.getDate().toString().padStart(2, '0');
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const year = date.getFullYear().toString();
  return `${day}.${month}.${year}`;
}

async function prevPage() {
  if (hasPrev.value) {
    currentPage.value -= 1;
    await getCandidates(currentPath.value, currentPage.value);
  }
}

async function nextPage() {
  if (hasNext.value) {
    currentPage.value += 1;
    await getCandidates(currentPath.value, currentPage.value);
  }
}

watch(
  () => route.params.flag,
  (newVal) => {
    path.value = String(newVal);
    getCandidates(path.value);
  }
);


</script>
