<script setup lang="ts">

import { ref } from 'vue';
import { appClassify } from '@store/classify';
import { locationStore } from '@store/location';
import { appAuth } from '@store/auth';
import server from '@store/server';
import ModalWin from './ModalWin.vue';
import ResumeForm from './ResumeForm.vue';

const emit = defineEmits(['updateMessage', 'updateItem']);

const storeAuth = appAuth()

const classifyApp = appClassify();

const storeLocation = locationStore();

const flag = ref('');

const props = defineProps({
  resume: Object,
  staffs: Array<Object>,
  docums: Array<Object>,
  addrs: Array<Object>,
  conts: Array<Object>,
  works: Array<Object>,
  relate: Array<Object>,
  candId: String,
  status: String
});


function updateMessage(alert: Object) {
  emit('updateMessage', alert)
};


function updateItem(resp_id: string) {
  emit('updateItem', resp_id);
};


async function updateStatus() {
  if (confirm("Вы действительно обновить статус?")) {
    const response = await storeAuth.axiosInstance.get(`${server}/anketa/status/${props.candId}`);
    const { message } = response.data;

    updateMessage({
      attr: message == classifyApp.status['update'] 
        ? "alert-success" 
        : "alert-warning",
      text: message == classifyApp.status['update'] 
        ? "Статус обновлен" 
        : "Анкету с текущим статусом обновить нельзя",
    });
    window.scrollTo(0,0)
  }
}


async function sendResume() {
  if (confirm("Вы действительно хотите отправить анкету на проверку?")) {
    
    const response = await storeAuth.axiosInstance.get(`${server}/anketa/probe/${props.candId}`);
    const { message } = response.data;
    emit('updateMessage', {
      attr: message === classifyApp.status['robot'] 
        ? 'alert-info' 
        : 'alert-warning',
      text: message === classifyApp.status['robot'] 
        ? 'Анкета отправлена на проверку' 
        : 'Проверка кандидата уже начата'
    });
    if (message !== classifyApp.status['robot']) return;

    const resp = await storeAuth.axiosInstance.get(`${server}/anketa/send/${props.candId}`);
    const { msg } = resp.data;
    const textMessage = {
      robot: ['Анкета кандидата взята в работу', "alert-success"],
      error: ['Отправка анкеты кандидата не удалась. Попробуйте позднее', "alert-info"],
    };
    updateMessage({
      attr: textMessage[msg as keyof typeof textMessage][1],
      text: textMessage[msg as keyof typeof textMessage][0]
    });
    window.scrollTo(0,0)
  }
}

function defineRegion(id: string) {
  return storeLocation.regionsObject[id]
}

async function deleteItem(id: string, flag: string) {
  if (confirm(`Вы действительно хотите удалить запись?`)) {
    const response = await storeAuth.axiosInstance.delete(`${server}/delete/${flag}/${id}`);
    const status = response.status;
    if (status === 200) {
      updateMessage({
        attr: 'alert-success',
        text: `Запись с ID ${id} из таблицы ${flag} удалена`
      })
      window.scrollTo(0,0);
      updateItem(props.candId as string)
    } else {
      updateMessage({
        attr: 'alert-danger',
        text: 'Возникла ошибка при удалении записи'
      })
    }
  }
};

</script>

