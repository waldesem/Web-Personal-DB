<script setup lang="ts">
/* Компонент анкеты */

import { appAnketa } from '@/store/anketa';
import { appProfile } from '@/store/profile';
import { appLocation } from '@/store/location';
import { appClassify } from '@/store/classify';
import ResumeForm from '@content/forms/ResumeForm.vue';
import RegionForm from '@content/forms/RegionForm.vue';
import StaffForm from '@content/forms/StaffForm.vue';
import DocumentForm from '@content/forms/DocumentForm.vue';
import AddressForm from '@content/forms/AddressForm.vue';
import ContactForm from '@content/forms/ContactForm.vue';
import RelationForm from '@content/forms/RelationForm.vue';
import WorkplaceForm from '@content/forms/WorkplaceForm.vue';

const storeAnketa = appAnketa();

const storeProfile = appProfile();

const storeLocation = appLocation();

const storeClassify = appClassify();

</script>

<template>
  <div class="p-3">
  
    <template v-if="storeAnketa.flag === 'resume'" >
      <ResumeForm />
    </template>

    <template v-else>
      <RegionForm />
      <table v-if="storeProfile.anketa.resume" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `ID #${storeProfile.anketa.resume['id']}` }}</th>
            <th>
              <a href="#" @click="storeAnketa.flag = 'resume'; storeAnketa.action = 'update'" title="Изменить">
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
              <a href="#" @click="storeAnketa.flag = 'location'; storeAnketa.action = 'update'; 
                                                                storeAnketa.itemId = storeProfile.anketa.resume['id']" 
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
            <td><a href="#" @click="storeAnketa.updateStatus">{{ storeProfile.anketa.resume['status'] }}</a></td>
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
        
    <a class="btn btn-link" @click="storeAnketa.flag === 'staff' ? storeAnketa.flag = '' : storeAnketa.flag = 'staff'; 
                                    storeAnketa.flag === 'staff' ? storeAnketa.action = 'create' : storeAnketa.action = ''; 
                                    storeAnketa.clearItem" 
                                    :title="storeAnketa.flag === 'staff' ? 'Закрыть окно' : 'Добавить должность'">Должности</a>
    <template v-if="storeAnketa.flag === 'staff'">
      <StaffForm />
    </template>

    <template v-else>
      <table v-if="storeProfile.anketa.staffs && storeProfile.anketa.staffs.length" v-for="tbl in storeProfile.anketa.staffs" :key="tbl['id' as keyof typeof tbl]" class="table table-responsive">
        <thead>
          <tr>
            <th  width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
            <th>
              <a href="#" @click="storeProfile.deleteItem(tbl['id' as keyof typeof tbl].toString(), 'staff')" title="Удалить">
                <i class="bi bi-trash"></i>
              </a>
              &nbsp;
              <a class="btn btn-link" @click= "storeAnketa.flag = 'staff'; 
                                      storeAnketa.action = 'update'; 
                                      storeAnketa.itemId = tbl['id' as keyof typeof tbl].toString(); 
                                      storeAnketa.itemForm = tbl" title="Изменить">
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


    <a class="btn btn-link" @click="storeAnketa.flag === 'document' ? storeAnketa.flag = '' : storeAnketa.flag = 'document'; 
                                    storeAnketa.flag === 'document' ? storeAnketa.action = 'create' : storeAnketa.action = ''; 
                                    storeAnketa.clearItem" 
                                    :title="storeAnketa.flag === 'document' ? 'Закрыть окно' : 'Добавить документ'">Документы</a>
    <template v-if="storeAnketa.flag === 'document'">
      <DocumentForm />
    </template>
    
    <template v-else>
      <table v-if="storeProfile.anketa.docums && storeProfile.anketa.docums.length" v-for="tbl in storeProfile.anketa.docums" :key="tbl['id' as keyof typeof tbl]" class="table table-responsive">
        <thead>
          <tr>
            <th  width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
            <th>
              <a href="#" @click="storeProfile.deleteItem(tbl['id' as keyof typeof tbl].toString(), 'document')"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Удалить">
                          <i class="bi bi-trash"></i></a>
              &nbsp;
              <a class="btn btn-link" @click= "storeAnketa.flag = 'document'; 
                                      storeAnketa.action = 'update'; 
                                      storeAnketa.itemId = tbl['id' as keyof typeof tbl].toString(); 
                                      storeAnketa.itemForm = tbl" title="Изменить">
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
      
    <a class="btn btn-link" @click="storeAnketa.flag === 'address' ? storeAnketa.flag = '' : storeAnketa.flag = 'address'; 
                                    storeAnketa.flag === 'address' ? storeAnketa.action = 'create' : storeAnketa.action = ''; 
                                    storeAnketa.clearItem" 
                                    :title="storeAnketa.flag === 'document' ? 'Закрыть окно' : 'Добавить адрес'">Адрес</a>
    <template v-if="storeAnketa.flag === 'address'">
      <AddressForm />
    </template>
    
    <template v-else>
      <table v-if="storeProfile.anketa.addrs && storeProfile.anketa.addrs.length" v-for="tbl in storeProfile.anketa.addrs" :key="tbl['id' as keyof typeof tbl]" class="table table-responsive">
        <thead>
          <tr>
            <th  width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
            <th>
              <a href="#" @click="storeProfile.deleteItem(tbl['id' as keyof typeof tbl].toString(), 'address')"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Удалить">
                          <i class="bi bi-trash"></i></a>
              &nbsp;
              <a class="btn btn-link" @click= "storeAnketa.flag = 'address'; 
                                      storeAnketa.action = 'update'; 
                                      storeAnketa.itemId = tbl['id' as keyof typeof tbl].toString(); 
                                      storeAnketa.itemForm = tbl" title="Изменить">
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

    <a class="btn btn-link" @click="storeAnketa.flag === 'contact' ? storeAnketa.flag = '' : storeAnketa.flag = 'contact'; 
                                    storeAnketa.flag === 'contact' ? storeAnketa.action = 'create' : storeAnketa.action = ''; 
                                    storeAnketa.clearItem" 
                                    :title="storeAnketa.flag === 'contact' ? 'Закрыть окно' : 'Добавить контакт'">Контакты</a>
    <template v-if="storeAnketa.flag === 'contact'">
      <ContactForm />
    </template>
    
    <template v-else>
      <table v-if="storeProfile.anketa.conts && storeProfile.anketa.conts.length" v-for="tbl in storeProfile.anketa.conts" :key="tbl['id' as keyof typeof tbl]" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
            <th>
              <a href="#" @click="storeProfile.deleteItem(tbl['id' as keyof typeof tbl].toString(), 'contact')"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Удалить">
                          <i class="bi bi-trash"></i></a>
              &nbsp;
              <a class="btn btn-link" @click= "storeAnketa.flag = 'contact'; 
                                      storeAnketa.action = 'update'; 
                                      storeAnketa.itemId = tbl['id' as keyof typeof tbl].toString(); 
                                      storeAnketa.itemForm = tbl" title="Изменить">
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

    <a class="btn btn-link" @click="storeAnketa.flag === 'workplace' ? storeAnketa.flag = '' : storeAnketa.flag = 'workplace'; 
                                    storeAnketa.flag === 'workplace' ? storeAnketa.action = 'create' : storeAnketa.action = ''; 
                                    storeAnketa.clearItem" 
                                    :title="storeAnketa.flag === 'workplace' ? 'Закрыть окно' : 'Добавить работу'">Работа</a>
    <template v-if="storeAnketa.flag === 'workplace'">
      <WorkplaceForm />
    </template>
    
    <template v-else>
      <table v-if="storeProfile.anketa.works && storeProfile.anketa.works.length" v-for="tbl in storeProfile.anketa.works" :key="tbl['id' as keyof typeof tbl]" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
            <th>
              <a href="#" @click="storeProfile.deleteItem(tbl['id' as keyof typeof tbl].toString(), 'workplace')"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Удалить">
                          <i class="bi bi-trash"></i></a>
              &nbsp;
              <a class="btn btn-link" @click= "storeAnketa.flag = 'workplace'; 
                                      storeAnketa.action = 'update'; 
                                      storeAnketa.itemId = tbl['id' as keyof typeof tbl].toString(); 
                                      storeAnketa.itemForm = tbl" title="Изменить">
                <i class="bi bi-pencil-square"></i>
              </a>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Период</td>
            <td>{{ tbl['start_date' as keyof typeof tbl] }} - {{ tbl['end_date' as keyof typeof tbl] }}</td>
          </tr>
          <tr><td>Организация</td><td>{{ tbl['workplace' as keyof typeof tbl] }}</td></tr>
          <tr><td>Адрес</td><td>{{ tbl['address' as keyof typeof tbl] }}</td></tr>
          <tr><td>Должность</td><td>{{ tbl['position' as keyof typeof tbl] }}</td></tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
    </template>

    <a class="btn btn-link" @click="storeAnketa.flag === 'relation' ? storeAnketa.flag = '' : storeAnketa.flag = 'relation'; 
                                    storeAnketa.flag === 'relation' ? storeAnketa.action = 'create' : storeAnketa.action = ''; 
                                    storeAnketa.clearItem" 
                                    :title="storeAnketa.flag === 'relation' ? 'Закрыть окно' : 'Добавить связь'">Связи</a>
    <template v-if="storeAnketa.flag === 'relation'">
      <RelationForm />
    </template>
    
    <template v-else>
      <table v-if="storeProfile.anketa.relate && storeProfile.anketa.relate.length" v-for="tbl in storeProfile.anketa.relate" :key="tbl['id' as keyof typeof tbl]" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
            <th>
              <a href="#" @click="storeProfile.deleteItem(tbl['id' as keyof typeof tbl].toString(), 'relation')"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Удалить">
                          <i class="bi bi-trash"></i></a>
              &nbsp;
              <a class="btn btn-link" @click= "storeAnketa.flag = 'relation'; 
                                      storeAnketa.action = 'update'; 
                                      storeAnketa.itemId = tbl['id' as keyof typeof tbl].toString(); 
                                      storeAnketa.itemForm = tbl" title="Изменить">
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
      <button @click="storeAnketa.sendResume" 
        :disabled="storeClassify.status 
        && (storeProfile.anketa.resume['status'] !== storeClassify.status['new'] 
        && storeProfile.anketa.resume['status'] !== storeClassify.status['update'])" 
        class="btn btn-outline-primary">Отправить на проверку
      </button>
    </div>
  
  </div>
</template>