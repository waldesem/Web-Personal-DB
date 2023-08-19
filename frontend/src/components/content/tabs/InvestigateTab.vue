<script setup lang="ts">
// компонент для отображения и редактирования данных расследований

import { ref } from 'vue';
import { appProfile } from '@/store/profile';

const storeProfile = appProfile();

// реактивные данные для показа в форме
const investigation = ref({
  theme: '',
  info: ''
});

const investigation_id = ref('');

const action = ref(''); // action для редактирования

/**
 * Updates an item.
 *
 * @return {void} This function does not return anything.
 */
 function updateItem(): void {
    storeProfile.updateItem(storeProfile.candId, 'investigation', action.value, investigation_id.value, {
      'theme': investigation.value.theme, 
      'info': investigation.value.info
    });
    cancelAction();
  };

/**
 * Cancels the current action.
 *
 * @return {void}  */
function cancelAction(): void {
    action.value = '';
    investigation_id.value = '';
    Object.assign(investigation.value, {
      'theme': '',
      'info': ''
    })
  };

</script>

<template>
  <div class="py-3">
    <template v-if="action">
      <form @submit.prevent="updateItem" class="form form-check" role="form"  id="investigationFormId">
        <div class="mb-3 row required">
          <label class="col-form-label col-lg-2" for="theme">Тема проверки</label>
          <div class="col-lg-10">
            <input class="form-control" id="theme" maxlength="250" name="theme" required type="text" v-model="investigation['theme' as keyof typeof investigation]">
          </div>
        </div>
        <div class="mb-3 row required">
          <label class="col-form-label col-lg-2" for="info">Информация</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="info" name="info" required v-model="investigation['info' as keyof typeof investigation]"></textarea>
          </div>
        </div>
        <div class=" row">
          <div class="offset-lg-2 col-lg-10">
            <div class="btn-group" role="group">
                <button class="btn btn-outline-primary" type="submit">Принять</button>
                <button class="btn btn-outline-primary" type="reset">Очистить</button>
                <button class="btn btn-outline-primary" type="button" @click="cancelAction">Отмена</button>
              </div>
            </div>
        </div>
      </form>
    </template>

    <template v-else>
      <table v-if="storeProfile.inquisition?.length" v-for="tbl in storeProfile.inquisition" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
            <th>
              <a href="#" @click="storeProfile.deleteItem(tbl['id' as keyof typeof tbl].toString(), 'investigation')"
                           data-bs-toggle="tooltip" data-bs-placement="right" title="Удалить">
                          <i class="bi bi-trash"></i></a>
                          &nbsp;
              <a href="#" @click="action = 'update'; investigation_id = tbl['id' as keyof typeof tbl].toString(); investigation = tbl"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Изменить" >
                <i class="bi bi-pencil-square"></i>
              </a>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Тема</td><td>{{ tbl['theme' as keyof typeof tbl] }}</td></tr>
          <tr><td>Информация</td><td>{{ tbl['info' as keyof typeof tbl] }}</td></tr>
          <tr><td>Сотрудник</td><td>{{ tbl['officer' as keyof typeof tbl] }}</td></tr>
          <tr>
            <td>Дата</td>
            <td>{{ new Date(String(tbl['deadline' as keyof typeof tbl])).toLocaleDateString('ru-RU') }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
      <a @click="action = 'create'" class="btn btn-outline-primary" type="button">Добавить запись</a>
    </template>
  </div>
</template>