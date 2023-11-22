<script setup lang="ts">

import { profileStore } from '@/store/profile';
import InvestigationForm from '@components/forms/InvestigationForm.vue';
import InvestigateAccord from '@components/tabs/accordions/InvestigateAccord.vue';

const storeProfile = profileStore();

</script>

<template>
  <div class="py-3">

    <InvestigationForm v-if="(storeProfile.dataProfile.action === 'update' 
                            || storeProfile.dataProfile.action === 'create') 
                          && storeProfile.dataProfile.flag === 'investigation'" />
    <div v-else>
      <InvestigateAccord :store="storeProfile.dataProfile"></InvestigateAccord>
      <div class="py-3">
        <a class="btn btn-outline-primary" type="button"
          @click="storeProfile.dataProfile.openForm('investigation', 'create')">Добавить запись
        </a>
      </div>
    </div>
  </div>
</template>