<script setup lang="ts">

import axios from 'axios';
import { ref } from 'vue';
import config from '../../config';
  
const props = defineProps({
  table: Array as () => Array<TableItem>,
  candId: String
});

type TableItem = {
  id: string;
  comments: string;
  decision: string;
  supervisor: string;
  deadline: Date;
};

const emit = defineEmits(['updateItem','updateMessage']);

const url = ref('');

async function submitData(event: Event) {
  try {
    const formData = new FormData(event.target as HTMLFormElement);
    const response = await axios.post(`${config.appUrl}/registry/${props.candId}`, formData, {
      headers: {'Authorization': `Bearer ${localStorage.getItem('access_token')}`}
    });
    const { message } = response.data;
    const alert = {
      'result': ['alert-success', 'Согласование отправлено'],
      'cancel': ['alert-warning', 'Отправка не удалась'],
      'error': ['alert-danger', 'Возникла ошибка']
    }
    emit('updateMessage', {
      attr: alert[message as keyof typeof alert][0],
      text: alert[message as keyof typeof alert][1]
    });
    url.value = '';
    emit('updateItem', props.candId);
  } catch (error) {
    console.error(error);
  }
}

</script>

<template>
  <div class="py-3">
    <template v-if="url">
      <form @submit.prevent="submitData" class="form form-check" role="form" id="registryFormId">
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="comments">Комментарий</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="comments" name="comments"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="decision">Решение</label>
          <div class="col-lg-10">
            <select class="form-select" id="decision" name="decision" value="">
              <option v-for="(name, value) in config.decisions" :key="name"  :value="value">{{ value }}</option>
            </select>
          </div>
        </div>
        <div class=" row">
          <div class="offset-lg-2 col-lg-10">
            <div class="btn-group" role="group">
              <button class="btn btn-outline-primary" type="submit">Принять</button>
              <button class="btn btn-outline-primary" type="reset">Очистить</button>
              <button class="btn btn-outline-primary" type="button" @click="url = ''">Отмена</button>
            </div>
          </div>
        </div>
      </form>
    </template>

    <template v-else>
      <table v-if="props.table?.length" v-for="tbl in props.table" class="table table-responsive">
        <thead><tr><th colspan="2">{{ `#${tbl['id']}` }}</th></tr></thead>
        <tbody>
          <tr><td width="25%">Комментарий</td><td>{{ tbl['comments'] }}</td></tr>
          <tr><td width="25%">Решение</td><td>{{ tbl['decision'] }}</td></tr>
          <tr><td width="25%">Согласующий</td><td>{{ tbl['supervisor'] }}</td></tr>
          <tr><td width="25%">Дата</td><td>{{ new Date(tbl['deadline']).toLocaleDateString('ru-RU') }}</td></tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
      <button @click="url = 'registry'" class="btn btn-outline-primary" type="button">Добавить запись</button>
    </template>
  </div>
</template>