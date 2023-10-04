<script setup lang="ts">
// компонент для отображения данных согласования кандидата
 
import { profileStore } from '@/store/profile';
import { classifyStore } from '@/store/classify';
import { loginStore } from '@/store/login';

const storeProfile = profileStore();
const classifyApp = classifyStore();
const loginStore = loginStore();

</script>

<template>
  <div class="py-3">

    <template v-if="storeProfile.action === 'create' && storeProfile.flag === 'registry'">
      <form @submit.prevent="storeProfile.updateItem()" class="form form-check" role="form"  id="registryFormId">
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="comments">Комментарий</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="comments" name="comments" v-model="storeProfile.itemForm['comments']"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="decision">Решение</label>
          <div class="col-lg-10">
            <select class="form-select" id="decision" name="decision" v-model="storeProfile.itemForm['decision']">
              <option v-for="(name, value) in classifyApp.decision" :key="value" :value="name">{{ name }}</option>
            </select>
          </div>
        </div>
        <div class=" row">
          <div class="offset-lg-2 col-lg-10">
            <div class="btn-group" role="group" :disabled="storeProfile.spinner">              
              <button class="btn btn-outline-primary" type="submit">{{ !storeProfile.spinner ? 'Принять' : '' }}
                <span v-if="storeProfile.spinner" class="spinner-border spinner-border-sm" aria-hidden="true"></span>
                <span v-if="storeProfile.spinner" role="status">Отправляется...</span>
              </button>
              <button v-if="!storeProfile.spinner" class="btn btn-outline-primary" type="reset">Очистить</button>
              <button v-if="!storeProfile.spinner" class="btn btn-outline-primary" type="button" @click="storeProfile.cancelEdit">Отмена</button>
            </div>
          </div>
        </div>
      </form>
    </template>

    <template v-else>
      <table v-if="storeProfile.register.length" v-for="tbl in storeProfile.register" :key="tbl['id']" class="table table-responsive">
        <thead>
          <tr><th width="25%">{{ tbl['id'] ? `#${tbl['id']}` : '' }}</th><th></th></tr>
        </thead>
        <tbody>
          <tr><td>Комментарий</td><td>{{ tbl['comments'] ? tbl['comments'] : '' }}</td></tr>
          <tr><td>Решение</td><td>{{ tbl['decision'] ? tbl['decision'] : '' }}</td></tr>
          <tr><td>Согласующий</td><td>{{ tbl['supervisor'] ? tbl['supervisor'] : '' }}</td></tr>
          <tr><td>Дата</td><td>{{ tbl['deadline'] ? new Date(tbl['deadline']).toLocaleDateString('ru-RU') : '' }}</td></tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
      <button v-if="!storeProfile.printPdf" :disabled="storeProfile.anketa.resume['status'] !== classifyApp.status['result']
                                            || !loginStore.hasRole('superuser')" 
                                            @click="storeProfile.action = 'create'; 
                                                    storeProfile.flag = 'registry';
                                                    storeProfile.itemForm = {}" 
        class="btn btn-outline-primary" type="button">Добавить запись
      </button>
    </template>
  
  </div>
</template>