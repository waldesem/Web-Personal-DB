<script setup lang="ts">

import { profileStore } from '@/store/profile';
import PoligrafForm from '@components/forms/PoligrafForm.vue';

const storeProfile = profileStore();

</script>

<template>
  <div class="py-3">
    
    <PoligrafForm v-if="(storeProfile.action === 'update' 
                  || storeProfile.action === 'create') 
                  && storeProfile.flag === 'poligraf'"/>
      
    <div v-else>
      <table v-if="storeProfile.profile.pfo.length" 
             v-for="tbl in storeProfile.profile.pfo" 
              :key="tbl['id' as keyof typeof tbl]" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
            <th v-if="!storeProfile.printPdf">
              <a href="#" @click="storeProfile.deleteItem(tbl['id'].toString(), 'poligraf')" 
                 title="Удалить">
                <i class="bi bi-trash"></i>
              </a>
              &nbsp;
              <a href="#" @click="storeProfile.action = 'update'; 
                                  storeProfile.flag = 'poligraf';
                                  storeProfile.itemId = tbl['id']; 
                                  storeProfile.itemForm = tbl"
                 title="Изменить" >
                <i class="bi bi-pencil-square"></i></a>
            </th>
            <th v-else>></th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Тема</td>
            <td>{{ tbl['theme' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Результат</td>
            <td>{{ tbl['results' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Ссылка</td>
            <td>{{ tbl['path' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Полиграфолог</td>
            <td>{{ tbl['officer' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Дата</td>
            <td>{{ new Date(String(tbl['deadline' as keyof typeof tbl])).
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
      <p v-else >Данные отсутствуют</p>
      <button v-if="!storeProfile.printPdf" 
              @click="storeProfile.action = 'create'; 
                      storeProfile.flag = 'poligraf';
                      storeProfile.itemForm = {}" 
        class="btn btn-outline-primary" type="button">Добавить запись</button>
    </div>
  
  </div>
</template>