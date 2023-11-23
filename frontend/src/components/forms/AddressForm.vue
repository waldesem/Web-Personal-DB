<script setup lang="ts">

import { defineAsyncComponent } from 'vue';
import { profileStore } from '@/store/profile';

const InputLabel = defineAsyncComponent(() => import('@components/elements/InputLabel.vue'));
const TextLabel = defineAsyncComponent(() => import('@components/elements/TextLabel.vue'));
const SelectDiv = defineAsyncComponent(() => import('@components/elements/SelectDiv.vue'));
const BtnGroupForm = defineAsyncComponent(() => import('@components/elements/BtnGroupForm.vue'));

const storeProfile = profileStore();

const selected_item = {
  registration: "Адрес регистрации",
  live: "Адрес проживания",
  others: "Другое"
};

</script>

<template>
   <form @submit.prevent="storeProfile.dataProfile.updateItem" class="form form-check" role="form">
    <SelectDiv :name="''" :label="''" :select="selected_item"
               :model="storeProfile.dataProfile.form['view']"/>
    <InputLabel :name="'region'" :label="'Регион'" :need="true"
                :model="storeProfile.dataProfile.form['region']"/>
    <TextLabel :name="'address'" :label="'Полный адрес'"
                :model="storeProfile.dataProfile.form['address']"/>
    <BtnGroupForm>
      <button class="btn btn-outline-primary btn-md" name="submit" type="submit">Принять</button>
      <button class="btn btn-outline-primary btn-md" name="reset" type="reset">Очистить</button>
    </BtnGroupForm>
  </form>
</template>
