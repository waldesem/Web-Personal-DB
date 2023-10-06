<script setup lang="ts">

import { profileStore } from '@/store/profile';
import InquiryForm from '@content/forms/InquiryForm.vue'

const storeProfile = profileStore();

</script>

<template>
  <div class="py-3">
    <InquiryForm v-if="(storeProfile.action === 'update'
                  || storeProfile.action === 'create') 
                  && storeProfile.flag === 'inquiry'" />

    <div v-else>
      <table v-if="storeProfile.profile.needs?.length" 
             v-for="tbl in storeProfile.profile.needs" 
             :key="tbl['id' as keyof typeof tbl]" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
            <th v-if="!storeProfile.printPdf">
              <a href="#" @click="storeProfile.deleteItem(tbl['id' as keyof typeof tbl].toString(), 'inquiry')"
                  title="Удалить">
                <i class="bi bi-trash"></i></a>
              &nbsp;
              <a href="#" @click="storeProfile.action = 'update';
                                  storeProfile.flag = 'inquiry';
                                  storeProfile.itemId = tbl['id' as keyof typeof tbl].toString(); 
                                  storeProfile.itemForm = tbl"
                title="Изменить"><i class="bi bi-pencil-square"></i></a>
            </th>
            <th v-else></th>
          </tr>
        </thead>        
        <tbody>
          <tr>
            <td>Информация</td>
            <td>{{ tbl['info' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Иннициатор</td>
            <td>{{ tbl['initiator' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Источник</td>
            <td>{{ tbl['source' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Сотрудник</td>
            <td>{{ tbl['officer' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Дата запроса</td>
            <td>{{ new Date(String(tbl['deadline' as keyof typeof tbl])).
              toLocaleDateString('ru-RU') }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
      <a v-if="!storeProfile.printPdf" @click="storeProfile.action = 'create'; 
                storeProfile.flag = 'inquiry';
                storeProfile.itemForm = {}"
         class="btn btn-outline-primary" type="button">Добавить запись</a>
    </div>
    
  </div>
</template>