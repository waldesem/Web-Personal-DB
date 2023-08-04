<script setup lang="ts">

import { onBeforeMount, ref } from 'vue'
import axios from 'axios';
import config from '../../config';
import NavbarAdmin from './NavbarAdmin.vue'
import AlertMessage from '../AlertMessage.vue';
import FooterDiv from '../FooterDiv.vue';


const data = ref({
    logs: [],
    attr: '',
    text: ''
  });


onBeforeMount(async () => {
  logsList();
});


async function logsList() {
  try {
    const response = await axios.get(`${config.appUrl}/admin/logs`, {
      headers: {'Authorization': `Bearer ${localStorage.getItem('access_token')}`}
    });
    data.value.logs = response.data;
  } catch (error) {
    console.error(error);
  }
}


async function logAction(flag: string) {
  try {
    const response = await axios.get(`${config.appUrl}/admin/logs/${flag}`, {
      headers: {'Authorization': `Bearer ${localStorage.getItem('access_token')}`}
    });
    data.value.logs = response.data;
  } catch (error) {
    console.error(error);
  }
}

</script>


<template>
  <NavbarAdmin />
  <div class="container py-5">
    <AlertMessage v-if="data.attr" :attr="data.attr" :text="data.text" />
    <div class="py-5"><h4>Системные сообщения</h4></div>
    <div class="py-3">
      <table class="table table-hover table-responsive align-middle">
        <thead>
          <tr height="50px">
            <th width="5%">#</th>
            <th width="15%">Время</th>
            <th width="15%">Уровень</th>
            <th >Сообщение</th>
            <th width="15%">Путь</th>
            <th width="15%">Строка</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="log in data.logs" :key="log">
            <td>{{ log["id" as keyof typeof log] }}</td>
            <td>{{ new Date(log["timestamp" as keyof typeof log]).toLocaleString('ru-RU') }}</td>
            <td>{{ log["level" as keyof typeof log] }}</td>
            <td>{{ log["message" as keyof typeof log] }}</td>
            <td>{{ log["pathname" as keyof typeof log] }}</td>
            <td>{{ log["lineno" as keyof typeof log] }}</td>
          </tr>
        </tbody>
      </table>
      <div class="btn-group py-3" role="group">
        <button @click="logAction('reply')" class="btn btn-outline-primary" type="button">Отметить прочитанными</button>
        <button @click="logAction('delete')" class="btn btn-outline-primary" type="button">Удалить всё</button>
      </div>  
    </div>
  </div>
  <FooterDiv />
</template>