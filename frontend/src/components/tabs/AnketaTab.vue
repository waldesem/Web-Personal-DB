<script setup lang="ts">

import { ref } from 'vue';
import { profileStore } from '@/store/profile';
import { classifyStore } from '@/store/classify';
import { fileManagerStore } from '@store/fmanager';
import { clearItem } from '@share/utilities'

const ResumeForm = () => import('@components/forms/ResumeForm.vue');
const RegionForm = () => import('@components/forms/RegionForm.vue');
const StaffForm = () => import('@components/forms/StaffForm.vue');
const DocumentForm = () => import('@components/forms/DocumentForm.vue');
const AddressForm = () => import('@components/forms/AddressForm.vue');
const ContactForm = () => import('@components/forms/ContactForm.vue');
const RelationForm = () => import('@components/forms/RelationForm.vue');
const WorkplaceForm = () => import('@components/forms/WorkplaceForm.vue');
const AffilationForm = () => import('@components/forms/AffilationForm.vue');

const storeProfile = profileStore();
const storeClassify = classifyStore();
const storeFmanager = fileManagerStore();

const hiddenSendBtn = ref(false);
const hiddenDelBtn = ref(false);

hiddenSendBtn.value = (storeProfile.profile.resume['status'] 
                        !== storeClassify.classifyItems.status['new'] 
                      && storeProfile.profile.resume['status'] 
                        !== storeClassify.classifyItems.status['update']
                      && storeProfile.profile.resume['status'] 
                        !== storeClassify.classifyItems.status['repeat']) 
                    || storeProfile.dataProfile.spinner

hiddenDelBtn.value = storeProfile.profile.resume['status']
                       === storeClassify.classifyItems.status['finish']
                    || storeProfile.dataProfile.spinner

function switchForm(item: string){
  storeProfile.dataProfile.flag === item 
    ? storeProfile.dataProfile.flag = '' 
    : storeProfile.dataProfile.flag = item;

  storeProfile.dataProfile.flag === item 
    ? storeProfile.dataProfile.action = 'create' 
    : storeProfile.dataProfile.action = ''; 

  clearItem(storeProfile.dataProfile.itemForm)
};

</script>

