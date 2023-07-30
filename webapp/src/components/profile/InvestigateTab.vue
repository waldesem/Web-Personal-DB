<script setup lang="ts">

import axios from 'axios';
import { ref } from 'vue';
import config from '@/config';

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
      <form @submit.prevent="submitData" class="form form-check" role="form" id="investigationFormId">
        <div class="mb-3 row required">
          <label class="col-form-label col-lg-2" for="theme">Тема проверки</label>
          <div class="col-lg-10">
            <input class="form-control" id="theme" maxlength="250" name="theme" required type="text" value="">
          </div>
        </div>
        <div class="mb-3 row required">
          <label class="col-form-label col-lg-2" for="info">Информация</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="info" name="info" required></textarea>
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
          <tr><td width="25%">Тема</td><td>{{ tbl['theme' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Информация</td><td>{{ tbl['info' as keyof typeof tbl] }}</td></tr>
          <tr>
            <td width="25%">Дата</td>
            <td>{{ new Date(String(tbl['deadline' as keyof typeof tbl])).toLocaleDateString('ru-RU') }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
      <a @click="url = 'investigation'" class="btn btn-outline-primary" type="button">Добавить запись</a>
    </template>
  </div>
</template>