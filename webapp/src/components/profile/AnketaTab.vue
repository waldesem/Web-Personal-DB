<script setup lang="ts">

import axios from 'axios';
import { useRoute } from 'vue-router';
import { onBeforeMount, ref, watch } from 'vue';
import ResumeForm from './ResumeForm.vue';
import UploadFile from './UploadFile.vue';
import ModalWin from './ModalWin.vue';
import config from '@/config';
import router from '@/router';


const props = defineProps({
  table: {
    type: Array as () => Array<Array<Object>>,
    required: true
  },
  candId: String,
  resume: Object,
  status: String
});

const route = useRoute();

const emit = defineEmits(['updateMessage', 'updateItem']);

const data = ref({
  flag: '',
  regions: {}
});

const headers = {
  headers: {'Authorization': `Bearer ${localStorage.getItem('access_token')}`}
};


onBeforeMount(async () => {  
  const resp = await axios.get(`${config.appUrl}/region/list`);
  const locations = resp.data;
  data.value.regions = locations.reduce(
    (acc: {[key: number]: string}, obj: {id: number, region: string}) => {
    acc[obj.id] = obj.region;
    return acc;
    }, {}
  );
});


watch(() => route.params.id,
  (newId) => {
    updateItem(String(newId));
    window.scrollTo(0,0)
  }
);


function updateMessage(alert: Object) {
  emit('updateMessage', alert)
};


function updateItem(resp_id: string) {
  emit('updateItem', resp_id);
};


function cancelEdit() {
  props.candId !== '0' 
  ? updateItem(String(props.candId))
  : router.push({ name: 'index', params: { flag: 'new' } })
};


async function updateStatus() {
  if (confirm("Вы действительно обновить статус?")) {
    const response = await axios.get(`${config.appUrl}/anketa/status/${props.candId}`, headers);
    const { message } = response.data;
    console.log(config.status.update)
    updateMessage({
      attr: message == config.status.update ? "alert-success" : "alert-warning",
      text: message == config.status.update ? "Статус обновлен" : "Анкету с текущим статусом обновить нельзя",
    });
    window.scrollTo(0,0)
  }
}


