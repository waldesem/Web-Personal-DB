<script setup lang="ts">

import { defineAsyncComponent } from 'vue';
import { profileStore } from '@/store/profile';
import { classifyStore } from '@/store/classify';

const TextLabel = defineAsyncComponent(() => import('@components/elements/TextLabel.vue'));
const SelectDiv = defineAsyncComponent(() => import('@components/elements/SelectDiv.vue'));
const BtnGroupForm = defineAsyncComponent(() => import('@components/elements/BtnGroupForm.vue'));

const storeClassify = classifyStore();
const storeProfile = profileStore();

</script>

<template v-if="storeProfile.action === 'create' && storeProfile.flag === 'registry'">
  <form @submit.prevent="storeProfile.dataProfile.updateItem" class="form form-check" role="form">
    <TextLabel :name="'comments'" :label="'Комментарий'"
               :model="storeProfile.dataProfile.form['comments']"/>
    <SelectDiv :name="'decision'" :label="'Решение'" :select="storeClassify.classData.decision"
               :model="storeProfile.dataProfile.form['decision']"/>
    <BtnGroupForm :disable="storeProfile.dataProfile.spinner">     
      <button class="btn btn-outline-primary" type="submit">
          {{ !storeProfile.dataProfile.spinner ? 'Принять' : '' }}
        <span v-if="storeProfile.dataProfile.spinner" class="spinner-border spinner-border-sm"></span>
        <span v-if="storeProfile.dataProfile.spinner" role="status">Отправляется...</span>
      </button>
      <button v-if="!storeProfile.dataProfile.spinner" 
                    class="btn btn-outline-primary" type="reset">Очистить</button>
      <button v-if="!storeProfile.dataProfile.spinner" 
                    class="btn btn-outline-primary" type="button" 
                    @click="storeProfile.dataProfile.cancelEdit">Отмена</button>
    </BtnGroupForm>
  </form>
</template>