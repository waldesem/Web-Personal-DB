<script setup lang="ts">
// компонент для отображения данных согласования кандидата
 
import { appAnketa } from '@/store/anketa';
import { appProfile } from '@/store/profile';
import { appClassify } from '@/store/classify';

const storeAnketa = appAnketa();

const storeProfile = appProfile();

const classifyApp = appClassify();

</script>

<template>
  <div class="py-3">

    <template v-if="storeAnketa.action">
      <form @submit.prevent="storeAnketa.updateItem" class="form form-check" role="form"  id="registryFormId">
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="comments">Комментарий</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="comments" name="comments" v-model="storeAnketa.itemForm.registry['comments']"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="decision">Решение</label>
          <div class="col-lg-10">
            <select class="form-select" id="decision" name="decision" v-model="storeAnketa.itemForm.registry['decision']">
              <option v-for="(name, value) in classifyApp.decision" :key="value" :value="name">{{ name }}</option>
            </select>
          </div>
        </div>
        <div class=" row">
          <div class="offset-lg-2 col-lg-10">
            <div class="btn-group" role="group">
              <button class="btn btn-outline-primary" type="submit">Принять</button>
              <button class="btn btn-outline-primary" type="reset">Очистить</button>
              <button class="btn btn-outline-primary" type="button" @click="storeAnketa.cancelEdit">Отмена</button>
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
      <button :disabled="classifyApp.status && (storeProfile.anketa.resume['status'] !== classifyApp.status['result'])" @click="storeAnketa.action = 'create'; storeAnketa.itemForm = {}; storeAnketa.itemId = ''" class="btn btn-outline-primary" type="button">Добавить запись</button>
    </template>
  
  </div>
</template>