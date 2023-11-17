<script setup lang="ts">

import { profileStore } from '@/store/profile';

const storeProfile = profileStore();

</script>

<template>
  <div class="py-3">
    <div class="accordion" id="accordionInquiry" v-if="storeProfile.profile.ones?.length" >
      <div class="accordion-item" v-for="tbl, idx in storeProfile.profile.ones" :key="tbl['id']" >
        <h6 class="accordion-header">
          <button type="button" data-bs-toggle="collapse"
                  :class="`accordion-button ${idx !== 0 ? 'collapsed' : ''}`"
                  :data-bs-target="`#collapseInquiry${tbl['id']}`">
            {{ `ID #${tbl['id']}` }}
          </button>
        </h6>
        <div :id="`collapseInquiry${tbl['id']}`" :class="`accordion-collapse collapse ${idx === 0 ? 'show' : ''}`" 
            data-bs-parent="#accordionInquiry">
          <div class="accordion-body">
            <table class="table table-responsive">
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
      </div>
    </div>
    <p v-else >Данные отсутствуют</p>
  </div>
</template>