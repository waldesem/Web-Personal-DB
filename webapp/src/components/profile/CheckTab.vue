<template>
  <div v-if="url" class="py-3">
    <form @submit.prevent="submitData" class="form form-check" role="form">
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="workplace">Проверка по месту работы</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="workplace" v-model="workplace"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="employee">Проверка по кадровому учету</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="employee" v-model="employee"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="document">Проверка документов</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="document" v-model="document"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="inn">Проверка ИНН</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="inn" v-model="inn"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="debt">Проверка задолженностей</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="debt" v-model="debt"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="bankruptcy">Проверка банкротства</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="bankruptcy" v-model="bankruptcy"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="bki">Проверка кредитной истории</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="bki" v-model="bki"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="courts">Проверка по решениям судов</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="courts" v-model="courts"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="affiliation">Проверка аффилированности</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="affiliation" v-model="affiliation"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="terrorist">Проверка списка террористов</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="terrorist" v-model="terrorist"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="mvd">Проверка учетам МВД</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="mvd" v-model="mvd"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="internet">Проверка по открытым источникам</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="internet" v-model="internet"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="cronos">Проверка Кронос</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="cronos" v-model="cronos"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="cros">Проверка Крос</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="cros" v-model="cros"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="addition">Дополнительная информация</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="addition" v-model="addition"></textarea>
        </div>
      </div>
      <div class=" row">
        <div class="offset-lg-2 col-lg-10">
          <div class="mb-3 form-check"><input class="form-check-input" id="pfo" v-model="pfo" type="checkbox" value="y">
            <label class="form-check-label" for="pfo">Полиграф</label>
          </div>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="conclusion">Результат</label>
        <div class="col-lg-10">
          <select class="form-select" id="conclusion" v-model="conclusion">
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
          <input class="form-control" id="comments" maxlength="250" v-model="comments" type="text">
        </div>
      </div>
      <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="deadline">Дата проверки</label>
        <div class="col-lg-10">
          <input class="form-control" id="deadline" v-model="deadline" required type="date">
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
  </div>
  <template v-else>
    <div v-html="table" class="py-3"></div>
    <div class="btn-group" role="group">
      <a @click="deleteCheck" :disabled="status === 'Окончено'" class="btn btn-outline-primary">Удалить проверку</a>
      <a @click="addCheck" :disabled="state && (status !== state['NEWFAG'] && status !== state['UPDATE'])" class="btn btn-outline-primary" type="button">Добавить проверку</a>
      <a @click="editCheck" :disabled="state && (status !== state['SAVE'] && status !== state['CANCEL'])"  class="btn btn-outline-primary" type="button">Изменить проверку</a>
    </div>
  </template>
</template>

<script setup lang="ts">

import axios from 'axios';
import { ref, toRefs } from 'vue';
import appUrl from '@/main';

const props = defineProps({
  table: String,
  item: Object,
  candId: String,
  state: Object,
  status: String
});

const { table, item, candId, state, status } = toRefs(props);

const emit = defineEmits(['updateMessage', 'updateItem'])

const url = ref('');
const workplace = ref('');
const employee = ref('');
const document = ref('');
const inn = ref('');
const debt = ref('');
const bankruptcy = ref('');
const bki = ref('');
const courts = ref('');
const affiliation = ref('');
const terrorist = ref('');
const mvd = ref('');
const internet = ref('');
const cronos = ref('');
const cros = ref('');
const addition = ref('');
const pfo = ref('');
const conclusion = ref('');
const comments = ref('');
const deadline = ref('');

async function submitData(event: Event){
  try {
    const formData = new FormData(event.target as HTMLFormElement);
    const response = await axios.post(`${appUrl}/check/new/${candId?.value}`, formData, {
      headers: {'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`}
    });
    const { message } = response.data;
    emit('updateMessage', {
      attr: "alert-warning",
      text: message
    });
    emit('updateItem', candId)
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
      emit('updateItem')
    } catch (error) {
    console.error(error);
    }
  }
}

async function addCheck() {
  url.value = 'new';
  const response = await axios.get(`${appUrl}/check/status/${candId?.value}`, {headers: {
    'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`
  }});
  const { message } = response.data;
  emit('updateMessage', {
    attr: "alert-warning",
    text: message
  });
}

async function editCheck() {
  if (item){
    const checkValue = item.value;
    if (checkValue) {
      url.value = 'edit';
      workplace.value = ref(checkValue.workplace);
      employee.value = ref(checkValue.employee);
      document.value = ref(checkValue.document);
      inn.value = ref(checkValue.inn);
      debt.value = ref(checkValue.debt);
      bankruptcy.value = ref(checkValue.bankruptcy);
      bki.value = ref(checkValue.bki);
      courts.value = ref(checkValue.courts);
      affiliation.value = ref(checkValue.affiliation);
      terrorist.value = ref(checkValue.terrorist);
      mvd.value = ref(checkValue.mvd);
      internet.value = ref(checkValue.internet);
      cronos.value = ref(checkValue.cronos);
      cros.value = ref(checkValue.cros);
      addition.value = ref(checkValue.addition);
      pfo.value = ref(checkValue.pfo);
      conclusion.value = ref(checkValue.conclusion);
      comments.value = ref(checkValue.comments);
      deadline.value = ref(checkValue.deadline)
    }
  }
}

</script>
