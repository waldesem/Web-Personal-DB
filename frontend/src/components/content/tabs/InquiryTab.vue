<script setup lang="ts">
// компонент для отображения и редактирования данных запросов

import { appAnketa } from '@/store/anketa';
import { appProfile } from '@/store/profile';

const storeAnketa = appAnketa();

const storeProfile = appProfile();

</script>

<template>
  <div class="py-3">
    <template v-if="storeAnketa.action">
      <form @submit.prevent="storeAnketa.updateItem" class="form form-check" role="form"  id="inquiryFormId">
        <div class="mb-3 row required">
          <label class="col-form-label col-lg-2" for="info">Информация</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="info" name="info" required v-model="storeAnketa.itemForm.inquiry['info']"></textarea>
          </div>
        </div>
        <div class="mb-3 row required">
          <label class="col-form-label col-lg-2" for="initiator">Инициатор</label>
          <div class="col-lg-10">
            <input class="form-control" id="initiator" maxlength="250" name="initiator" required type="text" v-model="storeAnketa.itemForm.inquiry['initiator']">
          </div>
        </div>
        <div class="mb-3 row required">
          <label class="col-form-label col-lg-2" for="source">Источник</label>
          <div class="col-lg-10">
            <input class="form-control" id="source" maxlength="250" name="source" required type="text" v-model="storeAnketa.itemForm.inquiry['source']">
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
      <table v-if="storeProfile.needs?.length" v-for="tbl in storeProfile.needs" :key="tbl['id' as keyof typeof tbl]" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
            <th>
              <a href="#" @click="storeProfile.deleteItem(tbl['id' as keyof typeof tbl].toString(), 'inquiry')"
                           title="Удалить">
                          <i class="bi bi-trash"></i></a>
              &nbsp;
              <a href="#" @click="storeAnketa.action = 'update'; storeAnketa.itemId = tbl['id' as keyof typeof tbl].toString(); storeAnketa.itemForm = tbl"
                          title="Изменить" >
                          <i class="bi bi-pencil-square"></i></a>
            </th>
          </tr>
        </thead>        
        <tbody>
          <tr><td>Информация</td><td>{{ tbl['info' as keyof typeof tbl] }}</td></tr>
          <tr><td>Иннициатор</td><td>{{ tbl['initiator' as keyof typeof tbl] }}</td></tr>
          <tr><td>Источник</td><td>{{ tbl['source' as keyof typeof tbl] }}</td></tr>
          <tr><td>Сотрудник</td><td>{{ tbl['officer' as keyof typeof tbl] }}</td></tr>
          <tr>
            <td>Дата запроса</td>
            <td>{{ new Date(String(tbl['deadline' as keyof typeof tbl])).toLocaleDateString('ru-RU') }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
      <a @click="storeAnketa.action = 'create'; storeAnketa.itemForm = {}; storeAnketa.itemId = ''" class="btn btn-outline-primary" type="button">Добавить запись</a>
    </template>
  </div>
</template>