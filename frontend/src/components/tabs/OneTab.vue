<script setup lang="ts">

import { profileStore } from '@/store/profile';

const storeProfile = profileStore();

</script>

<template>
  <div class="py-3">
    <div v-if="storeProfile.dataProfile.ones?.length" >
      <div v-for="tbl in storeProfile.dataProfile.ones" :key="tbl['id']" >
        <table class="table table-responsive">
          <thead>
            <th colspan="2">{{ `ID #${tbl['id']}` }}</th>
          </thead>
          <tbody>
            <tr>
              <td>Период</td>
              <td>{{ tbl['start_date'] }} - {{ tbl['end_date'] }}</td>
            </tr>
            <tr>
              <td>Стартовая должность</td>
              <td>{{ tbl['start_position'] ? tbl['start_position'] : 'Данные отсутствуют' }}</td>
            </tr>
            <tr>
              <td>Должность при увольнении</td>
              <td>{{ tbl['end_position'] ? tbl['end_position'] : 'Работает по н.в.' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <p v-else >Данные отсутствуют</p>
  </div>
</template>