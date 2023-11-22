<script setup lang="ts">

import { profileStore } from '@/store/profile';
import InquiryForm from '@components/forms/InquiryForm.vue';
import InquiryAccord from '@components/tabs/accordions/InquiryAccord.vue';

const storeProfile = profileStore();

</script>

<template>
  <div class="py-3">
    <InquiryForm v-if="(storeProfile.dataProfile.action === 'update'
                        || storeProfile.dataProfile.action === 'create') 
                      && storeProfile.dataProfile.flag === 'inquiry'" />

    <div v-else>
      <InquiryAccord :store="storeProfile.dataProfile"/>
      <div class="py-3">
        <a class="btn btn-outline-primary" type="button"
          @click="storeProfile.dataProfile.openForm('inquiry', 'create')">Добавить запись
        </a>
      </div>
    </div>
  </div>
</template>