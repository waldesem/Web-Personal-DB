<script setup lang="ts">
// компонент для отображения логов

import { onBeforeMount, ref } from 'vue'
import { appAuth } from '@store/auth';
import { appAlert } from '@store/alert';
import server from '@store/server';

const storeAuth = appAuth();

const storeAlert = appAlert();

const logs = ref([]);

// получение списка логов при загрузке страницы
onBeforeMount(async () => {
  logsList();
});

/**
 * Retrieves a list of logs from the server and updates the 'logs' value accordingly.
 *
 * @return {Promise<void>} A promise that resolves when the logs are successfully retrieved and updated.
 */
async function logsList(): Promise<void> {
  try {
    const response = await storeAuth.axiosInstance.get(`${server}/logs`);
    logs.value = response.data;
  
  } catch (error) {
    console.error(error);
  }
}


/**
 * Fetches logs based on the given flag and stores the result in the 'logs' variable.
 *
 * @param {string} flag - The flag to filter the logs by ('delete' or 'reply').
 * @return {Promise<void>} - A promise that resolves with no value.
 */
async function logAction(flag: string): Promise<void> {
  try {
    const response = await storeAuth.axiosInstance.get(`${server}/logs/${flag}`);
    logs.value = response.data;
    storeAlert.alertAttr = 'alert-info';
    storeAlert.alertText = flag === 'delete' ? 'Лог успешно удален' : 'Лог отмечен как прочитанный';
  
  } catch (error) {
    console.error(error);
  }
}

</script>


<template>
  <div class="container py-3">
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
          <tr v-for="log in logs" :key="log">
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
</template>