<template>
  <div v-if="url" class="py-3">
    <form @submit.prevent="submitData" class="form form-check" role="form">
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="workplace">Проверка по месту работы</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="workplace" name="workplace" v-model="check.workplace"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="employee">Проверка по кадровому учету</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="employee" name="employee" v-model="check.employee"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="document">Проверка документов</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="document" name="document" v-model="check.document"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="inn">Проверка ИНН</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="inn" name="inn" v-model="check.inn"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="debt">Проверка задолженностей</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="debt" name="debt" v-model="check.debt"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="bankruptcy">Проверка банкротства</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="bankruptcy" name="bankruptcy" v-model="check.bankruptcy"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="bki">Проверка кредитной истории</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="bki" name="bki" v-model="check.bki"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="courts">Проверка по решениям судов</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="courts" name="courts" v-model="check.courts"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="affiliation">Проверка аффилированности</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="affiliation" name="affiliation" v-model="check.affiliation"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="terrorist">Проверка списка террористов</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="terrorist" name="terrorist" v-model="check.terrorist"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="mvd">Проверка учетам МВД</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="mvd" name="mvd" v-model="check.mvd"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="internet">Проверка по открытым источникам</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="internet" name="internet" v-model="check.internet"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="cronos">Проверка Кронос</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="cronos" name="cronos" v-model="check.cronos"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="cros">Проверка Крос</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="cros" name="cros" v-model="check.cros"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="addition">Дополнительная информация</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="addition" name="addition" v-model="check.addition"></textarea>
        </div>
      </div>
      <div class=" row">
        <div class="offset-lg-2 col-lg-10">
          <div class="mb-3 form-check">
            <input class="form-check-input" id="pfo" name="pfo" v-model="check.pfo" type="checkbox" value="y">
            <label class="form-check-label" for="pfo">Полиграф</label>
          </div>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="conclusion">Результат</label>
        <div class="col-lg-10">
          <select class="form-select" id="conclusion" name="conclusion" v-model="check.conclusion">
            <option value="Без замечаний">Без замечаний</option>
            <option value="С комментарием">С комментарием</option>
            <option value="Негатив">Негатив</option>
            <option value="Отмена">Отмена</option>
            <option value="Сохранено">Сохранено</option>
          </select>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="comments">Комментарий</label>
        <div class="col-lg-10">
          <input class="form-control" id="comments" name="comments" maxlength="250" v-model="check.comments" type="text">
        </div>
      </div>
      <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="deadline">Дата проверки</label>
        <div class="col-lg-10">
          <input class="form-control" id="deadline" name="deadline" v-model="check.deadline" required type="date">
        </div>
      </div>
      <div class=" row">
        <div class="offset-lg-2 col-lg-10">
          <div class="btn-group" role="group">
            <button class="btn btn-outline-primary" type="submit">Принять</button>
            <button class="btn btn-outline-primary" type="reset">Очистить</button>
            <button class="btn btn-outline-primary" type="button" @click="updateStatus">Отмена</button>
          </div>
        </div>
      </div>
    </form>
  </div>
  <template v-else>
    <div v-html="table" class="py-3"></div>
    <div class="btn-group" role="group">
      <button @click="deleteCheck" :disabled="state && (status === state['FINISH'])" class="btn btn-outline-primary">Удалить проверку</button>
      <button @click="addCheck" :disabled="state && (status !== state['NEWFAG'] && status !== state['UPDATE'])" class="btn btn-outline-primary">Добавить проверку</button>
      <button @click="url='edit'" :disabled="state && (status !== state['SAVE'] && status !== state['CANCEL'])"  class="btn btn-outline-primary">Изменить проверку</button>
    </div>
  </template>
</template>

<script setup lang="ts">

import axios from 'axios';
import { ref, toRefs } from 'vue';
import appUrl from '@/config';

const emit = defineEmits(['updateMessage', 'updateItem'])

const props = defineProps({
  table: String,
  item: Object,
  candId: String,
  state: Object,
  status: String
});
const { table, item, candId, state, status } = toRefs(props);


let check: any = {};
if (item?.value) {
  check = item.value;
}

const url = ref('');

async function submitData(event: Event){
  try {
    const formData = new FormData(event.target as HTMLFormElement);
    const response = await axios.post(`${appUrl}/check/${url.value}/${candId?.value}`, formData, {
      headers: {'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`}
    });
    const { message } = response.data;
    emit('updateMessage', {
      attr: "alert-warning",
      text: message
    });
    emit('updateItem', candId?.value)
    url.value = ''
  } catch (error) {
    console.log(error);
  }
}
    
async function deleteCheck() {
  if (confirm("Вы действительно хотите удалить проверку?")) {
    try {
      const response = await axios.get(`${appUrl}/check/delete/${candId?.value}`, {headers: {
        'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`
      }});
      const { message } = response.data;
      emit('updateMessage', {
        attr: "alert-warning",
        text: message
      });
      emit('updateItem', candId?.value)
      window.scrollTo(0,0)
    } catch (error) {
    console.error(error);
    }
  }
}

async function addCheck() {
  try {
    const response = await axios.get(`${appUrl}/check/status/${candId?.value}`, {headers: {
      'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`
    }});
    const { message, alert } = response.data;
    alert == "alert-danger" ? url.value = '' : url.value = 'new';
    emit('updateMessage', {
      attr: alert,
      text: message
    });
  } catch (error) {
    console.error(error)
  }
}

async function updateStatus() {
  url.value = '';
  const response = await axios.get(`${appUrl}/resume/status/${candId?.value}`, {
    headers : {'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`}
  });
  const { message } = response.data;
  emit('updateMessage', {
    attr: "",
    text: message
  });
  window.scrollTo(0,0)
}

</script>
