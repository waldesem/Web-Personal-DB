<script setup lang="ts">

import { computed, onBeforeMount, ref } from 'vue';
import { onBeforeRouteLeave } from 'vue-router';
import { classifyStore } from '@store/classify';
import { authStore } from '@/store/token';
import { profileStore } from '@/store/profile';
import { loginStore } from '@/store/login';
import { debounce, server } from '@share/utilities';
import { Candidate } from '@/share/interfaces';
import HeaderDiv from '@components/layouts/HeaderDiv.vue';

const storeAuth = authStore();
const storeClassify = classifyStore();
const storeProfile = profileStore();
const storeLogin = loginStore();

const personData = ref({
  candidates: <Candidate[]>([]),
  has_prev: false,
  has_next: false,
  searchData: '',
  extendedSearch: false,
  currentPage: 1,
  currentPath: 'new'
});

onBeforeMount(() => {
  getCandidates();
});

onBeforeRouteLeave((_to: any, _from: any, next: () => void) => {
  Object.assign(personData.value, {
    has_prev: false,
    has_next: false,
    searchData: '',
    extendedSearch: false,
    currentPage: 1,
    currentPath: 'new'
  });
  next()
});

const header = computed(() => {
  const name = {
    'search': "Результаты поиска",
    'extended': 'Расширенный поиск',
    'officer': "Страница пользователя",
    'main': "Главная страница",
    'new': "Новые кандидаты"
  }
  return name[personData.value.currentPath as keyof typeof name]
});

/**
 * Retrieves candidates from the specified URL and updates the data store.
 *
 * @param {string} url - The URL to retrieve candidates from.
 * @return {Promise<void>} - A promise that resolves when the candidates are 
 * retrieved and the data store is updated.
 */
async function getCandidates(
    url: string=personData.value.currentPath,
    page: number = personData.value.currentPage
  ): Promise<void> {
  
    personData.value.currentPage = page;
    personData.value.currentPath = url;

  try {
    const response = await storeAuth.axiosInstance.post(
      `${server}/index/${url}/${page}`, 
        {'search': personData.value.searchData}
      );
    const [ datas, metadata ] = response.data;
    
    personData.value.candidates = datas;
    personData.value.has_prev = metadata.has_prev;
    personData.value.has_next = metadata.has_next;

  } catch (error) {
    console.error(error);
  }
};

const searchPerson = debounce(getCandidates, 500);

</script>

<template>
    <HeaderDiv :page-header="header" />
    <div class="row">
      <div class="col-md-3">
        <form class="form form-check" role="form">
          <label class="visually-hidden" for="action">Действия</label>
          <select class="form-select" id="region" name="region" 
                  v-model="personData.currentPath" 
                  @change="personData.searchData = ''; 
                  getCandidates(personData.currentPath, 1)">
            <option value="" selected>Выберите действие</option>
            <option value="new">Новые кандидаты</option>
            <option value="main">Все кандидаты</option>
            <option value="officer">Мои анкеты</option>
          </select>
        </form>
      </div>
      <div class="col-md-8">
        <form @input="searchPerson(personData.extendedSearch ? 'extended' : 'search')" 
              class="form form-check" role="form">
          <div class="row">
            <input class="form-control" id="search" maxlength="250" minlength="3" 
                  v-model="personData.searchData" 
                  name="search" placeholder="поиск по имени и ИНН" type="text">
          </div>
        </form>
      </div>
      <div class="col-md-1" v-show="storeLogin.userData.region_id == '1'" >
        <input class="form-check-input" type="checkbox" id="checkbox" 
               title="Расширенный поиск" style="width: 30px; height: 30px;"
               v-model="personData.extendedSearch" value="search">
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
          <tr v-for="candidate in personData.candidates" 
              :key="candidate.id" height="50px">
            <td>{{ candidate["id"] }}</td>
            <td>{{ storeClassify.classifyItems.regions[candidate.region_id] }}</td>
            <td>
              <router-link 
                :to="{ name: 'profile', params: { group: 'staffsec', id: candidate.id } }" 
                @click="storeProfile.candId = candidate.id.toString()">
                {{ candidate.fullname }}
              </router-link>
            </td>
            <td>{{ new Date(candidate.birthday).toLocaleDateString('ru-RU') }}</td>
            <td>{{ candidate.status }}</td>
            <td>{{ new Date(candidate.create).toLocaleDateString('ru-RU') }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="py-3">
      <nav v-if="personData.has_prev || personData.has_next">
        <ul class="pagination justify-content-center">
          <li v-bind:class="{ 'page-item': true, disabled: !personData.has_prev }">
            <a class="page-link" href="#" 
                v-on:click.prevent="getCandidates(
                  personData.currentPath, personData.currentPage - 1
                  )">
                Предыдущая
            </a>
          </li>
          <li v-bind:class="{ 'page-item': true, disabled: !personData.has_next }">
            <a class="page-link" href="#" 
                v-on:click.prevent="getCandidates(
                  personData.currentPath, personData.currentPage + 1
                  )">
                Следующая
            </a>
          </li>
        </ul>
      </nav>
    </div>

</template>
