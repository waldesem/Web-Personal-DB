<script setup lang="ts">

import { ref } from 'vue';
import { profileStore } from '@/store/profile';
import { classifyStore } from '@/store/classify';
import { clearItem } from '@utilities/utils'
import ResumeForm from '@components/forms/ResumeForm.vue';
import RegionForm from '@components/forms/RegionForm.vue';
import StaffForm from '@components/forms/StaffForm.vue';
import DocumentForm from '@components/forms/DocumentForm.vue';
import AddressForm from '@components/forms/AddressForm.vue';
import ContactForm from '@components/forms/ContactForm.vue';
import RelationForm from '@components/forms/RelationForm.vue';
import WorkplaceForm from '@components/forms/WorkplaceForm.vue';
import AffilationForm from '@components/forms/AffilationForm.vue';
import StaffAccord from '@components/tabs/accordions/StaffAccord.vue';
import DocumentAccord from '@components/tabs/accordions/DocumentAccord.vue';
import AddressAccord from '@components/tabs/accordions/AddressAccord.vue';
import ContactAccord from '@components/tabs/accordions/ContactAccord.vue';
import RelationAccord from '@components/tabs/accordions/RelationAccord.vue';
import WorkplaceAccord from '@components/tabs/accordions/WorkplaceAccord.vue';
import AffilationAccord from '@components/tabs/accordions/AffilationAccord.vue';

const storeProfile = profileStore();
const storeClassify = classifyStore();

const hiddenSendBtn = ref(false);
const hiddenDelBtn = ref(false);

hiddenSendBtn.value = (storeProfile.dataProfile.resume['status'] 
                        !== storeClassify.classData.status['new'] 
                      && storeProfile.dataProfile.resume['status'] 
                        !== storeClassify.classData.status['update']
                      && storeProfile.dataProfile.resume['status'] 
                        !== storeClassify.classData.status['repeat']) 
                    || storeProfile.dataProfile.spinner

hiddenDelBtn.value = storeProfile.dataProfile.resume['status']
                       === storeClassify.classData.status['finish']
                    || storeProfile.dataProfile.spinner

