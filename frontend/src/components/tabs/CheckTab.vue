<script setup lang="ts">

import { ref } from 'vue';
import { classifyStore } from '@store/classify';
import { profileStore } from '@/store/profile';
import { fileManagerStore } from '@store/fmanager';
import CheckForm from '@components/forms/CheckForm.vue'

const storeClassify = classifyStore();
const storeProfile = profileStore();
const storeFmanager = fileManagerStore();

const hiddenAddBtn = ref(false);
const hiddenDelBtn = ref(false);
const hiddenEditBtn = ref(false);

hiddenDelBtn.value = storeProfile.profile.resume['status'] 
                    === storeClassify.classifyItems.status['finish'] 
                  || storeProfile.profile.resume['status'] 
                    === storeClassify.classifyItems.status['robot'];

hiddenEditBtn.value = storeProfile.profile.resume['status'] 
                      !== storeClassify.classifyItems.status['save'] 
                    && storeProfile.profile.resume['status'] 
                      !== storeClassify.classifyItems.status['cancel'] 
                    && storeProfile.profile.resume['status'] 
                      !== storeClassify.classifyItems.status['manual']

hiddenAddBtn.value = ![storeClassify.classifyItems.status['new'], 
                      storeClassify.classifyItems.status['update'], 
                      storeClassify.classifyItems.status['save'], 
                      storeClassify.classifyItems.status['repeat']].
                        includes(storeProfile.profile.resume['status'])
</script>

<template>
  <div class="py-3">

    <CheckForm v-if="storeProfile.action === 'update' 
                    && storeProfile.flag === 'check'" />

    <div v-else>
      <div class="accordion" id="accordionCheck" v-if="storeProfile.profile.verification?.length">
        <div class="accordion-item" v-for="tbl, idx in storeProfile.profile.verification" 
                                    :key="tbl['id']" >
          <h6 class="accordion-header">
            <button :class="`accordion-button ${idx !== 0 ? 'collapsed' : ''}`" type="button" data-bs-toggle="collapse" 
                    :data-bs-target="`#collapseCheck${tbl['id']}`">
              {{ `ID #${tbl['id']}` }}
            </button>
          </h6>
          <div :id="`collapseCheck${tbl['id']}`" :class="`accordion-collapse collapse ${idx === 0 ? 'show' : ''}`" 
              data-bs-parent="#accordionCheck">
            <div class="accordion-body">
              <table class="table table-responsive">
                <thead>
                  <tr>
                    <th width="25%">
                      <a :hidden="hiddenDelBtn" href="#" title="Удалить"
                        @click="storeProfile.deleteItem(tbl['id'].toString(), 'check')">
                        <i class="bi bi-trash"></i>
                      </a>
                    </th>
                    <th>                    
                      <a :hidden="hiddenEditBtn" href="#" title="Изменить"
                        @click="storeProfile.openForm('check', 'update', 
                                                        tbl['id'].toString(), tbl)">
                        <i class="bi bi-pencil-square"></i>
                      </a>
                    </th>
                  </tr>
                </thead>      
                <tbody>
                  <tr>
                    <td>Проверка по местам работы</td>
                    <td>{{ tbl['workplace'] ? tbl['workplace'] : 'Данные отсутствуют' }}</td>
                  </tr>
                  <tr>
                    <td>Бывший работник МТСБ</td>
                    <td>{{ tbl['employee'] ? tbl['employee'] : 'Данные отсутствуют' }}</td>
                  </tr>
                  <tr>
                    <td>Проверка паспорта</td>
                    <td>{{ tbl['document'] ? tbl['document'] : 'Данные отсутствуют' }}</td>
                  </tr>
                  <tr>
                    <td>Проверка ИНН</td>
                    <td>{{ tbl['inn'] ? tbl['inn'] : 'Данные отсутствуют' }}</td>
                  </tr>
                  <tr>
                    <td>Проверка ФССП</td>
                    <td>{{ tbl['debt'] ? tbl['debt'] : 'Данные отсутствуют' }}</td>
                  </tr>
                  <tr>
                    <td>Проверка банкротства</td>
                    <td>{{ tbl['bankruptcy'] ? tbl['bankruptcy'] : 'Данные отсутствуют' }}</td>
                  </tr>
                  <tr>
                    <td>Проверка БКИ</td>
                    <td>{{ tbl['bki'] ? tbl['bki'] : 'Данные отсутствуют' }}</td>
                  </tr>
                  <tr>
                    <td>Проверка судебных дел</td>
                    <td>{{ tbl['courts'] ? tbl['courts'] : 'Данные отсутствуют' }}</td>
                  </tr>
                  <tr>
                    <td>Проверка аффилированности</td>
                    <td>{{ tbl['affiliation'] ? tbl['affiliation'] : 'Данные отсутствуют' }}</td>
                  </tr>
                  <tr>
                    <td>Проверка по списку террористов</td>
                    <td>{{ tbl['terrorist'] ? tbl['terrorist'] : 'Данные отсутствуют' }}</td>
                  </tr>
                  <tr>
                    <td>Проверка нахождения в розыске</td>
                    <td>{{ tbl['mvd'] ? tbl['mvd'] : 'Данные отсутствуют' }}</td>
                  </tr>
                  <tr>
                    <td>Проверка в открытых источниках</td>
                    <td>{{ tbl['internet'] ? tbl['internet'] : 'Данные отсутствуют' }}</td>
                  </tr>
                  <tr>
                    <td>Проверка Кронос</td>
                    <td>{{ tbl['cronos'] ? tbl['cronos'] : 'Данные отсутствуют' }}</td>
                  </tr>
                  <tr>
                    <td>Проверка Крос</td>
                    <td>{{ tbl['cros'] ? tbl['cros'] : 'Данные отсутствуют' }}</td>
                  </tr>
                  <tr>
                    <td>Дополнительная информация</td>
                    <td>{{ tbl['addition'] ? tbl['addition'] : 'Данные отсутствуют' }}</td>
                  </tr>
                  <tr v-if="tbl['path']">
                    <td>Материалы проверки</td>
                    <td>
                      <router-link @click="storeFmanager.fileManager.path = tbl['path'].split('/')" 
                                  :to="{ name: 'manager',  params: { group: 'staffsec' } }">
                      
                        {{ storeProfile.profile.resume['path'] }}
                      </router-link>
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
                      <a href="#" @click="storeProfile.getItem('check', 'self', tbl['id'].toString())">
                        {{ tbl['officer'] }}</a>
                    </td>
                  </tr>
                  <tr v-if="tbl['deadline']">
                    <td>Дата</td>
                    <td>{{ new Date(String(tbl['deadline'])).toLocaleDateString('ru-RU') }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
      <p v-else >Данные отсутствуют</p>
      <div class="py-3">
        <button class="btn btn-outline-primary" 
                @click="storeProfile.getItem('check', 'add')" 
                :disabled="hiddenAddBtn">Добавить проверку
        </button>
      </div>
    </div>
  </div>
</template>