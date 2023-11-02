<script setup lang="ts">

import { profileStore } from '@/store/profile';
import { classifyStore } from '@/store/classify';
import HeaderDiv from '@components/layouts/HeaderDiv.vue';

const storeProfile = profileStore();
const storeClassify = classifyStore();

</script>

<template>
  <div class="conrainer">

    <div class="text-secondary text-end text-opacity-85 py-3">
      <h6>Для служебного пользования</h6>
    </div>
    <div class="card" style="width: 16rem;">
      <img :src="storeProfile.urlImage 
            ? storeProfile.urlImage 
            : '/no-photo.png'" 
            style="width: 100%; height: auto;" 
            class="card-img-top" alt="...">
    </div>
    <HeaderDiv :page-header="storeProfile.profile.resume['fullname']" />
    <div class="fs-5 text-secondary text-end text-opacity-85">
      <p v-if="storeProfile.profile.staffs[0]['position']">
        {{ storeProfile.profile.staffs[0]['position'] }}
      </p>
      <p v-if="storeProfile.profile.staffs[0]['department']">
        {{ storeProfile.profile.staffs[0]['department'] }}
      </p>
    </div>
    <div class="text-primary text-opacity-85 py-3">
      <h5>Анкета</h5>
    </div>
    <div>
      <table v-if="storeProfile.profile.resume" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `ID #${storeProfile.profile.resume['id']}` }}</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="storeProfile.profile.resume['region_id']">
            <td>Регион</td>
            <td>
              {{ storeClassify.classifyItems.regions[storeProfile.profile.resume['region_id']]}}
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
          <tr v-if="storeProfile.profile.resume['birthplace']">
            <td>Место рождения</td>
            <td>{{ storeProfile.profile.resume['birthplace'] }}</td>
          </tr>
          <tr v-if="storeProfile.profile.resume['country']">
            <td>Гражданство</td>
            <td>{{ storeProfile.profile.resume['country'] }}</td>
          </tr>
          <tr v-if="storeProfile.profile.resume['snils']">
            <td>СНИЛС</td>
            <td>{{ storeProfile.profile.resume['snils'] }}</td>
          </tr>
          <tr v-if="storeProfile.profile.resume['inn']">
            <td>ИНН</td>
            <td>{{ storeProfile.profile.resume['inn'] }}</td>
          </tr>
          <tr v-if="storeProfile.profile.resume['education']">
            <td>Образование</td>
            <td>{{ storeProfile.profile.resume['education'] }}</td>
          </tr>
          <tr v-if="storeProfile.profile.resume['addition']">
            <td>Дополнительная информация</td>
            <td>{{ storeProfile.profile.resume['addition'] }}</td>
          </tr>
          <tr v-if="storeProfile.profile.resume['update']">
            <td>Обновлен</td>
            <td>{{ new Date(String(storeProfile.profile.resume['update'])).
                  toLocaleDateString('ru-RU') }}</td>
          </tr>
          <tr v-else>
            <td>Создан</td>
            <td>{{ new Date(String(storeProfile.profile.resume['create'])).
                  toLocaleDateString('ru-RU') }}</td>
          </tr>
        </tbody>
      </table>

      <div class="text-primary text-opacity-85 py-3">
        <h6>Документы</h6>
      </div>
      <table v-if="storeProfile.profile.docums && storeProfile.profile.docums.length" 
             v-for="tbl in storeProfile.profile.docums" 
             :key="tbl['id']" class="table table-responsive">
        <thead>
          <tr><th width="25%">{{ `#${tbl['id']}` }}</th><th></th></tr>
        </thead>
        <tbody>
          <tr v-if="tbl['view']"><td>Вид документа</td><td>{{ tbl['view'] }}</td></tr>
          <tr v-if="tbl['series']"><td>Серия</td><td>{{ tbl['series'] }}</td></tr>
          <tr v-if="tbl['number']"><td>Номер</td><td>{{ tbl['number'] }}</td></tr>
          <tr v-if="tbl['agency']"><td>Кем выдан</td><td>{{ tbl['agency'] }}</td></tr>
          <tr v-if="tbl['issue']">
            <td>Дата выдачи</td>
            <td>{{ new Date(String(tbl['issue'])).
                                        toLocaleDateString('ru-RU') }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>

      <div class="text-primary text-opacity-85 py-3">
        <h6>Адрреса</h6>
      </div>
      <table v-if="storeProfile.profile.addrs && storeProfile.profile.addrs.length" 
             v-for="tbl in storeProfile.profile.addrs" 
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
      <table v-if="storeProfile.profile.conts && storeProfile.profile.conts.length" 
             v-for="tbl in storeProfile.profile.conts" :key="tbl['id']" 
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
      <table v-if="storeProfile.profile.works && storeProfile.profile.works.length" 
             v-for="tbl in storeProfile.profile.works" 
              :key="tbl['id']" class="table table-responsive">
        <thead>
          <tr><th width="25%">{{ `#${tbl['id']}` }}</th><th></th></tr>
        </thead>
        <tbody>
          <tr>
            <td>Период</td><td>{{ tbl['start_date'] }} - {{ tbl['end_date'] }}</td></tr>
          <tr>
            <td>Работает по н.в.</td><td>{{ tbl['now_work'] ? 'Работает' : 'Не работает' }}</td>
          </tr>
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
      <table v-if="storeProfile.profile.relate && storeProfile.profile.relate.length" 
             v-for="tbl in storeProfile.profile.relate" 
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
      <table v-if="storeProfile.profile.verification?.length" 
             v-for="tbl in storeProfile.profile.verification" 
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
          <tr v-if="tbl['addition']">
            <td>Дополнительная информация</td>
            <td>{{ tbl['addition']}}</td>
          </tr>
          <tr v-if="tbl['path']">
            <td>Материалы проверки</td>
            <td>
              <a :href="'file://' + tbl['path']" target="_blank">
                {{ tbl['path'] }}
              </a>
            </td>
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
            <td>
              <a href="#" @click="storeProfile.getItem('check', 'self', tbl['id' as keyof typeof tbl].toString())">
                {{ tbl['officer'] }}</a>
            </td>
          </tr>
          <tr v-if="tbl['deadline']">
            <td>Дата</td>
            <td>{{ new Date(String(tbl['deadline'])).toLocaleDateString('ru-RU') }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
    </div>

    <div class="text-primary text-opacity-85 py-3">
      <h5>Согласования</h5>
    </div>
    <div>
      <table v-if="storeProfile.profile.register.length" 
             v-for="tbl in storeProfile.profile.register" 
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
      <table v-if="storeProfile.profile.pfo.length" 
             v-for="tbl in storeProfile.profile.pfo" 
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
          <tr v-if="tbl['path']">
            <td>Ссылка</td>
            <td>
              <a :href="'file://' + tbl['path']" target="_blank">
                {{ tbl['path'] }}
              </a>
            </td>
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
          <tr>
            <td colspan="2">
              <form class="form" enctype="multipart/form-data" role="form" 
                    @change="storeProfile.submitFile($event, 'poligraf', tbl['id'].toString())">
                <input class="form-control" id="file" type="file" ref="file" multiple>
              </form>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="text-primary text-opacity-85 py-3">
      <h5>Расследования</h5>
    </div>
    <div>
      <table v-if="storeProfile.profile.inquisition?.length" 
             v-for="tbl in storeProfile.profile.inquisition" 
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
          <tr v-if="tbl['path']">
            <td>Ссылка</td>
            <td>
              <a :href="'file://' + tbl['path']" target="_blank">
                {{ tbl['path'] }}
              </a>
            </td>
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
      <table class="table table-responsive" v-for="tbl in storeProfile.profile.needs" 
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