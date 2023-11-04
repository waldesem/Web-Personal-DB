<script setup lang="ts">

import { profileStore } from '@/store/profile';
import InvestigationForm from '@components/forms/InvestigationForm.vue'

const storeProfile = profileStore();

</script>

<template>
  <div class="py-3">

    <InvestigationForm v-if="(storeProfile.action === 'update' 
                            || storeProfile.action === 'create') 
                          && storeProfile.flag === 'investigation'" />

    <div v-else class="accordion" id="accordionInvestigation">
      <div class="accordion-item" v-if="storeProfile.profile.inquisition?.length" 
                                  v-for="tbl in storeProfile.profile.inquisition" 
                                   :key="tbl['id']" >
        <h6 class="accordion-header">
          <button class="accordion-button collapsed" type="button" data-bs-toogle="collapse" 
                  :data-bs-target="`#${tbl['id']}`">
            {{ `ID #${tbl['id']}` }}
          </button>
        </h6>
        <div :id="tbl['id']" class="accordion-collapse collapse" 
             data-bs-parent="#accordionInvestigation">
          <div class="accordion-body">
            <table class="table table-responsive">
              <thead>
                <tr>
                  <th width="25%">
                    <a href="#" title="Удалить"
                       @click="storeProfile.deleteItem(tbl['id'].toString(), 'investigation')">
                      <i class="bi bi-trash"></i>
                    </a>
                  </th>
                  <th>                    
                    <a href="#" title="Изменить"
                       @click="storeProfile.openForm('investigation', 'update', 
                                                      tbl['id'].toString(), tbl)">
                      <i class="bi bi-pencil-square"></i>
                    </a>
                  </th>
                </tr>
              </thead>        
              <tbody>
                <tr>
                  <td>Тема</td>
                  <td>{{ tbl['theme'] ? tbl['theme'] : 'Данные отсутствуют' }}</td>
                </tr>
                <tr>
                  <td>Информация</td>
                  <td>{{ tbl['info'] ? tbl['info'] : 'Данные отсутствуют' }}</td>
                </tr>
                <tr>
                  <td>Сотрудник</td>
                  <td>{{ tbl['officer'] ? tbl['officer'] : 'Данные отсутствуют' }}</td>
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
                  <td>Дата</td>
                  <td>{{ tbl['deadline'] ? new Date(String(tbl['deadline'])).
                    toLocaleDateString('ru-RU') : 'Данные отсутствуют' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <p v-else >Данные отсутствуют</p>
      
      <div class="py-3">
        <a class="btn btn-outline-primary" type="button"
          @click="storeProfile.openForm('investigation', 'create')">Добавить запись
        </a>
      </div>
    </div>
    
  </div>
</template>