<script setup lang="ts">
/* Компонент анкеты */

import { ref } from 'vue';
import { appClassify } from '@store/classify';
import { locationStore } from '@store/location';
import { appAuth } from '@store/auth';
import server from '@store/server';
import ModalWin from '@content/ModalWin.vue';
import ResumeForm from '@content/ResumeForm.vue';

const emit = defineEmits(['updateMessage', 'updateItem', 'deleteItem', 'getProfile']);

const storeAuth = appAuth()

const classifyApp = appClassify();

const storeLocation = locationStore();

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

const flag = ref('');

const modal = ref({});

const action = ref('');

const isHovered = ref(false);

/**
 * Updates the status.
 *
 * @return {Promise} The updated status.
 */
async function updateStatus(): Promise<any> {
  if (confirm("Вы действительно обновить статус?")) {
    const response = await storeAuth.axiosInstance.get(`${server}/anketa/status/${props.candId}`);
    const { message } = response.data;

    emit('updateMessage', {
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

/**
 * Sends the resume for verification.
 *
 * @return {Promise<void>} A promise that resolves when the resume is sent for verification.
 */
async function sendResume(): Promise<void> {
  if (confirm("Вы действительно хотите отправить анкету на проверку?")) {

    const resp = await storeAuth.axiosInstance.get(`${server}/anketa/send/${props.candId}`);
    const { msg } = resp.data;
    const textMessage = {
      robot: ['Анкета отправлена на проверку', "alert-success"],
      error: ['Отправка анкеты кандидата не удалась, либо анкета взята в работу', "alert-info"],
    };
    emit('updateMessage', {
      attr: textMessage[msg as keyof typeof textMessage][1],
      text: textMessage[msg as keyof typeof textMessage][0]
    });
    window.scrollTo(0,0)
  }
}

</script>

<template>

  <template v-if="flag === 'resume'" >
    <ResumeForm :resume="resume" 
                @cancelEdit="flag = ''" 
                @updateMessage="emit('updateMessage')" 
                @getProfile="emit('getProfile')"/>
  </template>

  <template v-else >
    <ModalWin :candId="props.candId" 
              :path="flag" 
              :modal="modal"
              :action="action"
              @updateItem="emit('updateItem')" />
    <div class="p-2">
      <table v-if="props.resume" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `ID #${props.resume['id']}` }}</th>
            <th @mouseover="isHovered = true" @mouseout="isHovered = false">
              <a href="#" :class="{isHovered ? 'link-opacity-75' : 'd-none'}" 
                          @click="flag = 'resume'"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Изменить">
                          <i class="bi bi-pencil-square"></i></a>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Категория</td><td>{{ props.resume['category'] }}</td></tr>
          <tr>
            <td>Регион</td>
            <td>
              <a href="#" @click="flag = 'location'; action = 'create'" data-bs-toggle="modal" data-bs-target="#modalWin">
                {{ storeLocation.regionsObject[props.resume['region_id']]}}</a>
            </td>
          </tr>
          <tr><td>Фамилия Имя Отчество</td><td>{{ props.resume['fullname'] }}</td></tr>
          <tr><td>Изменение имени</td><td>{{ props.resume['previous'] }}</td></tr>
          <tr><td>Дата рождения</td><td>{{ props.resume['birthday'] }}</td></tr>
          <tr><td>Место рождения</td><td>{{ props.resume['birthplace'] }}</td></tr>
          <tr><td>Гражданство</td><td>{{ props.resume['country'] }}</td></tr>
          <tr><td>СНИЛС</td><td>{{ props.resume['snils'] }}</td></tr>
          <tr><td>ИНН</td><td>{{ props.resume['inn'] }}</td></tr>
          <tr><td>Образование</td><td>{{ props.resume['education'] }}</td></tr>
          <tr><td>Дополнительная информация</td><td>{{ props.resume['addition'] }}</td></tr>
          <tr><td>Документы</td><td>{{ props.resume['path'] }}</td></tr>
          <tr>
            <td>Статус</td>
            <td><a href="#" @click="updateStatus">{{ props.resume['status'] }}</a></td>
          </tr>
          <tr>
            <td>Создан</td>
            <td>{{ new Date(String(props.resume['create'])).toLocaleDateString('ru-RU') }}</td>
          </tr>
          <tr>
            <td>Обновлен</td>
            <td>{{ new Date(String(props.resume['update'])).toLocaleDateString('ru-RU') }}</td>
          </tr>
          <tr><td>Внешний id</td><td>{{ props.resume['request_id'] }}</td></tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
      
      <button @click="flag = 'staff'; action = 'create'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Должность</button>
      <table v-if="props.staffs && props.staffs.length" v-for="tbl in props.staffs" class="table table-responsive">
        <thead>
          <tr>
            <th  width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
            <th @mouseover="isHovered = true" @mouseout="isHovered = false">
              <a href="#" :class="{isHovered ? 'link-opacity-75' : 'd-none'}" 
                          @click="emit('deleteItem', tbl['id' as keyof typeof tbl].toString(), 'staff')"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Удалить">
                          <i class="bi bi-trash"></i></a>
              <a href="#" :class="{isHovered ? 'link-opacity-75' : 'd-none'}" 
                          @click= "flag = 'staff'; action = 'update'; modal = tbl"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Изменить">
                          <i class="bi bi-pencil-square"></i></a>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Должность</td><td>{{ tbl['position' as keyof typeof tbl] }}</td></tr>
          <tr><td>Департамент</td><td>{{ tbl['department' as keyof typeof tbl] }}</td></tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
      
      <button @click="flag = 'document'; action = 'create'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Документы</button>
      <table v-if="props.docums && props.docums.length" v-for="tbl in props.docums" class="table table-responsive">
        <thead>
          <tr>
            <th  width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
            <th @mouseover="isHovered = true" @mouseout="isHovered = false">
              <a href="#" :class="{isHovered ? 'link-opacity-75' : 'd-none'}" 
                          @click="emit('deleteItem', tbl['id' as keyof typeof tbl].toString(), 'document')"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Удалить">
                          <i class="bi bi-trash"></i></a>
              <a href="#" :class="{isHovered ? 'link-opacity-75' : 'd-none'}" 
                          @click= "flag = 'document'; action = 'update'; modal = tbl"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Изменить">
                          <i class="bi bi-pencil-square"></i></a>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Вид документа</td><td>{{ tbl['view' as keyof typeof tbl] }}</td></tr>
          <tr><td>Серия</td><td>{{ tbl['series' as keyof typeof tbl] }}</td></tr>
          <tr><td>Номер</td><td>{{ tbl['number' as keyof typeof tbl] }}</td></tr>
          <tr><td>Кем выдан</td><td>{{ tbl['agency' as keyof typeof tbl] }}</td></tr>
          <tr><td>Дата выдачи</td><td>{{ new Date(String(tbl['issue' as keyof typeof tbl])).toLocaleDateString('ru-RU') }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
      
      <button @click="flag = 'address'; action = 'create'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Адреса</button>
      <table v-if="props.addrs && props.addrs.length" v-for="tbl in props.addrs" class="table table-responsive">
        <thead>
          <tr>
            <th  width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
            <th @mouseover="isHovered = true" @mouseout="isHovered = false">
              <a href="#" :class="{isHovered ? 'link-opacity-75' : 'd-none'}" 
                          @click="emit('deleteItem', tbl['id' as keyof typeof tbl].toString(), 'address')"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Удалить">
                          <i class="bi bi-trash"></i></a>
              <a href="#" :class="{isHovered ? 'link-opacity-75' : 'd-none'}" 
                          @click= "flag = 'address'; action = 'update'; modal = tbl"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Изменить">
                          <i class="bi bi-pencil-square"></i></a>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Тип</td><td>{{ tbl['view' as keyof typeof tbl] }}</td></tr>
          <tr><td>Регион</td><td>{{ tbl['region' as keyof typeof tbl] }}</td></tr>
          <tr><td>Адрес</td><td>{{ tbl['address' as keyof typeof tbl] }}</td></tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>

      <button @click="flag = 'contact'; action = 'create'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Контакты</button>
      <table v-if="props.conts && props.conts.length" v-for="tbl in props.conts" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
            <th @mouseover="isHovered = true" @mouseout="isHovered = false">
              <a href="#" :class="{isHovered ? 'link-opacity-75' : 'd-none'}" 
                          @click="emit('deleteItem', tbl['id' as keyof typeof tbl].toString(), 'contact')"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Удалить">
                          <i class="bi bi-trash"></i></a>
              <a href="#" :class="{isHovered ? 'link-opacity-75' : 'd-none'}" 
                          @click= "flag = 'contact'; action = 'update'; modal = tbl"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Изменить">
                          <i class="bi bi-pencil-square"></i></a>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Вид</td><td>{{ tbl['view' as keyof typeof tbl] }}</td></tr>
          <tr><td>Контакт</td><td>{{ tbl['contact' as keyof typeof tbl] }}</td></tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>

      <button @click="flag = 'workplace'; action = 'create'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Работа</button>
      <table v-if="props.works && props.works.length" v-for="tbl in props.works" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
            <th @mouseover="isHovered = true" @mouseout="isHovered = false">
              <a href="#" :class="{isHovered ? 'link-opacity-75' : 'd-none'}" 
                          @click="emit('deleteItem', tbl['id' as keyof typeof tbl].toString(), 'workplace')"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Удалить">
                          <i class="bi bi-trash"></i></a>
              <a href="#" :class="{isHovered ? 'link-opacity-75' : 'd-none'}" 
                          @click= "flag = 'workplace'; action = 'update'; modal = tbl"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Изменить">
                          <i class="bi bi-pencil-square"></i></a>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Период</td><td>{{ tbl['period' as keyof typeof tbl] }}</td></tr>
          <tr><td>Организация</td><td>{{ tbl['workplace' as keyof typeof tbl] }}</td></tr>
          <tr><td>Адрес</td><td>{{ tbl['address' as keyof typeof tbl] }}</td></tr>
          <tr><td>Должность</td><td>{{ tbl['position' as keyof typeof tbl] }}</td></tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>

      <button @click="flag = 'relation'; action = 'create'" type="button" class="btn btn-link" data-bs-toggle="modal" data-bs-target="#modalWin">Связи</button>
      <table v-if="props.relate && props.relate.length" v-for="tbl in props.relate" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
            <th @mouseover="isHovered = true" @mouseout="isHovered = false">
              <a href="#" :class="{isHovered ? 'link-opacity-75' : 'd-none'}" 
                          @click="emit('deleteItem', tbl['id' as keyof typeof tbl].toString(), 'relation')"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Удалить">
                          <i class="bi bi-trash"></i></a>
              <a href="#" :class="{isHovered ? 'link-opacity-75' : 'd-none'}" 
                          @click= "flag = 'relation'; action = 'update'; modal = tbl"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Изменить">
                          <i class="bi bi-pencil-square"></i></a>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Тип связи</td><td>{{ tbl['relation' as keyof typeof tbl] }}</td></tr>
          <tr>
            <td>Связь</td>
            <td><router-link :to="{ name: 'profile', params: {id: String(tbl['relation_id' as keyof typeof tbl])} }">
              Связь ID #{{ tbl['relation_id' as keyof typeof tbl] }}</router-link></td>
          </tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
    </div>

    <div class="py-3">
      <button @click="sendResume" 
        :disabled="classifyApp.status 
        && (status !== classifyApp.status['new'] 
        && status !== classifyApp.status['update'])" 
        class="btn btn-outline-primary">Отправить на проверку
      </button>
    </div>
  </template>

</template>