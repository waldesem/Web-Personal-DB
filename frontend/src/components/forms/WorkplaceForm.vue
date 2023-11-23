<script setup lang="ts">

import { defineAsyncComponent } from 'vue';
import { profileStore } from '@/store/profile';

const InputLabel = defineAsyncComponent(() => import('@components/elements/InputLabel.vue'));
const TextLabel = defineAsyncComponent(() => import('@components/elements/TextLabel.vue'));
const BtnGroupForm = defineAsyncComponent(() => import('@components/elements/BtnGroupForm.vue'));

const storeProfile = profileStore();

</script>

<template>
  <form @submit.prevent="storeProfile.dataProfile.updateItem" class="form form-check" role="form">
    <InputLabel :name="'start_date'" :label="'Начало работы'" :typeof="'date'"
                :model="storeProfile.dataProfile.form['start_date']"/>
    <InputLabel :name="'end_date'" :label="'Окончание работы'" :typeof="'date'"
                :model="storeProfile.dataProfile.form['end_date']"/>
    <InputLabel :name="'workplace'" :label="'Место работы'" :need="true"
               :model="storeProfile.dataProfile.form['workplace']"/>
    <TextLabel :name="'address'" :label="'Адрес организации'"
               :model="storeProfile.dataProfile.form['address']"/>
    <TextLabel :name="'position'" :label="'Должность'"
               :model="storeProfile.dataProfile.form['position']"/>
    <TextLabel :name="'reason'" :label="'Причина увольнения'"
               :model="storeProfile.dataProfile.form['reason']"/>
    <BtnGroupForm>
      <button class="btn btn-outline-primary btn-md" name="submit" type="submit">Принять</button>
      <button class="btn btn-outline-primary btn-md" name="reset" type="reset">Очистить</button>
    </BtnGroupForm>
  </form>
</template>