function switchForm(item: string){
  storeProfile.dataProfile.flag === item 
    ? storeProfile.dataProfile.flag = '' 
    : storeProfile.dataProfile.flag = item;

  storeProfile.dataProfile.flag === item 
    ? storeProfile.dataProfile.action = 'create' 
    : storeProfile.dataProfile.action = ''; 

  clearItem(storeProfile.dataProfile.form)
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
      <table v-if="storeProfile.dataProfile.resume" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `ID #${storeProfile.dataProfile.resume['id']}` }}</th>
            <th>
              <a href="#" title="Изменить"
                 @click="storeProfile.dataProfile.openForm('resume', 'update', 
                                                storeProfile.dataProfile.resume['id'],
                                                storeProfile.dataProfile.resume)">
                <i class="bi bi-pencil-square"></i>
              </a>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="storeProfile.dataProfile.resume['category']">
            <td>Категория</td>
            <td>{{ storeProfile.dataProfile.resume['category'] }}</td>
          </tr>
          <tr>
            <td>Регион</td>
            <td>
              <a href="#" data-bs-toggle="modal" data-bs-target="#modalRegion"
                 @click="storeProfile.dataProfile.openForm('resume', 'location', 
                                                storeProfile.dataProfile.resume['id'], 
                                                storeProfile.dataProfile.resume)">
                {{ storeClassify.classData.regions[storeProfile.dataProfile.resume['region_id']]}}
              </a>
            </td>
          </tr>
          <tr>
            <td>Фамилия Имя Отчество</td>
            <td>{{ storeProfile.dataProfile.resume['fullname'] }}</td>
          </tr>
          <tr v-if="storeProfile.dataProfile.resume['previous']">
            <td>Изменение имени</td>
            <td>{{ storeProfile.dataProfile.resume['previous'] }}</td>
          </tr>
          <tr>
            <td>Дата рождения</td>
            <td>{{ storeProfile.dataProfile.resume['birthday'] }}</td>
          </tr>
          <tr>
            <td>Место рождения</td>
            <td>{{ storeProfile.dataProfile.resume['birthplace'] 
                    ? storeProfile.dataProfile.resume['birthplace'] 
                    : 'Данные отсутствуют' }}</td>
          </tr>
          <tr>
            <td>Гражданство</td>
            <td>{{ storeProfile.dataProfile.resume['country'] 
                    ? storeProfile.dataProfile.resume['country'] 
                    : 'Данные отсутствуют' }}</td>
          </tr>
          <tr>
            <td>СНИЛС</td>
            <td>{{ storeProfile.dataProfile.resume['snils']
                    ? storeProfile.dataProfile.resume['snils']
                    : 'Данные отсутствуют' }}</td>
          </tr>
          <tr>
            <td>ИНН</td>
            <td>{{ storeProfile.dataProfile.resume['inn']
                    ? storeProfile.dataProfile.resume['inn']
                    : 'Данные отсутствуют' }}</td>
          </tr>
          <tr>
            <td>Образование</td>
            <td>{{ storeProfile.dataProfile.resume['education'] 
                    ? storeProfile.dataProfile.resume['education']
                    : 'Данные отсутствуют' }}</td>
          </tr>
          <tr v-if="storeProfile.dataProfile.resume['addition']">
            <td>Дополнительная информация</td>
            <td>{{ storeProfile.dataProfile.resume['addition'] }}</td>
          </tr>
          <tr v-if="storeProfile.dataProfile.resume['path']">
            <td>Материалы</td>
            <td>
              <router-link :to="{ name: 'manager',  params: { 
                  group: 'staffsec',  
                  path: storeProfile.dataProfile.resume['path'].split('/')
                } }">
                {{ storeProfile.dataProfile.resume['path'] }}
              </router-link>
            </td>
          </tr>
          <tr>
            <td>Статус</td>
            <td>
              <a href="#" @click="storeProfile.dataProfile.getItem('resume', 'status', storeProfile.dataProfile.candId)">
                {{ storeProfile.dataProfile.resume['status'] }}</a>
            </td>
          </tr>
          <tr v-if="storeProfile.dataProfile.resume['create']">
            <td>Создан</td>
            <td>{{ new Date(String(storeProfile.dataProfile.resume['create'])).
                  toLocaleDateString('ru-RU') }}</td>
          </tr>
          <tr v-if="storeProfile.dataProfile.resume['update']">
            <td>Обновлен</td>
            <td>{{ new Date(String(storeProfile.dataProfile.resume['update'])).
                  toLocaleDateString('ru-RU') }}</td>
          </tr>
          <tr v-if="storeProfile.dataProfile.resume['request_id']">
            <td>Внешний id</td>
            <td>{{ storeProfile.dataProfile.resume['request_id'] }}</td>
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
      <StaffAccord :store="storeProfile.dataProfile"/>
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
      <DocumentAccord :store="storeProfile.dataProfile"/>
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
      <AddressAccord :store="storeProfile.dataProfile"/>
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
      <ContactAccord :store="storeProfile.dataProfile"/>
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
      <WorkplaceAccord :store="storeProfile.dataProfile"/>
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
      <AffilationAccord :store="storeProfile.dataProfile"/>
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
      <RelationAccord :store="storeProfile.dataProfile"/>
    </template>

    <div class="py-3">
      <div class='btn-group' role="group">
        <button class="btn btn-outline-primary" 
                :disabled="hiddenSendBtn"
                @click="storeProfile.dataProfile.getItem('resume', 'send', storeProfile.dataProfile.candId)" >
            {{ !storeProfile.dataProfile.spinner ? 'Отправить на проверку' : '' }}
          <span v-if="storeProfile.dataProfile.spinner" class="spinner-border spinner-border-sm"></span>
          <span v-if="storeProfile.dataProfile.spinner" role="status">Отправляется...</span>
        </button>
        <button type="button" class="btn btn-outline-danger" 
                :disabled="hiddenDelBtn" 
                @click="storeProfile.dataProfile.deleteItem('resume', 'delete', 
                                                storeProfile.dataProfile.resume['id'])">
          Удалить анкету
        </button>
      </div>
    </div>
  
  </div>
</template>