async function sendResume() {
  if (confirm("Вы действительно хотите отправить анкету на проверку?")) {
    
    const response = await axios.get(`${config.appUrl}/anketa/probe/${props.candId}`, headers);
    const { message } = response.data;
    emit('updateMessage', {
      attr: message === config.status.robot ? 'alert-info' : 'alert-warning',
      text: message === config.status.robot ? 'Анкета отправлена на проверку' : 'Проверка кандидата уже начата'
    });
    if (message !== config.status.robot) return;

    const resp = await axios.get(`${config.appUrl}/anketa/send/${props.candId}`, headers);
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

</script>

<template>
  <div class="py-3">
    <template v-if="props.candId==='0'" >
      <UploadFile @updateMessage="updateMessage" @updateItem="updateItem"/>
      <ResumeForm :resume="resume" @cancelEdit="cancelEdit" @updateMessage="updateMessage" @updateItem="updateItem"/>
    </template>
    
    <template v-else >
      <ModalWin :candId="props.candId" :path="data.flag" :regions="data.regions" @updateItem="updateItem"/>
      <div v-if="props.candId !== '0'" class="row">
        <div class="col">
          <div class="text-end">
            <button @click="data.flag = 'location'" type="button" class="btn btn-link" 
                data-bs-toggle="modal" data-bs-target="#modalWin">Изменить регион</button>
          </div>
        </div>
      </div>
      
      <div>
        <h6>Резюме</h6>
        <table v-if="props.table[0] && props.table[0].length" v-for="tbl in props.table[0]" class="table table-responsive">
          <thead><tr><th colspan="2">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th></tr></thead>
          <tbody>
            <tr><td width="25%">Категория</td><td>{{ tbl['category' as keyof typeof tbl] }}</td></tr>
            <tr><td width="25%">Регион</td><td>{{ data.regions[tbl['region_id' as keyof typeof tbl]] }}</td></tr>
            <tr><td width="25%">Фамилия Имя Отчество</td><td>{{ tbl['fullname' as keyof typeof tbl] }}</td></tr>
            <tr><td width="25%">Изменение имени</td><td>{{ tbl['previous' as keyof typeof tbl] }}</td></tr>
            <tr><td width="25%">Дата рождения</td><td>{{ tbl['birthday' as keyof typeof tbl] }}</td></tr>
            <tr><td width="25%">Место рождения</td><td>{{ tbl['birthplace' as keyof typeof tbl] }}</td></tr>
            <tr><td width="25%">Гражданство</td><td>{{ tbl['country' as keyof typeof tbl] }}</td></tr>
            <tr><td width="25%">СНИЛС</td><td>{{ tbl['snils' as keyof typeof tbl] }}</td></tr>
            <tr><td width="25%">ИНН</td><td>{{ tbl['inn' as keyof typeof tbl] }}</td></tr>
            <tr><td width="25%">Образование</td><td>{{ tbl['education' as keyof typeof tbl] }}</td></tr>
            <tr><td width="25%">Дополнительная информация</td><td>{{ tbl['addition' as keyof typeof tbl] }}</td></tr>
            <tr><td width="25%">Документы</td><td><a :href="String(tbl['path' as keyof typeof tbl])">Открыть</a></td></tr>
            <tr style="display:none;"><td width="25%">Фото</td><td>{{ tbl['photo_path' as keyof typeof tbl] }}</td></tr>
            <tr><td width="25%">Статус</td><td>{{ tbl['status' as keyof typeof tbl] }}</td></tr>
            <tr><td width="25%">Создан</td><td>{{ new Date(String(tbl['create' as keyof typeof tbl])).toLocaleDateString('ru-RU') }}</td>
            </tr>
            <tr><td width="25%">Обновлен</td><td>{{ new Date(String(tbl['update' as keyof typeof tbl])).toLocaleDateString('ru-RU') }}</td>
            </tr>
            <tr><td width="25%">Внешний id</td><td>{{ tbl['request_id' as keyof typeof tbl] }}</td></tr>
          </tbody>
        </table>
        <p v-else >Данные отсутствуют</p>
        
        <button @click="data.flag = 'staff'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Должность</button>
        <table v-if="props.table[1] && props.table[1].length" v-for="tbl in props.table[1]" class="table table-responsive">
          <thead><tr><th colspan="2">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th></tr></thead>
          <tbody>
            <tr><td width="25%">Должность</td><td>{{ tbl['position' as keyof typeof tbl] }}</td></tr>
            <tr><td width="25%">Департамент</td><td>{{ tbl['department' as keyof typeof tbl] }}</td></tr>
          </tbody>
        </table>
        <p v-else >Данные отсутствуют</p>
        
        <button @click="data.flag = 'document'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Документы</button>
        <table v-if="props.table[2] && props.table[2].length" v-for="tbl in props.table[2]" class="table table-responsive">
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
        
        <button @click="data.flag = 'address'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Адреса</button>
        <table v-if="props.table[3] && props.table[3].length" v-for="tbl in props.table[3]" class="table table-responsive">
          <thead><tr><th colspan="2">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th></tr></thead>
          <tbody>
            <tr><td width="25%">Тип</td><td>{{ tbl['view' as keyof typeof tbl] }}</td></tr>
            <tr><td width="25%">Регион</td><td>{{ tbl['region' as keyof typeof tbl] }}</td></tr>
            <tr><td width="25%">Адрес</td><td>{{ tbl['address' as keyof typeof tbl] }}</td></tr>
          </tbody>
        </table>
        <p v-else >Данные отсутствуют</p>

        <button @click="data.flag = 'contact'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Контакты</button>
        <table v-if="props.table[4] && props.table[4].length" v-for="tbl in props.table[4]" class="table table-responsive">
          <thead><tr><th colspan="2">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th></tr></thead>
          <tbody>
            <tr><td width="25%">Вид</td><td>{{ tbl['view' as keyof typeof tbl] }}</td></tr>
            <tr><td width="25%">Контакт</td><td>{{ tbl['contact' as keyof typeof tbl] }}</td></tr>
          </tbody>
        </table>
        <p v-else >Данные отсутствуют</p>

        <button @click="data.flag = 'workplace'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Работа</button>
        <table v-if="props.table[5] && props.table[5].length" v-for="tbl in props.table[5]" class="table table-responsive">
          <thead><tr><th colspan="2">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th></tr></thead>
          <tbody>
            <tr><td width="25%">Период</td><td>{{ tbl['period' as keyof typeof tbl] }}</td></tr>
            <tr><td width="25%">Организация</td><td>{{ tbl['workplace' as keyof typeof tbl] }}</td></tr>
            <tr><td width="25%">Адрес</td><td>{{ tbl['address' as keyof typeof tbl] }}</td></tr>
            <tr><td width="25%">Должность</td><td>{{ tbl['position' as keyof typeof tbl] }}</td></tr>
          </tbody>
        </table>
        <p v-else >Данные отсутствуют</p>

        <button @click="data.flag = 'relation'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Связи</button>
        <table v-if="props.table[6] && props.table[6].length" v-for="tbl in props.table[6]" class="table table-responsive">
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
        <button @click="updateItem('0')" class="btn btn-outline-primary">Изменить анкету</button>
        <button @click="updateStatus" class="btn btn-outline-primary">Обновить статус</button>
        <button @click="sendResume" :disabled="config.status && (status !== config.status['new'] && status !== config.status['update'])" 
          class="btn btn-outline-primary">Отправить на проверку</button>
      </div>
    </template>
  </div>
</template>