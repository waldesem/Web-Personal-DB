<script setup lang="ts">

import { ref, onBeforeMount, computed } from 'vue';
import { locationStore } from '@store/location';
import { appAuth } from '@store/auth';
import { appAlert } from '@/store/alert';
import server from '@store/server';


const storeAuth = appAuth()

const store = locationStore();

const storeAlert = appAlert();

const props = defineProps({
  admin: Boolean
});

// Объявление переменных
const data = ref({
  fullname: '',
  birthday: '',
  candidates: [],
  hasPrev: false,
  hasNext: false,
  currentPage: 1,
  currentPath: 'main',
});

// Инициализация списка кандидатов
onBeforeMount(async () => {
  getCandidates(data.value.currentPath);
});

// матчинг заголовков страниц
const header = computed(() => {
  const name = {
    'search': "Результаты поиска", 
    'officer': "Страница пользователя",
    'main': props.admin ? "Список кандидатов" : "Главная страница",
    'new': "Новые кандидаты"
  }
  return name[data.value.currentPath as keyof typeof name]
});


/**
 * Retrieves candidates from the specified URL and updates the data store.
 *
 * @param {string} url - The URL to retrieve candidates from.
 * @param {number} [page=1] - The page number of the candidates to retrieve. Default is 1.
 * @return {Promise<void>} - A promise that resolves when the candidates are retrieved and the data store is updated.
 */
async function getCandidates(url: string, page: number=1): Promise<void> {
  data.value.currentPage = page;
  data.value.currentPath = url;
  let response
  const headers = {
    headers: {'Authorization': `Bearer ${localStorage.getItem('access_token')}`}
  }

  try {
    if (url !== 'search') {
      data.value.fullname = '';
      data.value.birthday = '';
      response = await storeAuth.axiosInstance.get(`${server}/index/${url}/${page}`, headers);
    // Поиск кандидатов
    } else {
      response = await storeAuth.axiosInstance.post(`${server}/index/${url}/${page}`, 
      {
        "fullname": data.value.fullname, 
        "birthday": data.value.birthday
      }, headers)
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

/**
 * Asynchronously moves to the previous page if it exists.
 *
 * @return {undefined} No return value.
 */
//
async function prevPage(): Promise<void> {
  if (data.value.hasPrev) {
    data.value.currentPage -= 1;
    getCandidates(data.value.currentPath, data.value.currentPage);
  }
};


/**
 * Moves to the next page if there is one available.
 *
 * @return {Promise<void>} A promise that resolves when the operation is complete.
 */
async function nextPage(): Promise<void> {
  if (data.value.hasNext) {
    data.value.currentPage += 1;
    getCandidates(data.value.currentPath, data.value.currentPage);
  }
};


/**
 * Deletes a person record.
 *
 * @param {String} id - The ID of the person to delete.
 * @return {Promise} A promise that resolves with the result of the deletion.
 */
async function delPerson(id: String): Promise<any> {
  if (confirm(`Вы действительно хотите удалить анкету?`)) {
    const response = await storeAuth.axiosInstance.get(`${server}/person/delete/${id}`, {
    headers: {'Authorization': `Bearer ${localStorage.getItem('access_token')}`}
  });
    const  { person } = response.data;
    
    storeAlert.alertAttr = 'alert-success';
    storeAlert.alertText = `Анкета ${person} удален`;

    getCandidates(data.value.currentPath);
  }
};


</script>

<template>
  <div class="container py-3">
    <div class="py-5"><h4>{{ header }}</h4></div>
    <div class="row py-3">
      <div class="col-md-3">
        <form class="form form-check" role="form">
          <label class="visually-hidden" for="region">Действия</label>
          <select class="form-select" id="region" name="region" v-model="data.currentPath" @change="getCandidates(data.currentPath)">
            <option value="new" selected>Новые кандидаты</option>
            <option value="main">Все кандидаты</option>
            <option value="officer">Мои анкеты</option>
          </select>
        </form>
      </div>
      <div class="col-md-9">
        <form @submit.prevent="getCandidates('search')" class="form form-check" role="form">
          <div class="row">
            <div class="col-md-7">
                <label class="visually-hidden" for="fullname">Fullname</label>
                <input class="form-control" id="fullname" maxlength="250" minlength="3" v-model="data.fullname" name="fullname" placeholder="поиск по ФИО" type="text">
            </div>
            <div class="col-md-3">
                <label class="visually-hidden" for="birthday">Birthday</label>
                <input class="form-control" id="birthday" v-model="data.birthday" name="birthday" placeholder="по дате рождения" type="date">
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
            <th v-if="admin" width="10%">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr height="50px" v-for="candidate in data.candidates" :key="candidate">
            <td>{{ candidate["id" as keyof typeof candidate] }}</td>
            <td>{{ store.regionsObject[candidate["region_id" as keyof typeof candidate]] }}</td>
            <td v-if="admin">{{ candidate["fullname" as keyof typeof candidate] }}</td>
            <td v-else>
              <router-link :to="{ name: 'profile', params: {
                id: candidate['id' as keyof typeof candidate]
                } }">{{ candidate["fullname" as keyof typeof candidate] }}
              </router-link>
            </td>
            <td>{{ new Date(candidate["birthday" as keyof typeof candidate]).toLocaleDateString('ru-RU')  }}</td>
            <td>{{ candidate["status" as keyof typeof candidate] }}</td>
            <td>{{ new Date(candidate["create" as keyof typeof candidate]).toLocaleDateString('ru-RU')  }}</td>
            <td v-if="admin">
              <a class="link-opacity-50" href="#" @click="delPerson(candidate['id' as keyof typeof candidate])">Удалить</a>
            </td>
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
</template>