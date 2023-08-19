<script setup lang="ts">
/* Компонент анкеты */

import { ref } from 'vue';
import { appClassify } from '@store/classify';
import { locationStore } from '@store/location';
import { appAuth } from '@store/auth';
import { appAlert } from '@store/alert';
import { appProfile } from '@/store/profile';
import server from '@store/server';
import ResumeForm from '@content/forms/ResumeForm.vue';
import RegionForm from '@content/forms/RegionForm.vue';
import StaffForm from '@content/forms/StaffForm.vue';
import DocumentForm from '@content/forms/DocumentForm.vue';
import AddressForm from '@content/forms/AddressForm.vue';
import ContactForm from '@content/forms/ContactForm.vue';
import RelationForm from '@content/forms/RelationForm.vue';
import WorkplaceForm from '@content/forms/WorkplaceForm.vue';

const emit = defineEmits(['updateItem', 'deleteItem', 'getProfile']);

const storeAuth = appAuth()

const classifyApp = appClassify();

const storeLocation = locationStore();

const storeAlert = appAlert();

const storeProfile = appProfile();

const flag = ref('');

const action = ref('');

const itemForm = ref({});

const itemId = ref('');


async function updateStatus(): Promise<any> {
  if (confirm("Вы действительно обновить статус?")) {
    const response = await storeAuth.axiosInstance.get(`${server}/anketa/status/${storeProfile.candId}`);
    const { message } = response.data;
    
    storeProfile.getProfile();
    
    storeAlert.alertAttr = message == classifyApp.status['update'] 
        ? "alert-success" 
        : "alert-warning";
    storeAlert.alertText = message == classifyApp.status['update'] 
        ? "Статус обновлен" 
        : "Анкету с текущим статусом обновить нельзя";
  }
}

/**
 * Sends the resume for verification.
 *
 * @return {Promise<void>} A promise that resolves when the resume is sent for verification.
 */
async function sendResume(): Promise<void> {
  if (confirm("Вы действительно хотите отправить анкету на проверку?")) {

    const resp = await storeAuth.axiosInstance.get(`${server}/anketa/send/${storeProfile.candId}`);
    const { msg } = resp.data;
    const textMessage = {
      robot: ['Анкета отправлена на проверку', "alert-success"],
      error: ['Отправка анкеты кандидата не удалась, либо анкета взята в работу', "alert-info"],
    };
    storeAlert.alertAttr = textMessage[msg as keyof typeof textMessage][1];
    storeAlert.alertText = textMessage[msg as keyof typeof textMessage][0];
    window.scrollTo(0,0)
  }
}

/**
 * Updates an item and emits an event.
 *
 * @param {Object} item - The item to update.
 * @return {void} This function does not return anything.
 */
 function updateItemEmit(item: Object): void {
  storeProfile.updateItem(storeProfile.candId, flag.value, action.value, itemId.value, item)
  cancelEdit();
};

/**
 * Cancels the current edit operation.
 *
 * @return {void} 
 */
function cancelEdit(): void {
  flag.value = '';
  action.value = '';
  itemId.value = '';
  itemForm.value = {}
};

</script>

