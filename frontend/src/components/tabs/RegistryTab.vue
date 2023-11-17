<script setup lang="ts">
 
import { ref } from 'vue';
import { profileStore } from '@/store/profile';
import { classifyStore } from '@/store/classify';
import { loginStore } from '@/store/login';

const RegistryForm = () => import('@components/forms/RegistryForm.vue');

const storeProfile = profileStore();
const classifyApp = classifyStore();
const storeLogin = loginStore();

const disableRegBtn = ref(false);
disableRegBtn.value = (storeProfile.profile.resume['status'] 
                      !== classifyApp.classifyItems.status['result'])
                    || !storeLogin.hasRole('superuser')
</script>

<template>
  <div class="py-3">

    <RegistryForm v-if="storeProfile.action === 'create' 
                     && storeProfile.flag === 'registry'" />
    
    <div v-else>
      <div class="accordion" id="accordionRegistry" v-if="storeProfile.profile.register?.length">
        <div class="accordion-item" v-for="tbl, idx in storeProfile.profile.register" 
                                    :key="tbl['id']" >
          <h6 class="accordion-header">
            <button :class="`accordion-button ${idx !== 0 ? 'collapsed' : ''}`" 
                    type="button" data-bs-toggle="collapse" 
                    :data-bs-target="`#collapseRegistry${tbl['id']}`">
              {{ `ID #${tbl['id']}` }}
            </button>
          </h6>
          <div :id="`collapseRegistry${tbl['id']}`" 
               :class="`accordion-collapse collapse ${idx === 0 ? 'show' : ''}`" 
               data-bs-parent="#accordionRegistry">
            <div class="accordion-body">
              <table class="table table-responsive">
                <thead>
                  <tr>
                    <th width="25%">
                      <a href="#" title="Удалить"
                        @click="storeProfile.deleteItem(tbl['id'].toString(), 'registry')">
                        <i class="bi bi-trash"></i>
                      </a>
                    </th>
                    <th>                    
                      <a href="#" title="Изменить"
                        @click="storeProfile.openForm('registry', 'update', 
                                                        tbl['id'].toString(), tbl)">
                        <i class="bi bi-pencil-square"></i>
                      </a>
                    </th>
                  </tr>
                </thead>    
                <tbody>
                  <tr v-if="tbl['comments']">
                    <td>Комментарий</td><td>{{ tbl['comments'] }}</td>
                  </tr>
                  <tr v-if="tbl['decision']">
                    <td>Решение</td><td>{{ tbl['decision'] }}</td>
                  </tr>
                  <tr v-if="tbl['supervisor']">
                    <td>Согласующий</td><td>{{ tbl['supervisor'] }}</td>
                  </tr>
                  <tr v-if="tbl['deadline']">
                    <td>Дата</td><td>{{ new Date(tbl['deadline']).toLocaleDateString('ru-RU') }}</td>
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
                :disabled="disableRegBtn" 
                @click="storeProfile.openForm('registry', 'create')">Добавить запись
        </button>
      </div>
    </div>
  </div>
</template>