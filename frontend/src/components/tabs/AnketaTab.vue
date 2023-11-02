<script setup lang="ts">

import { profileStore } from '@/store/profile';
import { classifyStore } from '@/store/classify';
import { clearItem } from '@share/utilities'
import ResumeForm from '@components/forms/ResumeForm.vue';
import RegionForm from '@components/forms/RegionForm.vue';
import StaffForm from '@components/forms/StaffForm.vue';
import DocumentForm from '@components/forms/DocumentForm.vue';
import AddressForm from '@components/forms/AddressForm.vue';
import ContactForm from '@components/forms/ContactForm.vue';
import RelationForm from '@components/forms/RelationForm.vue';
import WorkplaceForm from '@components/forms/WorkplaceForm.vue';

const storeProfile = profileStore();
const storeClassify = classifyStore();

</script>

<template>
  <div class="p-3">
  
    <template v-if="storeProfile.flag === 'resume' && storeProfile.action === 'update'" >
      <ResumeForm />
    </template>

    <template v-else>
      <RegionForm />
      <table v-if="storeProfile.profile.resume" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `ID #${storeProfile.profile.resume['id']}` }}</th>
            <th>
              <a href="#" @click="storeProfile.flag = 'resume'; 
                                  storeProfile.action = 'update';
                                  storeProfile.itemForm = storeProfile.profile.resume;
                                  storeProfile.itemId = storeProfile.profile.resume['id']"
                                  title="Изменить">
                <i class="bi bi-pencil-square"></i>
              </a>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="storeProfile.profile.resume['category']">
            <td>Категория</td>
            <td>{{ storeProfile.profile.resume['category'] }}</td>
          </tr>
          <tr>
            <td>Регион</td>
            <td>
              <a href="#" @click="storeProfile.flag = 'resume'; 
                                  storeProfile.action = 'location'; 
                                  storeProfile.itemForm = storeProfile.profile.resume;
                                  storeProfile.itemId = storeProfile.profile.resume['id']" 
                data-bs-toggle="modal" data-bs-target="#modalWin">
                {{ storeClassify.classifyItems.regions[storeProfile.profile.resume['region_id']]}}
              </a>
            </td>
          </tr>
          <tr>
            <td>Фамилия Имя Отчество</td>
            <td>{{ storeProfile.profile.resume['fullname'] }}</td>
          </tr>
          <tr v-if="storeProfile.profile.resume['previous']">
            <td>Изменение имени</td>
            <td>{{ storeProfile.profile.resume['previous'] }}</td>
          </tr>
          <tr>
            <td>Дата рождения</td>
            <td>{{ storeProfile.profile.resume['birthday'] }}</td>
          </tr>
          <tr>
            <td>Место рождения</td>
            <td>{{ storeProfile.profile.resume['birthplace'] 
                    ? storeProfile.profile.resume['birthplace'] 
                    : 'Данные отсутствуют' }}</td>
          </tr>
          <tr>
            <td>Гражданство</td>
            <td>{{ storeProfile.profile.resume['country'] 
                    ? storeProfile.profile.resume['country'] 
                    : 'Данные отсутствуют' }}</td>
          </tr>
          <tr>
            <td>СНИЛС</td>
            <td>{{ storeProfile.profile.resume['snils']
                    ? storeProfile.profile.resume['snils']
                    : 'Данные отсутствуют' }}</td>
          </tr>
          <tr>
            <td>ИНН</td>
            <td>{{ storeProfile.profile.resume['inn']
                    ? storeProfile.profile.resume['inn']
                    : 'Данные отсутствуют' }}</td>
          </tr>
          <tr>
            <td>Образование</td>
            <td>{{ storeProfile.profile.resume['education'] 
                    ? storeProfile.profile.resume['education']
                    : 'Данные отсутствуют' }}</td>
          </tr>
          <tr v-if="storeProfile.profile.resume['addition']">
            <td>Дополнительная информация</td>
            <td>{{ storeProfile.profile.resume['addition'] }}</td>
          </tr>
          <tr v-if="storeProfile.profile.resume['path']">
            <td>Материалы</td>
            <td>{{ storeProfile.profile.resume['path'] }}</td>
          </tr>
          <tr>
            <td>Статус</td>
            <td>
              <a href="#" @click="storeProfile.getItem('resume', 'status')">
                {{ storeProfile.profile.resume['status'] }}</a>
            </td>
          </tr>
          <tr v-if="storeProfile.profile.resume['create']">
            <td>Создан</td>
            <td>{{ new Date(String(storeProfile.profile.resume['create'])).
                  toLocaleDateString('ru-RU') }}</td>
          </tr>
          <tr v-if="storeProfile.profile.resume['update']">
            <td>Обновлен</td>
            <td>{{ new Date(String(storeProfile.profile.resume['update'])).
                  toLocaleDateString('ru-RU') }}</td>
          </tr>
          <tr v-if="storeProfile.profile.resume['request_id']">
            <td>Внешний id</td>
            <td>{{ storeProfile.profile.resume['request_id'] }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
    </template>
        
    <h6>Должности
      <a class="btn btn-link" @click="storeProfile.flag === 'staff' 
                                        ? storeProfile.flag = '' 
                                        : storeProfile.flag = 'staff'; 
                                      storeProfile.flag === 'staff' 
                                        ? storeProfile.action = 'create' 
                                        : storeProfile.action = ''; 
                                      clearItem(storeProfile.itemForm)" 
          :title="storeProfile.flag === 'staff' 
            ? 'Закрыть форму' : 'Добавить должность'">
        <i :class="storeProfile.flag === 'staff' 
            ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"></i>
      </a>
    </h6>
    <template v-if="storeProfile.flag === 'staff'">
      <StaffForm />
    </template>

    <template v-else>
      <table v-if="storeProfile.profile.staffs && storeProfile.profile.staffs.length" 
             v-for="tbl in storeProfile.profile.staffs" 
              :key="tbl['id']" class="table table-responsive">
        <thead>
          <tr>
            <th  width="25%">{{ `#${tbl['id']}` }}</th>
            <th>
              <a href="#" @click="storeProfile.deleteItem('staff', 'delete', tbl['id'].
                  toString())" title="Удалить">
                <i class="bi bi-trash"></i>
              </a>
              &nbsp;
              <a class="btn btn-link" @click= "storeProfile.flag = 'staff'; 
                                      storeProfile.action = 'update'; 
                                      storeProfile.itemId = tbl['id'].toString(); 
                                      storeProfile.itemForm = tbl" title="Изменить">
                <i class="bi bi-pencil-square"></i>
              </a>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Должность</td>
            <td>{{ tbl['position'] ? tbl['position'] : 'Данные отсутствуют' }}</td>
          </tr>
          <tr>
            <td>Департамент</td>
            <td>{{ tbl['department'] ? tbl['department'] : 'Данные отсутствуют' }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
    </template>

    <h6>Документы
      <a class="btn btn-link" @click="storeProfile.flag === 'document' 
                                ? storeProfile.flag = '' 
                                : storeProfile.flag = 'document'; 
                              storeProfile.flag === 'document' 
                                ? storeProfile.action = 'create' 
                                : storeProfile.action = ''; 
                              clearItem(storeProfile.itemForm)" 
          :title="storeProfile.flag === 'document' 
              ? 'Закрыть форму' : 'Добавить документ'">
        <i :class="storeProfile.flag === 'document' 
              ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"></i>
      </a>
    </h6>
    <template v-if="storeProfile.flag === 'document'">
      <DocumentForm />
    </template>
    
    <template v-else>
      <table v-if="storeProfile.profile.docums && storeProfile.profile.docums.length" 
             v-for="tbl in storeProfile.profile.docums" 
             :key="tbl['id']" class="table table-responsive">
        <thead>
          <tr>
            <th  width="25%">{{ `#${tbl['id']}` }}</th>
            <th>
              <a href="#" @click="storeProfile.deleteItem('document', 'delete', tbl['id'].toString())"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Удалить">
                          <i class="bi bi-trash"></i></a>
              &nbsp;
              <a class="btn btn-link" @click= "storeProfile.flag = 'document'; 
                                      storeProfile.action = 'update'; 
                                      storeProfile.itemId = tbl['id'].toString(); 
                                      storeProfile.itemForm = tbl" title="Изменить">
                <i class="bi bi-pencil-square"></i>
              </a>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Вид документа</td>
            <td>{{ tbl['view'] ? tbl['view'] : 'Данные отсутствуют' }}</td>
          </tr>
          <tr>
            <td>Серия</td>
            <td>{{ tbl['series'] ? tbl['series'] : 'Данные отсутствуют' }}</td>
          </tr>
          <tr>
            <td>Номер</td>
            <td>{{ tbl['number'] ? tbl['number'] : 'Данные отсутствуют' }}</td>
          </tr>
          <tr>
            <td>Кем выдан</td>
            <td>{{ tbl['agency'] ? tbl['agency'] : 'Данные отсутствуют' }}</td>
          </tr>
          <tr>
            <td>Дата выдачи</td>
            <td>{{ tbl['issue'] ? new Date(String(tbl['issue'])).
                                        toLocaleDateString('ru-RU') 
                                : 'Данные отсутствуют' }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
    </template>
    
    <h6>Адреса
      <a class="btn btn-link" @click="storeProfile.flag === 'address' 
                                ? storeProfile.flag = '' 
                                : storeProfile.flag = 'address'; 
                              storeProfile.flag === 'address' 
                                ? storeProfile.action = 'create' 
                                : storeProfile.action = ''; 
                              clearItem(storeProfile.itemForm)" 
          :title="storeProfile.flag === 'document' 
            ? 'Закрыть форму' : 'Добавить адрес'">
        <i :class="storeProfile.flag === 'address' 
            ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"></i>
      </a>
    </h6>
    <template v-if="storeProfile.flag === 'address'">
      <AddressForm />
    </template>
    
    <template v-else>
      <table v-if="storeProfile.profile.addrs && storeProfile.profile.addrs.length" 
             v-for="tbl in storeProfile.profile.addrs" 
              :key="tbl['id']" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `#${tbl['id']}` }}</th>
            <th>
              <a href="#" @click="storeProfile.deleteItem('address', 'delete', tbl['id'].toString())"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Удалить">
                          <i class="bi bi-trash"></i></a>
              &nbsp;
              <a class="btn btn-link" @click= "storeProfile.flag = 'address'; 
                                      storeProfile.action = 'update'; 
                                      storeProfile.itemId = tbl['id'].toString(); 
                                      storeProfile.itemForm = tbl" title="Изменить">
                <i class="bi bi-pencil-square"></i>
              </a>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Тип</td>
            <td>{{ tbl['view'] ? tbl['view'] : 'Данные отсутствуют' }}</td>
          </tr>
          <tr>
            <td>Регион</td>
            <td>{{ tbl['region'] ? tbl['region'] : 'Данные отсутствуют' }}</td>
          </tr>
          <tr>
            <td>Адрес</td>
            <td>{{ tbl['address'] ? tbl['address'] : 'Данные отсутствуют' }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
    </template>

    <h6>Контакты
      <a class="btn btn-link" @click="storeProfile.flag === 'contact' 
                                      ? storeProfile.flag = '' 
                                      : storeProfile.flag = 'contact'; 
                                      storeProfile.flag === 'contact' 
                                      ? storeProfile.action = 'create' 
                                      : storeProfile.action = ''; 
                                      clearItem(storeProfile.itemForm)" 
                              :title="storeProfile.flag === 'contact' 
                                      ? 'Закрыть форму' : 'Добавить контакт'">
        <i :class="storeProfile.flag === 'contact' 
            ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"></i>
      </a>
    </h6>
    <template v-if="storeProfile.flag === 'contact'">
      <ContactForm />
    </template>
    
    <template v-else>
      <table v-if="storeProfile.profile.conts && storeProfile.profile.conts.length" 
             v-for="tbl in storeProfile.profile.conts" :key="tbl['id']" 
                class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `#${tbl['id']}` }}</th>
            <th>
              <a href="#" @click="storeProfile.deleteItem('contact', 'delete', tbl['id'].toString())"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Удалить">
                          <i class="bi bi-trash"></i></a>
              &nbsp;
              <a class="btn btn-link" @click= "storeProfile.flag = 'contact'; 
                                      storeProfile.action = 'update'; 
                                      storeProfile.itemId = tbl['id'].toString(); 
                                      storeProfile.itemForm = tbl" title="Изменить">
                <i class="bi bi-pencil-square"></i>
              </a>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Вид</td>
            <td>{{ tbl['view'] ? tbl['view'] : 'Данные отсутствуют' }}</td>
          </tr>
          <tr>
            <td>Контакт</td>
            <td>{{ tbl['contact'] ? tbl['contact'] : 'Данные отсутствуют' }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
    </template>

    <h6>Работа
      <a class="btn btn-link" @click="storeProfile.flag === 'workplace' 
                                ? storeProfile.flag = '' 
                                : storeProfile.flag = 'workplace'; 
                              storeProfile.flag === 'workplace' 
                                ? storeProfile.action = 'create' 
                                : storeProfile.action = ''; 
                              clearItem(storeProfile.itemForm)" 
          :title="storeProfile.flag === 'workplace' 
            ? 'Закрыть форму' : 'Добавить работу'">
        <i :class="storeProfile.flag === 'workplace' 
            ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"></i>
      </a>
    </h6>
    <template v-if="storeProfile.flag === 'workplace'">
      <WorkplaceForm />
    </template>
    
    <template v-else>
      <table v-if="storeProfile.profile.works && storeProfile.profile.works.length" 
             v-for="tbl in storeProfile.profile.works" 
              :key="tbl['id']" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `#${tbl['id']}` }}</th>
            <th>
              <a href="#" @click="storeProfile.deleteItem('workplace', 'delete', tbl['id'].toString())"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Удалить">
                          <i class="bi bi-trash"></i></a>
              &nbsp;
              <a class="btn btn-link" @click= "storeProfile.flag = 'workplace'; 
                                      storeProfile.action = 'update'; 
                                      storeProfile.itemId = tbl['id'].toString(); 
                                      storeProfile.itemForm = tbl" title="Изменить">
                <i class="bi bi-pencil-square"></i>
              </a>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Период</td>
            <td>{{ tbl['start_date'] }} - {{ tbl['end_date'] }}</td>
          </tr>
          <tr>
            <td>Работает по н.в.</td>
            <td>{{ tbl['now_work'] ? 'Работает' : 'Не работает' }}</td>
          </tr>
          <tr>
            <td>Организация</td>
            <td>{{ tbl['workplace'] ? tbl['workplace'] : 'Данные отсутствуют' }}</td>
          </tr>
          <tr>
            <td>Адрес</td>
            <td>{{ tbl['address'] ? tbl['address'] : 'Данные отсутствуют' }}</td>
          </tr>
          <tr>
            <td>Должность</td>
            <td>{{ tbl['position'] ? tbl['position'] : 'Данные отсутствуют' }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
    </template>

    <h6>Связи
      <a class="btn btn-link" @click="storeProfile.flag === 'relation' 
                                ? storeProfile.flag = '' 
                                : storeProfile.flag = 'relation'; 
                              storeProfile.flag === 'relation' 
                                ? storeProfile.action = 'create' 
                                : storeProfile.action = ''; 
                              clearItem(storeProfile.itemForm)" 
          :title="storeProfile.flag === 'relation' 
            ? 'Закрыть форму' : 'Добавить связь'">
        <i :class="storeProfile.flag === 'relation' 
            ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"></i>
      </a>
    </h6>
    <template v-if="storeProfile.flag === 'relation'">
      <RelationForm />
    </template>
    
    <template v-else>
      <table v-if="storeProfile.profile.relate && storeProfile.profile.relate.length" 
             v-for="tbl in storeProfile.profile.relate" 
              :key="tbl['id']" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `#${tbl['id']}` }}</th>
            <th>
              <a href="#" @click="storeProfile.deleteItem('relation', 'delete', tbl['id'].toString())"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Удалить">
                          <i class="bi bi-trash"></i></a>
              &nbsp;
              <a class="btn btn-link" @click= "storeProfile.flag = 'relation'; 
                                      storeProfile.action = 'update'; 
                                      storeProfile.itemId = tbl['id'].toString(); 
                                      storeProfile.itemForm = tbl" title="Изменить">
                <i class="bi bi-pencil-square"></i>
              </a>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Тип связи</td><td>{{ tbl['relation'] }}</td></tr>
          <tr v-if="tbl['relation_id']">
            <td>Связь</td>
            <td>
              <router-link
                :to="{ name: 'profile', params: { group: 'staffsec', id: String(tbl['relation_id']) } }">
                ID #{{ tbl['relation_id'] }}
              </router-link>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
    </template>

    <div class="py-3">
      <div class='btn-group' role="group">
        <button @click="storeProfile.getItem('resume', 'send')" 
            :disabled="(storeProfile.profile.resume['status'] !== storeClassify.classifyItems.status['new'] 
              && storeProfile.profile.resume['status'] !== storeClassify.classifyItems.status['update']
              && storeProfile.profile.resume['status'] !== storeClassify.classifyItems.status['repeat']) 
              || storeProfile.spinner" 
            class="btn btn-outline-primary">{{ !storeProfile.spinner ? 'Отправить на проверку' : '' }}
          <span v-if="storeProfile.spinner" class="spinner-border spinner-border-sm" aria-hidden="true"></span>
          <span v-if="storeProfile.spinner" role="status">Отправляется...</span>
        </button>
        <button type="button" class="btn btn-outline-danger" 
          :disabled="storeProfile.profile.resume['status'] === storeClassify.classifyItems.status['finish']
            || storeProfile.spinner" 
          @click="storeProfile.deleteItem('resume', 'delete', storeProfile.profile.resume['id'])">
          Удалить анкету
        </button>
      </div>
    </div>
  
  </div>
</template>