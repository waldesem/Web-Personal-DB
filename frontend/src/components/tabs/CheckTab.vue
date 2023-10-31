<script setup lang="ts">

import { classifyStore } from '@store/classify';
import { profileStore } from '@/store/profile';
import CheckForm from '@components/forms/CheckForm.vue'

const storeClassify = classifyStore();
const storeProfile = profileStore();

</script>

<template>
  <div class="py-3">

    <CheckForm v-if="storeProfile.action === 'update' && storeProfile.flag === 'check'" />

    <div v-else>
      <table v-if="storeProfile.profile.verification?.length" 
             v-for="tbl in storeProfile.profile.verification" 
              :key="tbl['id']" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
            <th>
              <a href="#" :hidden="storeProfile.profile.resume['status'] === storeClassify.classifyItems.status['finish'] 
                                || storeProfile.profile.resume['status'] === storeClassify.classifyItems.status['robot']"
                          @click="storeProfile.deleteItem(
                            'check', 'delete', tbl['id' as keyof typeof tbl].toString()
                            )"
                           title="Удалить">
                          <i class="bi bi-trash"></i></a>
                          &nbsp;
              <a href="#" :hidden="storeProfile.profile.resume['status'] !== storeClassify.classifyItems.status['save'] 
                                  && storeProfile.profile.resume['status'] !== storeClassify.classifyItems.status['cancel'] 
                                  && storeProfile.profile.resume['status'] !== storeClassify.classifyItems.status['manual']" 
                          @click="storeProfile.action = 'update'; 
                                  storeProfile.flag = 'check';
                                  storeProfile.itemId = tbl['id' as keyof typeof tbl].toString(); 
                                  storeProfile.itemForm = tbl"
                          title="Изменить" >
                          <i class="bi bi-pencil-square"></i></a>
            </th>
          </tr>
        </thead>   
        <tbody>
          <tr>
            <td>Проверка по местам работы</td>
            <td>{{ tbl['workplace'] ? tbl['workplace'] : '' }}</td>
          </tr>
          <tr>
            <td>Бывший работник МТСБ</td>
            <td>{{ tbl['employee'] ? tbl['employee'] : '' }}</td>
          </tr>
          <tr>
            <td>Проверка паспорта</td>
            <td>{{ tbl['document'] ? tbl['document'] : '' }}</td>
          </tr>
          <tr>
            <td>Проверка ИНН</td>
            <td>{{ tbl['inn'] ? tbl['inn'] : '' }}</td>
          </tr>
          <tr>
            <td>Проверка ФССП</td>
            <td>{{ tbl['debt'] ? tbl['debt'] : '' }}</td>
          </tr>
          <tr>
            <td>Проверка банкротства</td>
            <td>{{ tbl['bankruptcy'] ? tbl['bankruptcy'] : '' }}</td>
          </tr>
          <tr>
            <td>Проверка БКИ</td>
            <td>{{ tbl['bki'] ? tbl['bki'] : '' }}</td>
          </tr>
          <tr>
            <td>Проверка судебных дел</td>
            <td>{{ tbl['courts'] ? tbl['courts'] : '' }}</td>
          </tr>
          <tr>
            <td>Проверка аффилированности</td>
            <td>{{ tbl['affiliation'] ? tbl['affiliation'] : '' }}</td>
          </tr>
          <tr>
            <td>Проверка по списку террористов</td>
            <td>{{ tbl['terrorist'] ? tbl['terrorist'] : '' }}</td>
          </tr>
          <tr>
            <td>Проверка нахождения в розыске</td>
            <td>{{ tbl['mvd'] ? tbl['mvd'] : '' }}</td>
          </tr>
          <tr>
            <td>Проверка в открытых источниках</td>
            <td>{{ tbl['internet'] ? tbl['internet'] : '' }}</td>
          </tr>
          <tr>
            <td>Проверка Кронос</td>
            <td>{{ tbl['cronos'] ? tbl['cronos'] : '' }}</td>
          </tr>
          <tr>
            <td>Проверка Крос</td>
            <td>{{ tbl['cros'] ? tbl['cros'] : '' }}</td>
          </tr>
          <tr>
            <td>Дополнительная информация</td>
            <td>{{ tbl['addition'] ? tbl['addition'] : '' }}</td>
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
      <button class="btn btn-outline-primary" 
              @click="storeProfile.getItem('check', 'add')" 
              :disabled="![storeClassify.classifyItems.status['new'], 
                          storeClassify.classifyItems.status['update'], 
                          storeClassify.classifyItems.status['save'], 
                          storeClassify.classifyItems.status['repeat']].includes(storeProfile.profile.resume['status'])">Добавить проверку
      </button>
    </div>

  </div>
</template>