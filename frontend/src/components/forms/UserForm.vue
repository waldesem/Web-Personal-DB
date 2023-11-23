<script setup lang="ts">

import { defineAsyncComponent } from 'vue';
import { adminStore } from '@store/admins';
import { classifyStore } from '@/store/classify';

const InputLabel = defineAsyncComponent(() => import('@components/elements/InputLabel.vue'));
const BtnGroupForm = defineAsyncComponent(() => import('@components/elements/BtnGroupForm.vue'));
const SelectDiv = defineAsyncComponent(() => import('@components/elements/SelectDiv.vue'));
const ModalWin = defineAsyncComponent(() => import('@components/layouts/ModalWin.vue'));

const storeAdmin = adminStore();
const storeClassify = classifyStore();

</script>

<template>
  <ModalWin :title ="storeAdmin.dataUsers.action === 'edit'
                ? 'Изменить пользователя' 
                : 'Создать пользователя'" 
              :size="'modal-xl'" :id="'modalUser'">
    <form @submit.prevent="storeAdmin.dataUsers.submitUser" class="form form-check" role="form">
      <InputLabel :name="'fullname'" :label="'Имя пользователя:'" :need="true" 
                  :pattern="'[a-zA-Zа-яА-Я ]+'"
                  :model="storeAdmin.dataUsers.form['fullname']"/>
      <InputLabel :name="'username'" :label="'Учетная запись:'" :need="true" 
                  :pattern="'[a-zA-Z]+'" 
                  :disable="storeAdmin.dataUsers.action === 'edit'"
                  :model="storeAdmin.dataUsers.form['username']"/>
      <InputLabel :name="'email'" :label="'Электронная почта:'" :need="true" 
                  :typeof="'email'"
                  :model="storeAdmin.dataUsers.form['email']"/>
      <SelectDiv :name="'region'" :label="'Регион'" 
                 :select="storeClassify.classData.regions"
                 :model="storeAdmin.dataUsers.form['region_id']" />

      <BtnGroupForm>
        <button class="btn btn-outline-primary" name="submit" type="submit" 
                data-bs-dismiss="modal">
          {{storeAdmin.dataUsers.action === 'create' ? 'Создать' : 'Изменить'}}
        </button>
        <button class="btn btn-outline-primary" name="reset" type="reset">
          Очистить
        </button>
        <button class="btn btn-outline-primary" name="cancel" type="button"
                data-bs-dismiss="modal" 
                @click="storeAdmin.dataUsers.action = ''" >
          Отмена
        </button>
      </BtnGroupForm>
    </form>

  </ModalWin>
</template>