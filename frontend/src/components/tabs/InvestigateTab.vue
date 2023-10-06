<script setup lang="ts">

import { profileStore } from '@/store/profile';
import InvestigationForm from '@content/forms/InvestigationForm.vue'

const storeProfile = profileStore();

</script>

<template>
  <div class="py-3">

    <InvestigationForm v-if="(storeProfile.action === 'update' 
                  || storeProfile.action === 'create') 
                  && storeProfile.flag === 'investigation'" />

    <div v-else>
      <table v-if="storeProfile.profile.inquisition?.length" 
             v-for="tbl in storeProfile.profile.inquisition" 
              :key="tbl['id']" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
            <th v-if="!storeProfile.printPdf">
              <a href="#" @click="storeProfile.deleteItem(tbl['id' as keyof typeof tbl].
                toString(), 'investigation')"
                           title="Удалить">
                          <i class="bi bi-trash"></i></a>
                          &nbsp;
              <a href="#" @click="storeProfile.action = 'update'; 
                                  storeProfile.flag = 'investigation';
                                  storeProfile.itemId = tbl['id' as keyof typeof tbl].
                                    toString(); 
                                  storeProfile.itemForm = tbl"
                title="Изменить"><i class="bi bi-pencil-square"></i>
              </a>
            </th>
            <th v-else></th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Тема</td>
            <td>{{ tbl['theme' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Информация</td>
            <td>{{ tbl['info' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Сотрудник</td>
            <td>{{ tbl['officer' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Дата</td>
            <td>{{ new Date(String(tbl['deadline' as keyof typeof tbl])).
              toLocaleDateString('ru-RU') }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
      <a v-if="!storeProfile.printPdf" 
               @click="storeProfile.action = 'create';
                       storeProfile.flag = 'investigation';
                       storeProfile.itemForm = {}" 
        class="btn btn-outline-primary" type="button">Добавить запись</a>
    </div>
    
  </div>
</template>