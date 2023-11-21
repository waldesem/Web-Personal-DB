<script setup lang="ts">

import { computed, defineAsyncComponent, onBeforeMount, ref } from 'vue';
import { onBeforeRouteLeave } from 'vue-router';
import { classifyStore } from '@store/classify';
import { authStore } from '@/store/token';
import { debounce, server } from '@utilities/utils';

const HeaderDiv = defineAsyncComponent(() => import('@components/layouts/HeaderDiv.vue'));
const PageSwitcher = defineAsyncComponent(() => import('@components/layouts/PageSwitcher.vue'));

const storeAuth = authStore();
const storeClassify = classifyStore();

const header = computed(() => {
  const name = {
    'search': "Результаты поиска",
    'extended': 'Расширенный поиск',
    'officer': "Страница пользователя",
    'main': "Главная страница",
    'new': "Новые кандидаты"
  }
  return name[personData.value.path as keyof typeof name]
});

interface Candidate {
  id: number;
  fullname: string;
  region_id: number;
  birthday: string;
  status: string;
  create: string;
};

const personData = ref({
  candidates: <Candidate[]>([]),
  prev: false,
  next: false,
  search: '',
  extsearch: false,
  page: 1,
  path: 'new',
  getCandidates: async function (page: number, url: string): Promise<void> {
    this.page = page;
    this.path = url;
    try {
      const response = await storeAuth.axiosInstance.post(
        `${server}/index/${url}/${page}`, {'search': this.search}
      );
      const [ datas, metadata ] = response.data;
      this.candidates = datas;
      this.prev = metadata.has_prev;
      this.next = metadata.has_next;
    } catch (error) {
      console.error(error);
    }
  }
});

onBeforeMount(() => {
  personData.value.getCandidates(personData.value.page, personData.value.path );
});

onBeforeRouteLeave((_to: any, _from: any, next: () => void) => {
  Object.assign(personData.value, {
    candidates: [],
    prev: false,
    next: false,
    search: '',
    extsearch: false,
    page: 1,
    path: 'new'
  });
  next()
});

const searchPerson = debounce(personData.value.getCandidates, 500);

</script>

<template>
  <div class="container py-3">
    <HeaderDiv :page-header="header" />
    <div class="row">
      <div class="col-md-3">
        <form class="form form-check" role="form">
          <label class="visually-hidden" for="action">Действия</label>
          <select class="form-select" id="region" name="region" 
                  v-model="personData.path" 
                  @change="personData.search = ''; 
                  personData.getCandidates(1, personData.path)">
            <option value="" selected>Выберите действие</option>
            <option value="new">Новые кандидаты</option>
            <option value="main">Все кандидаты</option>
            <option value="officer">Мои анкеты</option>
          </select>
        </form>
      </div>
      <div class="col-md-8">
        <form @input="searchPerson(1, personData.extsearch ? 'extended' : 'search')" 
              class="form form-check" role="form">
          <div class="row">
            <input class="form-control" id="search" maxlength="250" minlength="3" 
                  v-model="personData.search" 
                  name="search" placeholder="поиск по имени и ИНН" type="text">
          </div>
        </form>
      </div>
      <div class="col-md-1">
        <input class="form-check-input" type="checkbox" id="checkbox" 
               title="Расширенный поиск" style="width: 30px; height: 30px;"
               v-model="personData.extsearch" value="search">
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
            <td>{{ storeClassify.classData.regions[candidate.region_id] }}</td>
            <td>
              <router-link 
                :to="{ name: 'profile', params: { group: 'staffsec', id: candidate.id } }">
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
    <PageSwitcher :has_prev = "personData.prev"
                  :has_next = "personData.next"
                  :switchPrev = "personData.page-1"
                  :switchNext = "personData.page+1"
                  :option = "personData.path, "
                  :switchPage="personData.getCandidates" />
  </div>
</template>