<template>

  <template v-if="flag === 'edit'" >
    <ResumeForm :resume="resume" @cancelEdit="flag = ''" @updateMessage="updateMessage" @updateItem="updateItem"/>
  </template>

  <template v-else >
    <ModalWin :candId="props.candId" :path="flag" :regions="storeLocation.regionsObject" @updateItem="updateItem"/>
    <div class="p-2">
      <table v-if="props.resume" class="table table-responsive">
        <thead><tr><th colspan="2">{{ `ID #${props.resume['id']}` }}</th></tr></thead>
        <tbody>
          <tr><td width="25%">Категория</td><td>{{ props.resume['category'] }}</td></tr>
          <tr>
            <td width="25%">Регион</td>
            <td>
              <a href="#" @click="flag = 'location'" data-bs-toggle="modal" data-bs-target="#modalWin">{{ defineRegion(props.resume['region_id'])}}</a>
            </td>
          </tr>
          <tr><td width="25%">Фамилия Имя Отчество</td><td>{{ props.resume['fullname'] }}</td></tr>
          <tr><td width="25%">Изменение имени</td><td>{{ props.resume['previous'] }}</td></tr>
          <tr><td width="25%">Дата рождения</td><td>{{ props.resume['birthday'] }}</td></tr>
          <tr><td width="25%">Место рождения</td><td>{{ props.resume['birthplace'] }}</td></tr>
          <tr><td width="25%">Гражданство</td><td>{{ props.resume['country'] }}</td></tr>
          <tr><td width="25%">СНИЛС</td><td>{{ props.resume['snils'] }}</td></tr>
          <tr><td width="25%">ИНН</td><td>{{ props.resume['inn'] }}</td></tr>
          <tr><td width="25%">Образование</td><td>{{ props.resume['education'] }}</td></tr>
          <tr><td width="25%">Дополнительная информация</td><td>{{ props.resume['addition'] }}</td></tr>
          <tr><td width="25%">Документы</td><td>{{ props.resume['path'] }}</td></tr>
          <tr><td width="25%">Статус</td><td>{{ props.resume['status'] }}</td></tr>
          <tr><td width="25%">Создан</td><td>{{ new Date(String(props.resume['create'])).toLocaleDateString('ru-RU') }}</td>
          </tr>
          <tr><td width="25%">Обновлен</td><td>{{ new Date(String(props.resume['update'])).toLocaleDateString('ru-RU') }}</td>
          </tr>
          <tr><td width="25%">Внешний id</td><td>{{ props.resume['request_id'] }}</td></tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
      
      <button @click="flag = 'staff'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Должность</button>
      <table v-if="props.staffs && props.staffs.length" v-for="tbl in props.staffs" class="table table-responsive">
        <thead>
          <tr>
            <th>{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
            <th><a href="#" class="link-opacity-50" @click="deleteItem(tbl['id' as keyof typeof tbl].toString(), 'staff')">Удалить</a>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr><td width="25%">Должность</td><td>{{ tbl['position' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Департамент</td><td>{{ tbl['department' as keyof typeof tbl] }}</td></tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
      
      <button @click="flag = 'document'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Документы</button>
      <table v-if="props.docums && props.docums.length" v-for="tbl in props.docums" class="table table-responsive">
        <thead><tr><th colspan="2">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th></tr></thead>
        <tbody>
          <tr><td width="25%">Вид документа</td><td>{{ tbl['view' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Серия</td><td>{{ tbl['series' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Номер</td><td>{{ tbl['number' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Кем выдан</td><td>{{ tbl['agency' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Дата выдачи</td><td>{{ new Date(String(tbl['issue' as keyof typeof tbl])).toLocaleDateString('ru-RU') }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
      
      <button @click="flag = 'address'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Адреса</button>
      <table v-if="props.addrs && props.addrs.length" v-for="tbl in props.addrs" class="table table-responsive">
        <thead><tr><th colspan="2">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th></tr></thead>
        <tbody>
          <tr><td width="25%">Тип</td><td>{{ tbl['view' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Регион</td><td>{{ tbl['region' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Адрес</td><td>{{ tbl['address' as keyof typeof tbl] }}</td></tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>

      <button @click="flag = 'contact'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Контакты</button>
      <table v-if="props.conts && props.conts.length" v-for="tbl in props.conts" class="table table-responsive">
        <thead><tr><th colspan="2">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th></tr></thead>
        <tbody>
          <tr><td width="25%">Вид</td><td>{{ tbl['view' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Контакт</td><td>{{ tbl['contact' as keyof typeof tbl] }}</td></tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>

      <button @click="flag = 'workplace'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Работа</button>
      <table v-if="props.works && props.works.length" v-for="tbl in props.works" class="table table-responsive">
        <thead><tr><th colspan="2">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th></tr></thead>
        <tbody>
          <tr><td width="25%">Период</td><td>{{ tbl['period' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Организация</td><td>{{ tbl['workplace' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Адрес</td><td>{{ tbl['address' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Должность</td><td>{{ tbl['position' as keyof typeof tbl] }}</td></tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>

      <button @click="flag = 'relation'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Связи</button>
      <table v-if="props.relate && props.relate.length" v-for="tbl in props.relate" class="table table-responsive">
        <thead><tr><th colspan="2">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th></tr></thead>
        <tbody>
          <tr><td width="25%">Тип связи</td><td>{{ tbl['relation' as keyof typeof tbl] }}</td></tr>
          <tr>
            <td width="25%">Связь</td>
            <td><router-link :to="{ name: 'profile', params: {id: String(tbl['relation_id' as keyof typeof tbl])} }">
              Связь ID #{{ tbl['relation_id' as keyof typeof tbl] }}</router-link></td>
          </tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
    </div>

    <div class="btn-group py-3" role="group">
      <button @click="flag = 'edit'" class="btn btn-outline-primary">Изменить анкету</button>
      
      <button @click="updateStatus" class="btn btn-outline-primary">Обновить статус</button>
      <button @click="sendResume" 
        :disabled="classifyApp.status 
        && (status !== classifyApp.status['new'] 
        && status !== classifyApp.status['update'])" 
        class="btn btn-outline-primary">Отправить на проверку
      </button>
    </div>
  </template>

</template>