<script setup lang="ts">

import { onBeforeMount, watch } from 'vue';
import { useRoute } from 'vue-router';
import { loginStore } from '@/store/login';
import FooterDiv from '@components/layouts/FooterDiv.vue';
import AlertMessage from '@components/layouts/AlertMessage.vue';
import NavBar from '@components/layouts/NavBar.vue';

const storeLogin = loginStore();
const route = useRoute();

onBeforeMount(() => {
  storeLogin.getAuth()
});

watch(() => route.params.group,
  newValue => {
    storeLogin.pageIdentity = newValue as string;
  }
);

</script>

<template>
  <NavBar />
  <AlertMessage />
  <router-view></router-view>
  <FooterDiv />

  <div class="modal" id="modalApp" data-bs-backdrop="static" data-bs-keyboard="false" 
       tabindex="-1" aria-labelledby="modalAppLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
      <div class="modal-content">
          <button hidden class="btn-close" type="button" id="closeModal" data-bs-dismiss="modal"></button>
        <div class="modal-body py-5">
          <div class="text-primary text-opacity-75 py-3">
            <h1 class="text-center">StaffSec</h1>
          </div>
          <div class="text-secondary text-opacity-95 py-3">
            <h3 class="text-center">Кадровая безопасность</h3>
          </div>
          <div class="text-secondary text-opacity-95 py-3">
            <h5 class="text-center">Интерфейс базы данных кандидатов и сотрудников</h5>
          </div>
          <div class="progress" role="progressbar">
            <div class="progress-bar progress-bar-striped progress-bar-animated" style="width: 100%"></div>
          </div>
          <div class="py-3">
            <p class="text-center text-secondary text-opacity-95 py-1">MIT License</p>
            <p class="text-center text-secondary text-opacity-95 py-1">2023 Версия 0.1</p>
          </div>
        </div>  

      </div>
    </div>
  </div>

  <button id="openModal" hidden type="button" data-bs-toggle="modal" data-bs-target="#modalApp"></button>

</template>

<style>
.modal-backdrop {
  opacity: 0.85 !important;
}
</style>
