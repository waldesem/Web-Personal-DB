<script setup lang="ts">

import { classifyStore } from '@store/classify';
import { profileStore } from '@/store/profile';
import { loginStore } from '@store/login';
import CheckForm from '@components/forms/CheckForm.vue'

const storeClassify = classifyStore();
const storeProfile = profileStore();
const storeLogin = loginStore();

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
            <th v-if="!storeProfile.printPdf">
              <a href="#" :disabled="storeClassify.classifyItems.status 
                          && (storeProfile.profile.resume['status'] === 
                              storeClassify.classifyItems.status['finish'])" 
                          @click="storeProfile.deleteItem(
                            'check', 'delete', tbl['id' as keyof typeof tbl].toString()
                            )"
                           title="Удалить">
                          <i class="bi bi-trash"></i></a>
                          &nbsp;
              <a href="#" :disabled="storeClassify.classifyItems.status 
                            && (storeProfile.profile.resume['status'] !== storeClassify.classifyItems.status['save'] 
                            && storeProfile.profile.resume['status'] !== storeClassify.classifyItems.status['cancel'] 
                            && storeProfile.profile.resume['status'] !== storeClassify.classifyItems.status['manual'])
                            || storeLogin.userData.region_id !== '1'" 
                          @click="storeProfile.action = 'update'; 
                                  storeProfile.flag = 'check';
                                  storeProfile.itemId = tbl['id' as keyof typeof tbl].toString(); 
                                  storeProfile.itemForm = tbl"
                          title="Изменить" >
                          <i class="bi bi-pencil-square"></i></a>
            </th>
            <th v-else></th>
          </tr>
        </thead>   
        <tbody>
          <tr>
            <td>Проверка по местам работы</td>
            <td>{{ tbl['workplace' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Бывший работник МТСБ</td>
            <td>{{ tbl['employee' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Проверка паспорта</td>
            <td>{{ tbl['document' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Проверка ИНН</td>
            <td>{{ tbl['inn' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Проверка ФССП</td>
            <td>{{ tbl['debt' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Проверка банкротства</td>
            <td>{{ tbl['bankruptcy' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Проверка БКИ</td>
            <td>{{ tbl['bki' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Проверка судебных дел</td>
            <td>{{ tbl['courts' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Проверка аффилированности</td>
            <td>{{ tbl['affiliation' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Проверка по списку террористов</td>
            <td>{{ tbl['terrorist' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Проверка нахождения в розыске</td>
            <td>{{ tbl['mvd' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Проверка в открытых источниках</td>
            <td>{{ tbl['internet' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Проверка Кронос</td>
            <td>{{ tbl['cronos' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Проверка Крос</td>
            <td>{{ tbl['cros' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Дополнительная информация</td>
            <td>{{ tbl['addition' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Материалы проверки</td>
            <td>{{ tbl['path' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>ПФО</td>
            <td>{{ tbl['pfo' as keyof typeof tbl] ? "Назначено" : "Не назначено" }}</td>
          </tr>
          <tr>
            <td>Комментарии</td>
            <td>{{ tbl['comments' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Результат проверки</td>
            <td>{{ tbl['conclusion' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Сотрудник</td>
            <td>
              <a href="#" @click="storeProfile.getItem('check', 'self', tbl['id' as keyof typeof tbl].toString())">
                {{ tbl['officer' as keyof typeof tbl] }}</a>
            </td>
          </tr>
          <tr>
            <td>Дата</td>
            <td>{{ new Date(String(tbl['deadline' as keyof typeof tbl])).toLocaleDateString('ru-RU') }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
      <button v-if="!storeProfile.printPdf" 
              @click="storeProfile.getItem('check', 'add')" 
              :disabled="![storeClassify.classifyItems.status['new'], 
                          storeClassify.classifyItems.status['update'], 
                          storeClassify.classifyItems.status['save'], 
                          storeClassify.classifyItems.status['repeat']].includes(storeProfile.profile.resume['status'])" 
        class="btn btn-outline-primary">Добавить проверку
      </button>
    </div>

  </div>
</template>