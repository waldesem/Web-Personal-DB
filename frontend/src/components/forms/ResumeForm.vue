<script setup lang="ts">

import { defineAsyncComponent } from 'vue';
import { profileStore } from '@/store/profile';

const SelectDiv = defineAsyncComponent(() => import('@components/elements/SelectDiv.vue'));
const InputLabel = defineAsyncComponent(() => import('@components/elements/InputLabel.vue'));
const TextLabel = defineAsyncComponent(() => import('@components/elements/TextLabel.vue'));
const BtnGroupForm = defineAsyncComponent(() => import('@components/elements/BtnGroupForm.vue'));

const storeProfile = profileStore();

const select_items = {
  candidate: "Кандидат",
  suspict: "Проверяемый"
};

</script>


<template>
  <div class="py-3">
    <form @submit.prevent="storeProfile.dataProfile.submitResume" class="form form-check" role="form">
      <SelectDiv :name="'category'" :label="'Категория'" :select="select_items"
                 :model="storeProfile.dataProfile.form['category']" />
      <InputLabel :isneed="true" :name="'fullname'" :label="'Полное ФИО*'" 
                  :pattern="'[a-zA-Zа-я-АЯ -]+'"
                  :model="storeProfile.dataProfile.form['fullname']"/>
      <TextLabel :name="'previous'" :label="'Изменение имени'"
                  :model="storeProfile.dataProfile.form['previous']"/>
      <InputLabel :isneed="true" :name="'birthday'" :label="'Дата рождения*'" 
                  :typeof="'date'"
                  :model="storeProfile.dataProfile.form['previous']"/>
      <TextLabel :name="'birthplace'" :label="'Место рождения'" 
                  :model="storeProfile.dataProfile.form['birthplace']"/>
      <InputLabel :name="'country'" :label="'Гражданство'" :max="'255'"
                  :model="storeProfile.dataProfile.form['country']"/>
      <InputLabel :name="'ext_country'" :label="'Двойное гражданство'" :max="'255'"
                  :model="storeProfile.dataProfile.form['ext_country']"/>
      <InputLabel :name="'snils'" :label="'СНИЛС'" :max="'11'" :pattern="'\d{11}'"
                  :model="storeProfile.dataProfile.form['snils']"/>
      <InputLabel :name="'inn'" :label="'ИНН'" :max="'12'" :pattern="'\d{12}'"
                  :model="storeProfile.dataProfile.form['inn']"/>
      <TextLabel :name="'education'" :label="'Образование'" 
                  :model="storeProfile.dataProfile.form['education']"/>   
      <InputLabel :name="'marital'" :label="'Семейнное положение'" :max="'255'"
                  :model="storeProfile.dataProfile.form['marital']"/>
      <TextLabel :name="'addition'" :label="'Дополнительно'" 
                  :model="storeProfile.dataProfile.form['addition']"/>

      <BtnGroupForm>
        <button class="btn btn-outline-primary" type="submit">Принять</button>
        <button class="btn btn-outline-primary" type="reset">Очистить</button>
        <router-link v-if="storeProfile.dataProfile.action !== 'update'" 
                class="btn btn-outline-primary" type="button"
                :to="{ name: 'persons', params: { group: 'staffsec' }}">
                Отмена
        </router-link>
        <button v-else class="btn btn-outline-primary" type="button" 
                @click="storeProfile.dataProfile.cancelEdit">Отмена</button>
      </BtnGroupForm>
    </form>
  </div>
</template>
