<script setup lang="ts">

import { profileStore } from '@/store/profile';
import InquiryForm from '@components/forms/InquiryForm.vue'

const storeProfile = profileStore();

</script>

<template>
  <div class="py-3">
    <InquiryForm v-if="(storeProfile.action === 'update'
                  || storeProfile.action === 'create') 
                  && storeProfile.flag === 'inquiry'" />

    <div v-else class="accordion" id="accordionInquiry">
      <div class="accordion-item" v-if="storeProfile.profile.needs?.length" 
                                  v-for="tbl in storeProfile.profile.needs" 
                                  :key="tbl['id']" >
        <h6 class="accordion-header">
          <button class="accordion-button collapsed" type="button" data-bs-toogle="collapse" 
                  :data-bs-target="`#${tbl['id']}`">
            {{ `#${tbl['id']}` }}
          </button>
        </h6>
        <div :id="tbl['id']" class="accordion-collapse collapse" 
             data-bs-parent="#accordionInquiry">
          <div class="accordion-body">
            <table class="table table-responsive">
              <thead>
                <tr>
                  <th width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
                  <th>
                    <a href="#" title="Удалить"
                       @click="storeProfile.deleteItem(tbl['id'].toString(), 'inquiry')">
                      <i class="bi bi-trash"></i>
                    </a>
                    &nbsp;
                    <a href="#" title="Изменить"
                       @click="storeProfile.openForm('inquiry', 'update', 
                                                      tbl['id'].toString(), tbl)">
                      <i class="bi bi-pencil-square"></i>
                    </a>
                  </th>
                </tr>
              </thead>        
              <tbody>
                <tr>
                  <td>Информация</td>
                  <td>{{ tbl['info'] ? tbl['info'] : 'Данные отсутствуют' }}</td>
                </tr>
                <tr>
                  <td>Иннициатор</td>
                  <td>{{ tbl['initiator'] ? tbl['initiator'] : 'Данные отсутствуют' }}</td>
                </tr>
                <tr>
                  <td>Источник</td>
                  <td>{{ tbl['source'] ? tbl['source'] : 'Данные отсутствуют' }}</td>
                </tr>
                <tr>
                  <td>Сотрудник</td>
                  <td>{{ tbl['officer'] ? tbl['officer'] : 'Данные отсутствуют' }}</td>
                </tr>
                <tr>
                  <td>Дата запроса</td>
                  <td>{{tbl['deadline']
                        ? new Date(String(tbl['deadline'])).toLocaleDateString('ru-RU') 
                        : 'Данные отсутствуют' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <p v-else >Данные отсутствуют</p>
      <a class="btn btn-outline-primary" type="button"
         @click="storeProfile.openForm('inquiry', 'create')">Добавить запись
      </a>
    </div>
  </div>
</template>