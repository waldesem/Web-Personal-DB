<script setup lang="ts">
/* Компонент анкеты */

import { appProfile } from '@/store/profile';
import { appClassify } from '@/store/classify';
import ResumeForm from '@content/forms/ResumeForm.vue';
import RegionForm from '@content/forms/RegionForm.vue';
import StaffForm from '@content/forms/StaffForm.vue';
import DocumentForm from '@content/forms/DocumentForm.vue';
import AddressForm from '@content/forms/AddressForm.vue';
import ContactForm from '@content/forms/ContactForm.vue';
import RelationForm from '@content/forms/RelationForm.vue';
import WorkplaceForm from '@content/forms/WorkplaceForm.vue';

const storeProfile = appProfile();
const storeClassify = appClassify();

</script>

<template>
  <div class="p-3">
  
    <template v-if="storeProfile.flag === 'resume'" >
      <ResumeForm />
    </template>

    <template v-else>
      <RegionForm />
      <table v-if="storeProfile.anketa.resume" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `ID #${storeProfile.anketa.resume['id']}` }}</th>
            <th v-if="!storeProfile.printPdf">
              <a href="#" @click="storeProfile.flag = 'resume'; 
                                  storeProfile.action = 'update';
                                  storeProfile.itemForm = storeProfile.anketa.resume;
                                  storeProfile.itemId = storeProfile.anketa.resume['id']"
                                  title="Изменить">
                <i class="bi bi-pencil-square"></i>
              </a>
            </th>
            <th v-else></th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Категория</td><td>{{ storeProfile.anketa.resume['category'] }}</td></tr>
          <tr>
            <td>Регион</td>
            <td>
              <a href="#" @click="storeProfile.flag = 'location'; 
                                  storeProfile.action = 'update'; 
                                  storeProfile.itemForm = storeProfile.anketa.resume;
                                  storeProfile.itemId = storeProfile.anketa.resume['id']" 
                data-bs-toggle="modal" data-bs-target="#modalWin">
                {{ storeClassify.regions[storeProfile.anketa.resume['region_id']]}}
              </a>
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
            <td><a href="#" @click="storeProfile.updateStatus">{{ storeProfile.anketa.resume['status'] }}</a></td>
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
        
    <a class="btn btn-link" @click="storeProfile.flag === 'staff' ? storeProfile.flag = '' : storeProfile.flag = 'staff'; 
                                    storeProfile.flag === 'staff' ? storeProfile.action = 'create' : storeProfile.action = ''; 
                                    storeProfile.clearItem" 
                                    :title="storeProfile.flag === 'staff' ? 'Закрыть форму' : 'Добавить должность'">Должности</a>
    <template v-if="storeProfile.flag === 'staff'">
      <StaffForm />
    </template>

    <template v-else>
      <table v-if="storeProfile.anketa.staffs && storeProfile.anketa.staffs.length" v-for="tbl in storeProfile.anketa.staffs" :key="tbl['id']" class="table table-responsive">
        <thead>
          <tr>
            <th  width="25%">{{ `#${tbl['id']}` }}</th>
            <th v-if="!storeProfile.printPdf">
              <a href="#" @click="storeProfile.deleteItem(tbl['id'].toString(), 'staff')" title="Удалить">
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
            <th v-else></th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Должность</td><td>{{ tbl['position'] }}</td></tr>
          <tr><td>Департамент</td><td>{{ tbl['department'] }}</td></tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
    </template>


    <a class="btn btn-link" @click="storeProfile.flag === 'document' ? storeProfile.flag = '' : storeProfile.flag = 'document'; 
                                    storeProfile.flag === 'document' ? storeProfile.action = 'create' : storeProfile.action = ''; 
                                    storeProfile.clearItem" 
      :title="storeProfile.flag === 'document' ? 'Закрыть форму' : 'Добавить документ'">Документы</a>
    <template v-if="storeProfile.flag === 'document'">
      <DocumentForm />
    </template>
    
    <template v-else>
      <table v-if="storeProfile.anketa.docums && storeProfile.anketa.docums.length" v-for="tbl in storeProfile.anketa.docums" :key="tbl['id']" class="table table-responsive">
        <thead>
          <tr>
            <th  width="25%">{{ `#${tbl['id']}` }}</th>
            <th v-if="!storeProfile.printPdf">
              <a href="#" @click="storeProfile.deleteItem(tbl['id'].toString(), 'document')"
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
            <th v-else></th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Вид документа</td><td>{{ tbl['view'] }}</td></tr>
          <tr><td>Серия</td><td>{{ tbl['series'] }}</td></tr>
          <tr><td>Номер</td><td>{{ tbl['number'] }}</td></tr>
          <tr><td>Кем выдан</td><td>{{ tbl['agency'] }}</td></tr>
          <tr><td>Дата выдачи</td><td>{{ new Date(String(tbl['issue'])).toLocaleDateString('ru-RU') }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
    </template>
      
    <a class="btn btn-link" @click="storeProfile.flag === 'address' ? storeProfile.flag = '' : storeProfile.flag = 'address'; 
                                    storeProfile.flag === 'address' ? storeProfile.action = 'create' : storeProfile.action = ''; 
                                    storeProfile.clearItem" 
                                    :title="storeProfile.flag === 'document' ? 'Закрыть форму' : 'Добавить адрес'">Адрес</a>
    <template v-if="storeProfile.flag === 'address'">
      <AddressForm />
    </template>
    
    <template v-else>
      <table v-if="storeProfile.anketa.addrs && storeProfile.anketa.addrs.length" v-for="tbl in storeProfile.anketa.addrs" :key="tbl['id']" class="table table-responsive">
        <thead>
          <tr>
            <th  width="25%">{{ `#${tbl['id']}` }}</th>
            <th v-if="!storeProfile.printPdf">
              <a href="#" @click="storeProfile.deleteItem(tbl['id'].toString(), 'address')"
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
            <th v-else></th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Тип</td><td>{{ tbl['view'] }}</td></tr>
          <tr><td>Регион</td><td>{{ tbl['region'] }}</td></tr>
          <tr><td>Адрес</td><td>{{ tbl['address'] }}</td></tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
    </template>

    <a class="btn btn-link" @click="storeProfile.flag === 'contact' ? storeProfile.flag = '' : storeProfile.flag = 'contact'; 
                                    storeProfile.flag === 'contact' ? storeProfile.action = 'create' : storeProfile.action = ''; 
                                    storeProfile.clearItem" 
                                    :title="storeProfile.flag === 'contact' ? 'Закрыть форму' : 'Добавить контакт'">Контакты</a>
    <template v-if="storeProfile.flag === 'contact'">
      <ContactForm />
    </template>
    
    <template v-else>
      <table v-if="storeProfile.anketa.conts && storeProfile.anketa.conts.length" v-for="tbl in storeProfile.anketa.conts" :key="tbl['id']" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `#${tbl['id']}` }}</th>
            <th v-if="!storeProfile.printPdf">
              <a href="#" @click="storeProfile.deleteItem(tbl['id'].toString(), 'contact')"
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
            <th v-else></th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Вид</td><td>{{ tbl['view'] }}</td></tr>
          <tr><td>Контакт</td><td>{{ tbl['contact'] }}</td></tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
    </template>

    <a class="btn btn-link" @click="storeProfile.flag === 'workplace' ? storeProfile.flag = '' : storeProfile.flag = 'workplace'; 
                                    storeProfile.flag === 'workplace' ? storeProfile.action = 'create' : storeProfile.action = ''; 
                                    storeProfile.clearItem" 
                                    :title="storeProfile.flag === 'workplace' ? 'Закрыть форму' : 'Добавить работу'">Работа</a>
    <template v-if="storeProfile.flag === 'workplace'">
      <WorkplaceForm />
    </template>
    
    <template v-else>
      <table v-if="storeProfile.anketa.works && storeProfile.anketa.works.length" v-for="tbl in storeProfile.anketa.works" :key="tbl['id']" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `#${tbl['id']}` }}</th>
            <th v-if="!storeProfile.printPdf">
              <a href="#" @click="storeProfile.deleteItem(tbl['id'].toString(), 'workplace')"
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
            <th v-else></th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Период</td>
            <td>{{ tbl['start_date'] }} - {{ tbl['end_date'] }}</td>
          </tr>
          <tr><td>Организация</td><td>{{ tbl['workplace'] }}</td></tr>
          <tr><td>Адрес</td><td>{{ tbl['address'] }}</td></tr>
          <tr><td>Должность</td><td>{{ tbl['position'] }}</td></tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
    </template>

    <a class="btn btn-link" @click="storeProfile.flag === 'relation' ? storeProfile.flag = '' : storeProfile.flag = 'relation'; 
                                    storeProfile.flag === 'relation' ? storeProfile.action = 'create' : storeProfile.action = ''; 
                                    storeProfile.clearItem" 
                                    :title="storeProfile.flag === 'relation' ? 'Закрыть форму' : 'Добавить связь'">Связи</a>
    <template v-if="storeProfile.flag === 'relation'">
      <RelationForm />
    </template>
    
    <template v-else>
      <table v-if="storeProfile.anketa.relate && storeProfile.anketa.relate.length" v-for="tbl in storeProfile.anketa.relate" :key="tbl['id']" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `#${tbl['id']}` }}</th>
            <th v-if="!storeProfile.printPdf">
              <a href="#" @click="storeProfile.deleteItem(tbl['id'].toString(), 'relation')"
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
            <th v-else></th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Тип связи</td><td>{{ tbl['relation'] }}</td></tr>
          <tr>
            <td>Связь</td>
            <td><router-link v-if="tbl['relation_id']" :to="{ name: 'profile', params: {id: String(tbl['relation_id'])} }">
              Связь ID #{{ tbl['relation_id'] }}</router-link></td>
          </tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
    </template>

    <div v-if="!storeProfile.printPdf" class="py-3">
      <div class='btn-group' role="group">
        
        <button @click="storeProfile.sendResume" 
          :disabled="(storeProfile.anketa.resume['status'] !== storeClassify.status['new'] 
            && storeProfile.anketa.resume['status'] !== storeClassify.status['update']) 
            || storeProfile.spinner" 
          class="btn btn-outline-primary">{{ !storeProfile.spinner ? 'Отправить на проверку' : '' }}
          <span v-if="storeProfile.spinner" class="spinner-border spinner-border-sm" aria-hidden="true"></span>
          <span v-if="storeProfile.spinner" role="status">Отправляется...</span>
        </button>
        
        <button type="button" class="btn btn-outline-danger" 
          :disabled="storeProfile.anketa.resume['status'] === storeClassify.status['finish']
            || storeProfile.spinner" 
          @click="storeProfile.deleteItem(storeProfile.anketa.resume['id'], 'person')">Удалить анкету
        </button>

      </div>
    </div>
  
  </div>
</template>