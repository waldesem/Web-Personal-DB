<script setup lang="ts">

import { onBeforeMount } from 'vue';
import { useRoute } from 'vue-router';
import { storeContact } from '@/store/contacts';

const contactStore = storeContact();

const route = useRoute();

contactStore.contactId = route.params.id as string;

onBeforeMount(async () => {
  contactStore.viewContact();
});

</script>

<template>
  <div class="container py-3">
    <div class="py-5"><h4>{{ contactStore.contactData.organization }}</h4></div>
    <div class="py-3">
      <table class="table table-hover table-responsive align-middle">
        <thead> 
          <tr height="50px">
            <th>Контакты</th>
          </tr>
        </thead>
        <tbody>
          <tr height="50px">
            <td></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
