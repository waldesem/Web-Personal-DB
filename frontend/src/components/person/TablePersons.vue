<script setup lang="ts">

import { ref, onBeforeMount, computed } from 'vue';
import { locationStore } from '../../store/location';
import { appAuth } from '../../store/auth';
import server from '../../store/server';


const emit = defineEmits(['updateMessage']);

const storeAuth = appAuth()

const store = locationStore();

const props = defineProps({
  admin: Boolean
});

const data = ref({
  fullname: '',
  birthday: '',
  candidates: [],
  hasPrev: false,
  hasNext: false,
  currentPage: 1,
  currentPath: 'main',
});


onBeforeMount(async () => {
  getCandidates(data.value.currentPath);
});


const header = computed(() => {
  const name = {
    'search': "Результаты поиска", 
    'officer': "Страница пользователя",
    'main': props.admin ? "Список кандидатов" : "Главная страница",
    'new': "Новые кандидаты"
  }
  return name[data.value.currentPath as keyof typeof name]
});

function updateMessage(alert: Object) {
  emit('updateMessage', alert)
};

async function getCandidates(url: string, page=1) {
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


async function delPerson(id: String) {
  if (confirm(`Вы действительно хотите удалить анкету?`)) {
    const response = await storeAuth.axiosInstance.get(`${server}/person/delete/${id}`, {
    headers: {'Authorization': `Bearer ${localStorage.getItem('access_token')}`}
  });
    const  { person } = response.data;
    updateMessage({
      attr: 'alert-success',
      text: `Анкета ${person} удален`
    })
    
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
          <select class="form-select" id="action" name="action" v-model="data.currentPath" @change="getCandidates(data.currentPath)">
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
            <!-- <div class="col-md-1">
              <button class="btn btn-outline-primary btn-md" type="reset" data-bs-toggle="tooltip" data-bs-placement="top" title="Очистить поиск">
                <i class="bi bi-trash"></i>
              </button>
            </div-->
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