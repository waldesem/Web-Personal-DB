<script setup lang="ts">
// компонент для отображения данных согласования кандидата

import { ref } from 'vue';
import { appClassify } from '@store/classify';
import { appProfile } from '@/store/profile';

const classifyApp = appClassify();

const storeProfile = appProfile();

const registry = ref({});  // реактивные данные для показа в форме

const action = ref(''); // action для редактирования

/**
 * Updates an item.
 *
 * @return {void} This function does not return anything.
 */
 function updateItem(): void {
  storeProfile.updateItem(storeProfile.candId, 'registry', action.value, '', registry.value)
    action.value = '';
  };

</script>

<template>
  <div class="py-3">

    <template v-if="action">
      <form @submit.prevent="updateItem" class="form form-check" role="form"  id="registryFormId">
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="comments">Комментарий</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="comments" name="comments" v-model="registry['comments' as keyof typeof registry]"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="decision">Решение</label>
          <div class="col-lg-10">
            <select class="form-select" id="decision" name="decision" v-model="registry['decision' as keyof typeof registry]">
              <option v-for="(name, value) in classifyApp.decision" :key="value"  :value="name">{{ name }}</option>
            </select>
          </div>
        </div>
        <div class=" row">
          <div class="offset-lg-2 col-lg-10">
            <div class="btn-group" role="group">
              <button class="btn btn-outline-primary" type="submit">Принять</button>
              <button class="btn btn-outline-primary" type="reset">Очистить</button>
              <button class="btn btn-outline-primary" type="button" @click="action = ''; registry = {}">Отмена</button>
            </div>
          </div>
        </div>
      </form>
    </template>

    <template v-else>
      <table v-if="storeProfile.register.length" v-for="tbl in storeProfile.register" class="table table-responsive">
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
      <button :disabled="classifyApp.status && (storeProfile.status !== classifyApp.status['result'])" @click="action = 'create'" class="btn btn-outline-primary" type="button">Добавить запись</button>
    </template>
  
  </div>
</template>