<template>
  <div class="p-3">
  
    <template v-if="storeProfile.dataProfile.flag === 'resume' 
                 && storeProfile.dataProfile.action === 'update'" >
      <ResumeForm />
    </template>

    <template v-else>
      <RegionForm />
      <table v-if="storeProfile.profile.resume" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `ID #${storeProfile.profile.resume['id']}` }}</th>
            <th>
              <a href="#" title="Изменить"
                 @click="storeProfile.openForm('resume', 'update', 
                                                storeProfile.profile.resume['id'],
                                                storeProfile.profile.resume)">
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
              <a href="#" data-bs-toggle="modal" data-bs-target="#modalRegion"
                 @click="storeProfile.openForm('resume', 'location', 
                                                storeProfile.profile.resume['id'], 
                                                storeProfile.profile.resume)">
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
            <td>
              <router-link @click="storeFmanager.fileManager.path = storeProfile.profile.resume['path'].split('/')" 
                           :to="{ name: 'manager',  params: { group: 'staffsec' } }">
              
                {{ storeProfile.profile.resume['path'] }}
              </router-link>
            </td>
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
      <a class="btn btn-link" :title="storeProfile.dataProfile.flag === 'staff' 
                                      ? 'Закрыть форму' : 'Добавить должность'"
         @click="switchForm('staff')">
        <i :class="storeProfile.dataProfile.flag === 'staff' 
          ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"></i>
      </a>
    </h6>
    <template v-if="storeProfile.dataProfile.flag === 'staff'">
      <StaffForm />
    </template>

    <template v-else>
      <div class="accordion" id="accordionStaff" v-if="storeProfile.profile.staffs.length">
        <div class="accordion-item" v-for="tbl, idx in storeProfile.profile.staffs" 
                                    :key="tbl['id']" >
          <h6 class="accordion-header">
            <button class="accordion-button" :class="{'collapsed': idx > 0 }" type="button" data-bs-toggle="collapse" 
                    :data-bs-target="`#collapseStaff${tbl['id']}`">
              {{ `ID #${tbl['id']}` }}
            </button>
          </h6>
          <div :id="`collapseStaff${tbl['id']}`" class="accordion-collapse collapse" 
               :class="{ 'show': idx === 0}" 
              data-bs-parent="#accordionStaff">
            <div class="accordion-body">
              <table class="table table-responsive">
                <thead>
                  <tr>
                    <th width="25%">
                      <a href="#" @click="storeProfile.deleteItem('staff', 'delete', tbl['id'].
                          toString())" title="Удалить">
                        <i class="bi bi-trash"></i>
                      </a>
                    </th>
                    <th>
                      <a class="btn btn-link" title="Изменить"
                        @click= "storeProfile.openForm('staff', 'update', tbl['id'].toString(), tbl)">
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
            </div>
          </div>
        </div>
      </div>
      <p v-else >Данные отсутствуют</p>
    </template>

    <h6>Документы
      <a class="btn btn-link" :title="storeProfile.dataProfile.flag === 'document' 
                                      ? 'Закрыть форму' : 'Добавить документ'"
         @click="switchForm('document')" >
        <i :class="storeProfile.dataProfile.flag === 'document' 
                              ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"></i>
      </a>
    </h6>
    <template v-if="storeProfile.dataProfile.flag === 'document'">
      <DocumentForm />
    </template>
    
    <template v-else>
      <div class="accordion" id="accordionDocument" v-if="storeProfile.profile.docums.length">
        <div class="accordion-item" v-for="tbl, idx in storeProfile.profile.docums" 
                                    :key="tbl['id']" >
          <h6 class="accordion-header">
            <button class="accordion-button" :class="{'collapsed': idx > 0 }" type="button" data-bs-toggle="collapse" 
                    :data-bs-target="`#collapseDocument${tbl['id']}`">
              {{ `ID #${tbl['id']}` }}
            </button>
          </h6>
          <div :id="`collapseDocument${tbl['id']}`" class="accordion-collapse collapse" 
               :class="{ 'show': idx === 0}" 
              data-bs-parent="#accordionDocument">
            <div class="accordion-body">
              <table class="table table-responsive">
                <thead>
                  <tr>
                    <th width="25%">
                      <a href="#" @click="storeProfile.deleteItem('document', 'delete', tbl['id'].
                          toString())" title="Удалить">
                        <i class="bi bi-trash"></i>
                      </a>
                    </th>
                    <th>
                      <a class="btn btn-link" title="Изменить"
                        @click= "storeProfile.openForm('document', 'update', tbl['id'].toString(), tbl)">
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
                    <td>{{ tbl['issue'] ? new Date(String(tbl['issue'])).toLocaleDateString('ru-RU') 
                                        : 'Данные отсутствуют' }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
      <p v-else >Данные отсутствуют</p>
    </template>
    
    <h6>Адреса
      <a class="btn btn-link" @click="switchForm('address')" 
          :title="storeProfile.dataProfile.flag === 'document' 
                  ? 'Закрыть форму' : 'Добавить адрес'">
        <i :class="storeProfile.dataProfile.flag === 'address' 
                  ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"></i>
      </a>
    </h6>
    <template v-if="storeProfile.dataProfile.flag === 'address'">
      <AddressForm />
    </template>
    
    <template v-else>
      <div class="accordion" id="accordionAddress" v-if="storeProfile.profile.addrs.length">
        <div class="accordion-item" v-for="tbl, idx in storeProfile.profile.addrs" 
                                    :key="tbl['id']" >
          <h6 class="accordion-header">
            <button class="accordion-button" :class="{'collapsed': idx > 0 }" type="button" data-bs-toggle="collapse" 
                    :data-bs-target="`#collapseAddress${tbl['id']}`">
              {{ `ID #${tbl['id']}` }}
            </button>
          </h6>
          <div :id="`collapseAddress${tbl['id']}`" class="accordion-collapse collapse" 
               :class="{ 'show': idx === 0}" 
              data-bs-parent="#accordionAddress">
            <div class="accordion-body">
              <table class="table table-responsive">
                <thead>
                  <tr>
                    <th width="25%">
                      <a href="#" @click="storeProfile.deleteItem('address', 'delete', tbl['id'].
                          toString())" title="Удалить">
                        <i class="bi bi-trash"></i>
                      </a>
                    </th>
                    <th>
                      <a class="btn btn-link" title="Изменить"
                        @click= "storeProfile.openForm('address', 'update', tbl['id'].toString(), tbl)">
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
            </div>
          </div>
        </div>
      </div>
      <p v-else >Данные отсутствуют</p>
    </template>

    <h6>Контакты
      <a class="btn btn-link" @click="switchForm('contact')" 
          :title="storeProfile.dataProfile.flag === 'contact' 
            ? 'Закрыть форму' : 'Добавить контакт'">
        <i :class="storeProfile.dataProfile.flag === 'contact' 
            ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"></i>
      </a>
    </h6>
    <template v-if="storeProfile.dataProfile.flag === 'contact'">
      <ContactForm />
    </template>
    
    <template v-else>
      <div class="accordion" id="accordionContact" v-if="storeProfile.profile.conts.length">
        <div class="accordion-item" v-for="tbl, idx in storeProfile.profile.conts" 
                                    :key="tbl['id']" >
          <h6 class="accordion-header">
            <button class="accordion-button" :class="{'collapsed': idx > 0 }" type="button" data-bs-toggle="collapse" 
                    :data-bs-target="`#collapseContact${tbl['id']}`">
              {{ `ID #${tbl['id']}` }}
            </button>
          </h6>
          <div :id="`collapseContact${tbl['id']}`" class="accordion-collapse collapse" 
               :class="{ 'show': idx === 0}" 
              data-bs-parent="#accordionContact">
            <div class="accordion-body">
              <table class="table table-responsive">
                <thead>
                  <tr>
                    <th width="25%">
                      <a href="#" @click="storeProfile.deleteItem('contact', 'delete', tbl['id'].
                          toString())" title="Удалить">
                        <i class="bi bi-trash"></i>
                      </a>
                    </th>
                    <th>
                      <a class="btn btn-link" title="Изменить"
                        @click= "storeProfile.openForm('contact', 'update', tbl['id'].toString(), tbl)">
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
            </div>
          </div>
        </div>
      </div>
      <p v-else >Данные отсутствуют</p>
    </template>

    <h6>Работа
      <a class="btn btn-link" @click="switchForm('workplace')" 
          :title="storeProfile.dataProfile.flag === 'workplace' 
            ? 'Закрыть форму' : 'Добавить работу'">
        <i :class="storeProfile.dataProfile.flag === 'workplace' 
            ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"></i>
      </a>
    </h6>
    <template v-if="storeProfile.dataProfile.flag === 'workplace'">
      <WorkplaceForm />
    </template>
    
    <template v-else>
      <div class="accordion" id="accordionWork" v-if="storeProfile.profile.works.length">
        <div class="accordion-item" v-for="tbl, idx in storeProfile.profile.works" 
                                    :key="tbl['id']" >
          <h6 class="accordion-header">
            <button class="accordion-button" :class="{'collapsed': idx > 0 }" type="button" data-bs-toggle="collapse" 
                    :data-bs-target="`#collapseWork${tbl['id']}`">
              {{ `ID #${tbl['id']}` }}
            </button>
          </h6>
          <div :id="`collapseWork${tbl['id']}`" class="accordion-collapse collapse" 
               :class="{ 'show': idx === 0}" 
              data-bs-parent="#accordionWork">
            <div class="accordion-body">
              <table class="table table-responsive">
                <thead>
                  <tr>
                    <th width="25%">
                      <a href="#" @click="storeProfile.deleteItem('workplace', 'delete', tbl['id'].
                          toString())" title="Удалить">
                        <i class="bi bi-trash"></i>
                      </a>
                    </th>
                    <th>
                      <a class="btn btn-link" title="Изменить"
                        @click= "storeProfile.openForm('workplace', 'update', tbl['id'].toString(), tbl)">
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
            </div>
          </div>
        </div>
      </div>
      <p v-else >Данные отсутствуют</p>
    </template>

    <h6>Аффилированность
      <a class="btn btn-link" @click="switchForm('affilation')" 
          :title="storeProfile.dataProfile.flag === 'affilation' 
            ? 'Закрыть форму' : 'Добавить участие'">
        <i :class="storeProfile.dataProfile.flag === 'affilation' 
            ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"></i>
      </a>
    </h6>
    <template v-if="storeProfile.dataProfile.flag === 'affilation'">
      <AffilationForm />
    </template>
    
    <template v-else>
      <div class="accordion" id="accordionAffilate" v-if="storeProfile.profile.affilation.length">
        <div class="accordion-item" v-for="tbl, idx in storeProfile.profile.affilation" 
                                    :key="tbl['id']" >
          <h6 class="accordion-header">
            <button class="accordion-button" :class="{'collapsed': idx > 0 }" type="button" data-bs-toggle="collapse" 
                    :data-bs-target="`#collapseAffilate${tbl['id']}`">
              {{ `ID #${tbl['id']}` }}
            </button>
          </h6>
          <div class="accordion-collapse collapse" data-bs-parent="#accordionAffilate"
                :id="`collapseAffilate${tbl['id']}`" 
                :class="{ 'show': idx === 0}" >
            <div class="accordion-body">
              <table class="table table-responsive">
                <thead>
                  <tr>
                    <th width="25%">
                      <a href="#" @click="storeProfile.deleteItem('affilation', 'delete', tbl['id'].
                          toString())" title="Удалить">
                        <i class="bi bi-trash"></i>
                      </a>
                    </th>
                    <th>
                      <a class="btn btn-link" title="Изменить"
                        @click= "storeProfile.openForm('affilation', 'update', tbl['id'].toString(), tbl)">
                        <i class="bi bi-pencil-square"></i>
                      </a>
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr><td>Тип участия</td><td>{{ tbl['view'] }}</td></tr>
                  <tr><td>Организация</td><td>{{ tbl['name'] }}</td></tr>
                  <tr><td>ИНН</td><td>{{ tbl['inn'] ? tbl['inn'] : 'Данных нет' }}</td></tr>
                  <tr><td>Должность</td><td>{{ tbl['position'] }}</td></tr>
                  <tr>
                    <td>Дата декларации</td>
                    <td>{{ new Date(tbl['deadline']).toLocaleDateString('ru-RU') }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
      <p v-else >Данные отсутствуют</p>
    </template>

    <h6>Связи
      <a class="btn btn-link" @click="switchForm('relation')" 
          :title="storeProfile.dataProfile.flag === 'relation' 
            ? 'Закрыть форму' : 'Добавить связь'">
        <i :class="storeProfile.dataProfile.flag === 'relation' 
            ? 'bi bi-dash-circle' : 'bi bi-plus-circle'"></i>
      </a>
    </h6>
    <template v-if="storeProfile.dataProfile.flag === 'relation'">
      <RelationForm />
    </template>
    
    <template v-else>
      <div class="accordion" id="accordionRelation" v-if="storeProfile.profile.relate.length">
        <div class="accordion-item" v-for="tbl, idx in storeProfile.profile.relate" 
                                    :key="tbl['id']" >
          <h6 class="accordion-header">
            <button class="accordion-button" :class="{'collapsed': idx > 0 }" type="button" data-bs-toggle="collapse" 
                    :data-bs-target="`#collapseRelation${tbl['id']}`">
              {{ `ID #${tbl['id']}` }}
            </button>
          </h6>
          <div :id="`collapseRelation${tbl['id']}`" class="accordion-collapse collapse" 
               :class="{ 'show': idx === 0}" 
              data-bs-parent="#accordionRelation">
            <div class="accordion-body">
              <table class="table table-responsive">
                <thead>
                  <tr>
                    <th width="25%">
                      <a href="#" @click="storeProfile.deleteItem('relation', 'delete', tbl['id'].
                          toString())" title="Удалить">
                        <i class="bi bi-trash"></i>
                      </a>
                    </th>
                    <th>
                      <a class="btn btn-link" title="Изменить"
                        @click= "storeProfile.openForm('relation', 'update', tbl['id'].toString(), tbl)">
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
            </div>
          </div>
        </div>
      </div>
      <p v-else >Данные отсутствуют</p>
    </template>

    <div class="py-3">
      <div class='btn-group' role="group">
        <button class="btn btn-outline-primary" 
                :disabled="hiddenSendBtn"
                @click="storeProfile.getItem('resume', 'send')" >
            {{ !storeProfile.dataProfile.spinner ? 'Отправить на проверку' : '' }}
          <span v-if="storeProfile.dataProfile.spinner" class="spinner-border spinner-border-sm"></span>
          <span v-if="storeProfile.dataProfile.spinner" role="status">Отправляется...</span>
        </button>
        <button type="button" class="btn btn-outline-danger" 
                :disabled="hiddenDelBtn" 
                @click="storeProfile.deleteItem('resume', 'delete', 
                                                storeProfile.profile.resume['id'])">
          Удалить анкету
        </button>
      </div>
    </div>
  
  </div>
</template>