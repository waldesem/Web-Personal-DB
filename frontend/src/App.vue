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
  // const appModal = new bootstrap.Model('#modalApp')
  // appModal.show();
  // setTimeout(appModal.hide(), 3000)
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
    <div class="modal-dialog modal-dialog-centered modal" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="modalUserLabel">Кадровая безопасность</h1>
        </div>
        <div class="modal-body">
          <div class="py-2">
            <div class="text-primary text-opacity-75 py-3">
              <h1>StaffSec</h1>
            </div>
            <p class="text-center">Web interface for managing a candidate database</p>
            <div class="modal-footer">
              <p class="text-end">2023</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>
