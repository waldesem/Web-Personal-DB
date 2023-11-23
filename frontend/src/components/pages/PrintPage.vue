<script setup lang="ts">

import { defineAsyncComponent } from 'vue';
import { profileStore } from '@/store/profile';
import { classifyStore } from '@/store/classify';

const HeaderDiv = defineAsyncComponent(() => import('@components/layouts/HeaderDiv.vue'));
const RowDiv = defineAsyncComponent(() => import('@components/elements/RowDiv.vue'));

const storeProfile = profileStore();
const storeClassify = classifyStore();

</script>

<template>
  <div class="container">

    <div class="text-secondary text-end text-opacity-85 py-3">
      <h6>Для служебного пользования</h6>
    </div>
    <div class="card" style="width: 16rem;">
      <img :src="storeProfile.dataProfile.url 
            ? storeProfile.dataProfile.url 
            : '/no-photo.png'" 
            style="width: 100%; height: auto;" 
            class="card-img-top" alt="...">
    </div>
    <HeaderDiv :page-header="storeProfile.dataProfile.resume['fullname']" />
    <div class="fs-4 text-secondary text-opacity-95">
      <p v-if="storeProfile.dataProfile.staffs[0]['position']">
        {{ storeProfile.dataProfile.staffs[0]['position'] }}
      </p>
      <p v-if="storeProfile.dataProfile.staffs[0]['department']">
        {{ storeProfile.dataProfile.staffs[0]['department'] }}
      </p>
    </div>
    <div class="text-primary text-opacity-85 py-3">
      <h5>Анкета</h5>
    </div>
    <div>
      <div v-if="storeProfile.dataProfile.resume" class="d-flex justify-content-start">
        <RowDiv :label="'ID'" 
                :value="storeProfile.dataProfile.resume['id']"/>
        <RowDiv v-if="storeProfile.dataProfile.resume['region_id']"
                :label="'Регион'"
                :value="storeClassify.classData.regions[storeProfile.dataProfile.resume['region_id']]"/>
        <RowDiv :label="'Фамилия Имя Отчество'"
                :value="storeProfile.dataProfile.resume['fullname']"/>
        <RowDiv v-if="storeProfile.dataProfile.resume['previous']"
                :label="'Изменение имени'"
                :value="storeProfile.dataProfile.resume['previous']"/>
        <RowDiv :label="'Дата рождения'"
                :value="storeProfile.dataProfile.resume['birthday']"/>
        <RowDiv v-if="storeProfile.dataProfile.resume['birthplace']"
                :label="'Место рождения'"
                :value="storeProfile.dataProfile.resume['birthplace']"/>
        <RowDiv v-if="storeProfile.dataProfile.resume['country']"
                :label="'Гражданство'"
                :value="storeProfile.dataProfile.resume['country']"/>
        <RowDiv v-if="storeProfile.dataProfile.resume['snils']"
                :label="'СНИЛС'"
                :value="storeProfile.dataProfile.resume['snils']"/>
        <RowDiv v-if="storeProfile.dataProfile.resume['inn']"
                :label="'ИНН'"
                :value="storeProfile.dataProfile.resume['inn']"/>
        <RowDiv v-if="storeProfile.dataProfile.resume['education']"
                :label="'Образование'"
                :value="storeProfile.dataProfile.resume['education']"/>
        <RowDiv v-if="storeProfile.dataProfile.resume['addition']"
                :label="'Дополнительная информация'"
                :value="storeProfile.dataProfile.resume['addition']"/>
        <RowDiv v-if="storeProfile.dataProfile.resume['update']"
                :label="'Обновлен'"
                :value="new Date(String(storeProfile.dataProfile.resume['update'])).
                        toLocaleDateString('ru-RU')"/>
        <RowDiv v-else
                :label="'Создан'"
                :value="new Date(String(storeProfile.dataProfile.resume['create'])).
                        toLocaleDateString('ru-RU')"/>
      </div>

      <div class="text-primary text-opacity-85 py-3">
        <h6>Документы</h6>
      </div>
      <div v-if="storeProfile.dataProfile.docums && storeProfile.dataProfile.docums.length" 
             v-for="tbl in storeProfile.dataProfile.docums" 
                    :key="tbl['id']" 
                    class="d-flex justify-content-start">
        <RowDiv :label="'#'"
                    :value="tbl['id']"/>
        <RowDiv v-if="tbl['view']"
                    :label="'Вид документа'"
                    :value="tbl['view']"/>
        <RowDiv v-if="tbl['series']"
                    :label="'Серия'"
                    :value="tbl['series']"/>
        <RowDiv v-if="tbl['number']"
                    :label="'Номер'"
                    :value="tbl['number']"/>
        <RowDiv v-if="tbl['agency']"
                    :label="'Кем выдан'"
                    :value="tbl['agency']"/>
        <RowDiv v-if="tbl['issue']"
                    :label="'Дата выдачи'"
                    :value="new Date(String(tbl['issue'])).
                              toLocaleDateString('ru-RU')"/>
      </div>
      <p v-else >Данные отсутствуют</p>

      <div class="text-primary text-opacity-85 py-3">
        <h6>Адрреса</h6>
      </div>
      <table v-if="storeProfile.dataProfile.addrs && storeProfile.dataProfile.addrs.length" 
             v-for="tbl in storeProfile.dataProfile.addrs" 
              :key="tbl['id']" class="table table-responsive">
        <thead>
          <tr><th width="25%">{{ `#${tbl['id']}` }}</th><th></th></tr>
        </thead>
        <tbody>
          <tr v-if="tbl['view']"><td>Тип</td><td>{{ tbl['view'] }}</td></tr>
          <tr v-if="tbl['region']"><td>Регион</td><td>{{ tbl['region'] }}</td></tr>
          <tr v-if="tbl['address']"><td>Адрес</td><td>{{ tbl['address'] }}</td></tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>

      <div class="text-primary text-opacity-85 py-3">
        <h6>Контакты</h6>
      </div>
      <table v-if="storeProfile.dataProfile.conts && storeProfile.dataProfile.conts.length" 
             v-for="tbl in storeProfile.dataProfile.conts" :key="tbl['id']" 
                class="table table-responsive">
        <thead>
          <tr><th width="25%">{{ `#${tbl['id']}` }}</th><th></th></tr>
        </thead>
        <tbody>
          <tr v-if="tbl['view']"><td>Вид</td><td>{{ tbl['view'] }}</td></tr>
          <tr v-if="tbl['contact']"><td>Контакт</td><td>{{ tbl['contact'] }}</td></tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
      
      <div class="text-primary text-opacity-85 py-3">
        <h6>Место работы</h6>
      </div>
      <table v-if="storeProfile.dataProfile.works && storeProfile.dataProfile.works.length" 
             v-for="tbl in storeProfile.dataProfile.works" 
              :key="tbl['id']" class="table table-responsive">
        <thead>
          <tr><th width="25%">{{ `#${tbl['id']}` }}</th><th></th></tr>
        </thead>
        <tbody>
          <tr>
            <td>Период</td><td>{{ tbl['start_date'] }} - {{ tbl['end_date'] }}</td></tr>
          <tr v-if="tbl['workplace']">
            <td>Организация</td><td>{{ tbl['workplace'] }}</td>
          </tr>
          <tr v-if="tbl['address']">
            <td>Адрес</td><td>{{ tbl['address'] }}</td>
          </tr>
          <tr v-if="tbl['position']">
            <td>Должность</td><td>{{ tbl['position'] }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>

      <div class="text-primary text-opacity-85 py-3">
        <h6>Связи</h6>
      </div>
      <table v-if="storeProfile.dataProfile.relate && storeProfile.dataProfile.relate.length" 
             v-for="tbl in storeProfile.dataProfile.relate" 
              :key="tbl['id']" class="table table-responsive">
        <thead>
          <tr><th width="25%">{{ `#${tbl['id']}` }}</th><th></th></tr>
        </thead>
        <tbody>
          <tr><td>Тип связи</td><td>{{ tbl['relation'] }}</td></tr>
          <tr v-if="tbl['relation_id']">
            <td>Связь</td><td>ID #{{ tbl['relation_id'] }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="text-primary text-opacity-85 py-3">
      <h5>Проверки</h5>
    </div>
    <div>
      <table v-if="storeProfile.dataProfile.verification?.length" 
             v-for="tbl in storeProfile.dataProfile.verification" 
              :key="tbl['id']" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th><th></th>
          </tr>
        </thead>   
        <tbody>
          <tr v-if="tbl['workplace']">
            <td>Проверка по местам работы</td>
            <td>{{ tbl['workplace'] }}</td>
          </tr>
          <tr v-if="tbl['employee']">
            <td>Бывший работник МТСБ</td>
            <td>{{ tbl['employee'] }}</td>
          </tr>
          <tr v-if="tbl['document']">
            <td>Проверка паспорта</td>
            <td>{{ tbl['document'] }}</td>
          </tr>
          <tr v-if="tbl['inn']">
            <td>Проверка ИНН</td>
            <td>{{ tbl['inn'] }}</td>
          </tr>
          <tr v-if="tbl['debt']">
            <td>Проверка ФССП</td>
            <td>{{ tbl['debt'] }}</td>
          </tr>
          <tr v-if="tbl['bankruptcy']">
            <td>Проверка банкротства</td>
            <td>{{ tbl['bankruptcy'] }}</td>
          </tr>
          <tr v-if="tbl['bki']">
            <td>Проверка БКИ</td>
            <td>{{ tbl['bki'] }}</td>
          </tr>
          <tr v-if="tbl['courts']">
            <td>Проверка судебных дел</td>
            <td>{{ tbl['courts'] }}</td>
          </tr>
          <tr v-if="tbl['affiliation']">
            <td>Проверка аффилированности</td>
            <td>{{ tbl['affiliation'] }}</td>
          </tr>
          <tr v-if="tbl['terrorist']">
            <td>Проверка по списку террористов</td>
            <td>{{ tbl['terrorist'] }}</td>
          </tr>
          <tr v-if="tbl['mvd']">
            <td>Проверка нахождения в розыске</td>
            <td>{{ tbl['mvd'] }}</td>
          </tr>
          <tr  v-if="tbl['internet']">
            <td>Проверка в открытых источниках</td>
            <td>{{ tbl['internet'] }}</td>
          </tr>
          <tr v-if="tbl['cronos']">
            <td>Проверка Кронос</td>
            <td>{{ tbl['cronos'] }}</td>
          </tr>
          <tr v-if="tbl['cros']">
            <td>Проверка Крос</td>
            <td>{{ tbl['cros'] }}</td>
          </tr>
          <tr>
            <td>ПФО</td>
            <td>{{ tbl['pfo'] ? "Назначено" : "Не назначено" }}</td>
          </tr>
          <tr v-if="tbl['comments']">
            <td>Комментарии</td>
            <td>{{ tbl['comments'] }}</td>
          </tr>
          <tr v-if="tbl['conclusion']">
            <td>Результат проверки</td>
            <td>{{ tbl['conclusion'] }}</td>
          </tr>
          <tr v-if="tbl['officer']">
            <td>Сотрудник</td>
            <td>{{ tbl['officer'] }}</td>
          </tr>
          <tr v-if="tbl['deadline']">
            <td>Дата</td>
            <td>{{ new Date(String(tbl['deadline'])).toLocaleDateString('ru-RU') }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="text-primary text-opacity-85 py-3">
      <h5>Согласования</h5>
    </div>
    <div>
      <table v-if="storeProfile.dataProfile.register.length" 
             v-for="tbl in storeProfile.dataProfile.register" 
              :key="tbl['id']" class="table table-responsive">
        <thead>
          <tr><th width="25%">{{ tbl['id'] }}</th><th></th></tr>
        </thead>
        <tbody>
          <tr v-if="tbl['comments']">
            <td>Комментарий</td>
            <td>{{ tbl['comments'] }}</td>
          </tr>
          <tr v-if="tbl['decision']">
            <td>Решение</td>
            <td>{{ tbl['decision'] }}</td>
          </tr>
          <tr v-if="tbl['supervisor']">
            <td>Согласующий</td>
            <td>{{ tbl['supervisor'] }}</td>
          </tr>
          <tr>
            <td>Дата</td>
            <td>{{ tbl['deadline'] ? new Date(tbl['deadline']).toLocaleDateString('ru-RU') : '' }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="text-primary text-opacity-85 py-3">
      <h5>Полиграф</h5>
    </div>
    <div>
      <table v-if="storeProfile.dataProfile.pfo.length" 
             v-for="tbl in storeProfile.dataProfile.pfo" 
              :key="tbl['id' as keyof typeof tbl]" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th><th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="tbl['theme']">
            <td>Тема</td>
            <td>{{ tbl['theme'] }}</td>
          </tr>
          <tr v-if="tbl['results']">
            <td>Результат</td>
            <td>{{ tbl['results'] }}</td>
          </tr>
          <tr>
            <td>Полиграфолог</td>
            <td>{{ tbl['officer'] ? tbl['officer'] : 'Данные отсуствуют' }}</td>
          </tr>
          <tr v-if="tbl['deadline']">
            <td>Дата</td>
            <td>{{new Date(String(tbl['deadline'])).
              toLocaleDateString('ru-RU') }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="text-primary text-opacity-85 py-3">
      <h5>Расследования</h5>
    </div>
    <div>
      <table v-if="storeProfile.dataProfile.inquisition?.length" 
             v-for="tbl in storeProfile.dataProfile.inquisition" 
              :key="tbl['id']" class="table table-responsive">
        <thead>
          <tr><th width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th><th></th></tr>
        </thead>
        <tbody>
          <tr v-if="tbl['theme']">
            <td>Тема</td>
            <td>{{ tbl['theme'] }}</td>
          </tr>
          <tr v-if="tbl['info']">
            <td>Информация</td>
            <td>{{ tbl['info'] }}</td>
          </tr>
          <tr v-if="tbl['officer']">
            <td>Сотрудник</td>
            <td>{{ tbl['officer'] }}</td>
          </tr>
          <tr v-if="tbl['deadline']">
            <td>Дата</td>
            <td>{{ tbl['deadline'] ? new Date(String(tbl['deadline'])).
              toLocaleDateString('ru-RU') : 'Данные отсутствуют' }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="text-primary text-opacity-85 py-3">
      <h5>Запросы</h5>
    </div>
    <div>
      <table class="table table-responsive" v-for="tbl in storeProfile.dataProfile.needs" 
                                            :key="tbl['id' as keyof typeof tbl]" >
        <thead>
          <tr><th width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th><th></th></tr>
        </thead>        
        <tbody>
          <tr v-if="tbl['info']">
            <td>Информация</td>
            <td>{{ tbl['info'] }}</td>
          </tr>
          <tr v-if="tbl['initiator']">
            <td>Иннициатор</td>
            <td>{{ tbl['initiator'] }}</td>
          </tr>
          <tr v-if="tbl['source']">
            <td>Источник</td>
            <td>{{ tbl['source'] }}</td>
          </tr>
          <tr v-if="tbl['officer']">
            <td>Сотрудник</td>
            <td>{{ tbl['officer'] }}</td>
          </tr>
          <tr v-if="tbl['deadline']">
            <td>Дата запроса</td>
            <td>{{tbl['deadline'] ? new Date(String(tbl['deadline'])).
              toLocaleDateString('ru-RU') : 'Данные отсутствуют' }}</td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>