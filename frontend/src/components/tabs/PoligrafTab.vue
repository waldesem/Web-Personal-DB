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
      <div class="accordion" id="accordionPoligraf" v-if="storeProfile.profile.pfo?.length">
        <div class="accordion-item" v-for="tbl, idx in storeProfile.profile.pfo" 
                                    :key="tbl['id']" >
          <h6 class="accordion-header">
            <button :class="`accordion-button ${idx !== 0 ? 'collapsed' : ''}`" type="button" data-bs-toggle="collapse" 
                    :data-bs-target="`#collapsePoligraf${tbl['id']}`">
              {{ `ID #${tbl['id']}` }}
            </button>
          </h6>
          <div :id="`collapsePoligraf${tbl['id']}`" :class="`accordion-collapse collapse ${idx === 0 ? 'show' : ''}`" 
              data-bs-parent="#accordionPoligraf">
            <div class="accordion-body">
              <table class="table table-responsive">
                <thead>
                  <tr>
                    <th width="25%">
                      <a href="#" title="Удалить"
                        @click="storeProfile.deleteItem(tbl['id'].toString(), 'poligraf')">
                        <i class="bi bi-trash"></i>
                      </a>
                    </th>
                    <th>                    
                      <a href="#" title="Изменить"
                        @click="storeProfile.openForm('poligraf', 'update', 
                                                        tbl['id'].toString(), tbl)">
                        <i class="bi bi-pencil-square"></i>
                      </a>
                    </th>
                  </tr>
                </thead>        
                <tbody>
                  <tr>
                    <td>Тема</td>
                    <td>{{ tbl['theme'] ? tbl['theme'] : 'Данные отсуствуют' }}</td>
                  </tr>
                  <tr>
                    <td>Результат</td>
                    <td>{{ tbl['results'] ? tbl['results'] : 'Данные отсуствуют' }}</td>
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
                  <tr>
                    <td>Дата</td>
                    <td>{{ tbl['deadline'] ? new Date(String(tbl['deadline'])).
                      toLocaleDateString('ru-RU') : 'Данные отсуствуют' }}</td>
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
          </div>
        </div>
      </div>
      <p v-else >Данные отсутствуют</p>
      <div class="py-3">
        <button class="btn btn-outline-primary" type="button"
                @click="storeProfile.openForm('poligraf', 'create')">Добавить запись
        </button>
      </div>
    </div>
  </div>
  
</template>