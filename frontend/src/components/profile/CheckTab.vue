<script setup lang="ts">

import axios from 'axios';
import { ref, toRefs } from 'vue';
import config from '../../config';

const emit = defineEmits(['updateMessage', 'updateItem'])

const props = defineProps({
  table: Array as () => Array<TableItem>,
  item: Object,
  candId: String,
  status: String
});


type TableItem = {
  id: string;
  comments: string;
  decision: string;
  supervisor: string;
  deadline: Date;
};

const { item } = toRefs(props);
const check = item?.value ?? {};

const url = ref('');

const headers = {
  headers: {'Authorization': `Bearer ${localStorage.getItem('access_token')}`}
};


async function addCheck() {
  if (props.status === config.status.save || 
    props.status === config.status.manual ||
    props.status === config.status.robot) {
    emit('updateMessage', {
      attr: 'alert-warning',
      text: 'Нельзя добавить проверку к текущему статусу'
    })
  } else {
    try {
      const response = await axios.get(`${config.appUrl}/check/add/${props.candId}`, headers);
      const { message } = response.data;
      message === "manual" ? url.value = 'new' : url.value = '';
      emit('updateMessage', {
        attr: message === "manual" ? 'alert-info' : 'alert-warning',
        text: message === "manual" ? 'Начата ручная проверка' : 'Проверка кандидата уже начата'
      });
    } catch (error) {
      console.error(error)
    }
  }
};


async function submitData(){
  try {
    const response = await axios.post(`${config.appUrl}/check/create/${props.candId}`, check, headers);
    const { message } = response.data;
    const alert = {
      'save': ['alert-info', 'Проверка сохранена'],
      'cancel': ['alert-warning', 'Проверка отменена'],
      'poligraf': ['alert-info', 'Окончено. Назначено проведение ПФО'],
      'result': ['alert-success', 'Проверка окончена']
    }
    
    emit('updateMessage', {
      attr: alert[message as keyof typeof alert][0],
      text: alert[message as keyof typeof alert][1]
    });

    emit('updateItem', props.candId)
    url.value = ''
  } catch (error) {
    console.log(error);
  }
};


function deleteCheck() {
  if (props.status === config.status.robot) {
  emit('updateMessage', {
      attr: 'alert-warning',
      text: 'Нельзя удалить проверку с текущим статусом'
    })
  } else {
    if (confirm("Вы действительно хотите удалить проверку?")) {
      checkDelete();
    }
  }
};

async function cancelCheck() {
  checkDelete();
  url.value = '';
  const response = await axios.get(`${config.appUrl}/anketa/status/${props.candId}`, headers);
  const { message } = response.data;
  emit('updateMessage', {
    attr: message == 'update' ? "alert-success" : "alert-warning",
    text: message == 'update' ? "Статус обновлен" : "Текущий статус обновить нельзя",
  });
  window.scrollTo(0,0)
}

async function checkDelete() {
  try {
    const response = await axios.get(`${config.appUrl}/check/delete/${props.candId}`, headers);
    const { message } = response.data;
    emit('updateMessage', {
      attr: message === "reply" ? 'alert-success' : 'alert-warning',
      text: message === "reply" ? 'Проверка удалена' : 'Проверку с текущим статусом удалить нельзя'
    });
    emit('updateItem', props.candId)
    window.scrollTo(0,0)
  } catch (error) {
  console.error(error);
  }
};

</script>

<template>
  <div class="py-3">
    <template v-if="url">
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
              <option v-for="(name, value) in config.conclusions" :key="value" :value="name">{{ name }}</option>
            </select>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="comments">Комментарий</label>
          <div class="col-lg-10">
            <input class="form-control" id="comments" name="comments" maxlength="250" v-model="check.comments" type="text">
          </div>
        </div>
        <div class=" row">
          <div class="offset-lg-2 col-lg-10">
            <div class="btn-group" role="group">
              <button class="btn btn-outline-primary" type="submit">Принять</button>
              <button class="btn btn-outline-primary" type="reset">Очистить</button>
              <button class="btn btn-outline-primary" type="button" @click="cancelCheck">Отмена</button>
            </div>
          </div>
        </div>
      </form>
    </template>
    <template v-else>
      <table v-if="props.table?.length" v-for="tbl in props.table" class="table table-responsive">
        <thead><tr><th colspan="2">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th></tr></thead>
        <tbody>
          <tr><td width="25%">Проверка по местам работы</td><td>{{ tbl['workplace' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Бывший работник МТСБ</td><td>{{ tbl['employee' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Проверка паспорта</td><td>{{ tbl['document' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Проверка ИНН</td><td>{{ tbl['inn' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Проверка ФССП</td><td>{{ tbl['debt' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Проверка банкротства</td><td>{{ tbl['bankruptcy' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Проверка БКИ</td><td>{{ tbl['bki' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Проверка судебных дел</td><td>{{ tbl['courts' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Проверка аффилированности</td><td>{{ tbl['affiliation' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Проверка по списку террористов</td><td>{{ tbl['terrorist' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Проверка нахождения в розыске</td><td>{{ tbl['mvd' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Проверка в открытых источниках</td><td>{{ tbl['internet' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Проверка Кронос</td><td>{{ tbl['cronos' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Проверка Крос</td><td>{{ tbl['cros' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Дополнительная информация</td><td>{{ tbl['addition' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Материалы проверки</td><td>{{ tbl['path' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">ПФО</td><td>{{ tbl['pfo' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Комментарии</td><td>{{ tbl['comments' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Результат проверки</td><td>{{ tbl['conclusion' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Сотрудник</td><td>{{ tbl['officer' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Дата</td><td>{{ new Date(String(tbl['deadline' as keyof typeof tbl])).toLocaleDateString('ru-RU') }}</td></tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
      <div class="btn-group" role="group">
        <button @click="deleteCheck" :disabled="config.status && (status === config.status['finish'])" class="btn btn-outline-primary">Удалить проверку</button>
        <button @click="addCheck" :disabled="config.status && (status !== config.status['new'] && 
                                                               status !== config.status['update'])" class="btn btn-outline-primary">Добавить проверку</button>
        <button @click="url='edit'" :disabled="config.status && (status !== config.status['save'] && 
                                                                 status !== config.status['cancel'] && 
                                                                 status !== config.status['manual'])"  class="btn btn-outline-primary">Изменить проверку</button>
      </div>
    </template>
  </div>
</template>