<script setup lang="ts">

import { profileStore } from '@/store/profile';
import { fileManagerStore } from '@store/fmanager';
import InvestigationForm from '@components/forms/InvestigationForm.vue'

const storeProfile = profileStore();
const storeFmanager = fileManagerStore();

</script>

<template>
  <div class="py-3">

    <InvestigationForm v-if="(storeProfile.action === 'update' 
                            || storeProfile.action === 'create') 
                          && storeProfile.flag === 'investigation'" />
    <div v-else>
      <div class="accordion" id="accordionInvestigation" v-if="storeProfile.profile.inquisition?.length" >
        <div class="accordion-item" v-for="tbl, idx in storeProfile.profile.inquisition" 
                                    :key="tbl['id']" >
          <h6 class="accordion-header">
            <button class="accordion-button" :class="{'collapsed': idx > 0 }" type="button" data-bs-toggle="collapse" 
                    :data-bs-target="`#collapseInvestigation${tbl['id']}`">
              {{ `ID #${tbl['id']}` }}
            </button>
          </h6>
          <div :id="`collapseInvestigation${tbl['id']}`" class="accordion-collapse collapse" :class="{ 'show': idx === 0}" 
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
                      <router-link @click="storeFmanager.fileManager.path = tbl['path'].split('/')" 
                                  :to="{ name: 'manager',  params: { group: 'staffsec' } }">
                      
                        {{ storeProfile.profile.resume['path'] }}
                      </router-link>
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