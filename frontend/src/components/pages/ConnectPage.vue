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
        <tbody>
          <th>
            <!--td width="15%">#</td><td width="15%">#</td><td width="15%">#</td><td width="15%">#</td><td width="15%">#</td><td width="15%">#</td-->
          </th>
          <tr v-for="location in contactStore.contactData.locations" :key="location['id']">
            <td>{{ location['territory'] }}</td>
            <td>
              <table>
                <tbody>
                  <tr v-for="connect in contactStore.contactData.connects" :key="connect['id']">
                    <td>{{ connect["name"] }}</td>
                    <td>{{ connect["comment"] }}</td>
                    <td>{{ connect["data"] }}</td>
                    <td>
                      <table>
                        <tbody>
                          <tr v-for="contact in contactStore.contactData.contacts" :key="contact['id']">
                            <td>{{ contact['view'] }}</td>
                            <td>{{ contact['contact'] }}</td>
                          </tr>
                        </tbody>
                      </table>
                    </td>
                  </tr>
                </tbody>
              </table>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
