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
  
const emit = defineEmits(['updateMessage', 'updateItem']);

const url = ref('');

async function submitData(event: Event) {
  try {
    const formData = new FormData(event.target as HTMLFormElement);
    const response = await axios.post(`${config.appUrl}/${url.value}/${props.candId}`, formData, {
      headers: {'Authorization': `Bearer ${localStorage.getItem('access_token')}`}
    });
    const { message } = response.data;
    emit('updateMessage', {
      attr: 'alert-success',
      text: `Запись добавлена для ID ${message}`
    });
    emit('updateItem', props.candId);
    url.value = ''
  } catch (error) {
    console.error(error);
  }
}

</script>

<template>
  <div class="py-3">
    <template v-if="url">
      <form @submit.prevent="submitData" class="form form-check" role="form"  id="poligrafFormId">
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="theme">Тема проверки</label>
          <div class="col-lg-10">
            <select class="form-select" id="theme" name="theme">
              <option value="Проверка кандидата">Проверка кандидата</option>
              <option value="Служебная проверка">Служебная проверка</option>
              <option value="Служебное расследование">Служебное расследование</option>
              <option value="Другое">Другое</option>
            </select>
          </div>
        </div>
        <div class="mb-3 row required">
          <label class="col-form-label col-lg-2" for="results">Результат</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="results" name="results" required></textarea>
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
        <thead><tr><th colspan="2">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th></tr></thead>
        <tbody>
          <tr><td width="25%">Тематика</td><td>{{ tbl['theme' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Результат</td><td>{{ tbl['results' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Полиграфолог</td><td>{{ tbl['officer' as keyof typeof tbl] }}</td></tr>
          <tr>
            <td width="25%">Дата</td>
            <td>{{ new Date(String(tbl['deadline' as keyof typeof tbl])).toLocaleDateString('ru-RU') }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
      <button @click="url = 'poligraf'" class="btn btn-outline-primary" type="button">Добавить запись</button>
    </template>
  </div>
  
</template>