<template>
  <div class="p-3">
  
    <template v-if="flag === 'resume'" >
      <ResumeForm :resume="storeProfile.anketa.resume" 
                  @cancelEdit="flag = ''" 
                  @updateProfile="storeProfile.getProfile"/>
    </template>

    <template v-else>
      <RegionForm :item="itemForm" @formItem="updateItemEmit"/>

      <table v-if="storeProfile.anketa.resume" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `ID #${storeProfile.anketa.resume['id']}` }}</th>
            <th>
              <a href="#" @click="flag = 'resume'" title="Изменить">
                <i class="bi bi-pencil-square"></i>
              </a>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Категория</td><td>{{ storeProfile.anketa.resume['category'] }}</td></tr>
          <tr>
            <td>Регион</td>
            <td>
              <a href="#" @click="flag = 'location'; action = 'update'; itemId = storeProfile.anketa.resume['id']" 
                data-bs-toggle="modal" data-bs-target="#modalWin">
                {{ storeLocation.regionsObject[storeProfile.anketa.resume['region_id']]}}</a>
            </td>
          </tr>
          <tr><td>Фамилия Имя Отчество</td><td>{{ storeProfile.anketa.resume['fullname'] }}</td></tr>
          <tr><td>Изменение имени</td><td>{{ storeProfile.anketa.resume['previous'] }}</td></tr>
          <tr><td>Дата рождения</td><td>{{ storeProfile.anketa.resume['birthday'] }}</td></tr>
          <tr><td>Место рождения</td><td>{{ storeProfile.anketa.resume['birthplace'] }}</td></tr>
          <tr><td>Гражданство</td><td>{{ storeProfile.anketa.resume['country'] }}</td></tr>
          <tr><td>СНИЛС</td><td>{{ storeProfile.anketa.resume['snils'] }}</td></tr>
          <tr><td>ИНН</td><td>{{ storeProfile.anketa.resume['inn'] }}</td></tr>
          <tr><td>Образование</td><td>{{ storeProfile.anketa.resume['education'] }}</td></tr>
          <tr><td>Дополнительная информация</td><td>{{ storeProfile.anketa.resume['addition'] }}</td></tr>
          <tr><td>Документы</td><td>{{ storeProfile.anketa.resume['path'] }}</td></tr>
          <tr>
            <td>Статус</td>
            <td><a href="#" @click="updateStatus">{{ storeProfile.anketa.resume['status'] }}</a></td>
          </tr>
          <tr>
            <td>Создан</td>
            <td>{{ new Date(String(storeProfile.anketa.resume['create'])).toLocaleDateString('ru-RU') }}</td>
          </tr>
          <tr>
            <td>Обновлен</td>
            <td>{{ new Date(String(storeProfile.anketa.resume['update'])).toLocaleDateString('ru-RU') }}</td>
          </tr>
          <tr><td>Внешний id</td><td>{{ storeProfile.anketa.resume['request_id'] }}</td></tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
    </template>
        
    <a class="btn btn-link" @click="flag === 'staff' ? flag = '' : flag = 'staff'; 
                                    flag === 'staff' ? action = 'create' : action = ''; 
                                    itemId = ''; itemForm = {}" 
                                    :title="flag === 'staff' ? 'Закрыть окно' : 'Добавить должность'">Должности</a>
    <template v-if="flag === 'staff'">
      <StaffForm :item="itemForm" @formItem="updateItemEmit"/>
    </template>
    
    <template v-else>
      <table v-if="storeProfile.anketa.staffs && storeProfile.anketa.staffs.length" v-for="tbl in storeProfile.anketa.staffs" class="table table-responsive">
        <thead>
          <tr>
            <th  width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
            <th>
              <a href="#" @click="emit('deleteItem', tbl['id' as keyof typeof tbl].toString(), 'staff')" title="Удалить">
                <i class="bi bi-trash"></i>
              </a>
              &nbsp;
              <a class="btn btn-link" @click= "flag = 'staff'; 
                                      action = 'update'; 
                                      itemId = tbl['id' as keyof typeof tbl].toString(); 
                                      itemForm = tbl" title="Изменить">
                <i class="bi bi-pencil-square"></i>
              </a>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Должность</td><td>{{ tbl['position' as keyof typeof tbl] }}</td></tr>
          <tr><td>Департамент</td><td>{{ tbl['department' as keyof typeof tbl] }}</td></tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
    </template>


    <a class="btn btn-link" @click="flag === 'document' ? flag = '' : flag = 'document'; 
                                    flag === 'document' ? action = 'create' : action = ''; 
                                    itemId = ''; itemForm = {}" 
                                    :title="flag === 'document' ? 'Закрыть окно' : 'Добавить документ'">Документы</a>
    <template v-if="flag === 'document'">
      <DocumentForm :item="itemForm" @formItem="updateItemEmit"/>
    </template>
    
    <template v-else>
      <table v-if="storeProfile.anketa.docums && storeProfile.anketa.docums.length" v-for="tbl in storeProfile.anketa.docums" class="table table-responsive">
        <thead>
          <tr>
            <th  width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
            <th>
              <a href="#" @click="emit('deleteItem', tbl['id' as keyof typeof tbl].toString(), 'document')"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Удалить">
                          <i class="bi bi-trash"></i></a>
              &nbsp;
              <a class="btn btn-link" @click= "flag = 'document'; 
                                      action = 'update'; 
                                      itemId = tbl['id' as keyof typeof tbl].toString(); 
                                      itemForm = tbl" title="Изменить">
                <i class="bi bi-pencil-square"></i>
              </a>
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
    </template>
      
    <a class="btn btn-link" @click="flag === 'address' ? flag = '' : flag = 'address'; 
                                    flag === 'address' ? action = 'create' : action = ''; 
                                    itemId = ''; itemForm = {}" 
                                    :title="flag === 'document' ? 'Закрыть окно' : 'Добавить адрес'">Адрес</a>
    <template v-if="flag === 'address'">
      <AddressForm :item="itemForm" @formItem="updateItemEmit"/>
    </template>
    
    <template v-else>
      <table v-if="storeProfile.anketa.addrs && storeProfile.anketa.addrs.length" v-for="tbl in storeProfile.anketa.addrs" class="table table-responsive">
        <thead>
          <tr>
            <th  width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
            <th>
              <a href="#" @click="emit('deleteItem', tbl['id' as keyof typeof tbl].toString(), 'address')"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Удалить">
                          <i class="bi bi-trash"></i></a>
              &nbsp;
              <a class="btn btn-link" @click= "flag = 'address'; 
                                      action = 'update'; 
                                      itemId = tbl['id' as keyof typeof tbl].toString(); 
                                      itemForm = tbl" title="Изменить">
                <i class="bi bi-pencil-square"></i>
              </a>
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
    </template>

    <a class="btn btn-link" @click="flag === 'contact' ? flag = '' : flag = 'contact'; 
                                    flag === 'contact' ? action = 'create' : action = ''; 
                                    itemId = ''; itemForm = {}" 
                                    :title="flag === 'contact' ? 'Закрыть окно' : 'Добавить контакт'">Контакты</a>
    <template v-if="flag === 'contact'">
      <ContactForm :item="itemForm" @formItem="updateItemEmit"/>
    </template>
    
    <template v-else>
      <table v-if="storeProfile.anketa.conts && storeProfile.anketa.conts.length" v-for="tbl in storeProfile.anketa.conts" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
            <th>
              <a href="#" @click="emit('deleteItem', tbl['id' as keyof typeof tbl].toString(), 'contact')"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Удалить">
                          <i class="bi bi-trash"></i></a>
              &nbsp;
              <a class="btn btn-link" @click= "flag = 'contact'; 
                                      action = 'update'; 
                                      itemId = tbl['id' as keyof typeof tbl].toString(); 
                                      itemForm = tbl" title="Изменить">
                <i class="bi bi-pencil-square"></i>
              </a>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Вид</td><td>{{ tbl['view' as keyof typeof tbl] }}</td></tr>
          <tr><td>Контакт</td><td>{{ tbl['contact' as keyof typeof tbl] }}</td></tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
    </template>

    <a class="btn btn-link" @click="flag === 'workplace' ? flag = '' : flag = 'workplace'; 
                                    flag === 'workplace' ? action = 'create' : action = ''; 
                                    itemId = ''; itemForm = {}" 
                                    :title="flag === 'workplace' ? 'Закрыть окно' : 'Добавить работу'">Работа</a>
    <template v-if="flag === 'workplace'">
      <WorkplaceForm :item="itemForm" @formItem="updateItemEmit"/>
    </template>
    
    <template v-else>
      <table v-if="storeProfile.anketa.works && storeProfile.anketa.works.length" v-for="tbl in storeProfile.anketa.works" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
            <th>
              <a href="#" @click="emit('deleteItem', tbl['id' as keyof typeof tbl].toString(), 'workplace')"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Удалить">
                          <i class="bi bi-trash"></i></a>
              &nbsp;
              <a class="btn btn-link" @click= "flag = 'workplace'; 
                                      action = 'update'; 
                                      itemId = tbl['id' as keyof typeof tbl].toString(); 
                                      itemForm = tbl" title="Изменить">
                <i class="bi bi-pencil-square"></i>
              </a>
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
    </template>

    <a class="btn btn-link" @click="flag === 'relation' ? flag = '' : flag = 'relation'; 
                                    flag === 'relation' ? action = 'create' : action = ''; 
                                    itemId = ''; itemForm = {}" 
                                    :title="flag === 'relation' ? 'Закрыть окно' : 'Добавить связь'">Связи</a>
    <template v-if="flag === 'relation'">
      <RelationForm :item="itemForm" @formItem="updateItemEmit"/>
    </template>
    
    <template v-else>
      <table v-if="storeProfile.anketa.relate && storeProfile.anketa.relate.length" v-for="tbl in storeProfile.anketa.relate" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
            <th>
              <a href="#" @click="emit('deleteItem', tbl['id' as keyof typeof tbl].toString(), 'relation')"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Удалить">
                          <i class="bi bi-trash"></i></a>
              &nbsp;
              <a class="btn btn-link" @click= "flag = 'relation'; 
                                      action = 'update'; 
                                      itemId = tbl['id' as keyof typeof tbl].toString(); 
                                      itemForm = tbl" title="Изменить">
                <i class="bi bi-pencil-square"></i>
              </a>
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
    </template>

    <div class="py-3">
      <button @click="sendResume" 
        :disabled="classifyApp.status 
        && (storeProfile.status !== classifyApp.status['new'] 
        && storeProfile.status !== classifyApp.status['update'])" 
        class="btn btn-outline-primary">Отправить на проверку
      </button>
    </div>
  
  </div>
</template>