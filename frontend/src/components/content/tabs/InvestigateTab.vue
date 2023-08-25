<script setup lang="ts">
// компонент для отображения и редактирования данных расследований

import { appProfile } from '@/store/profile';

const storeProfile = appProfile();

</script>

<template>
  <div class="py-3">
    <template v-if="(storeProfile.action === 'update' || storeProfile.action === 'create') && storeProfile.flag === 'investigation'">
      <form @submit.prevent="storeProfile.updateItem" class="form form-check" role="form"  id="investigationFormId">
        <div class="mb-3 row required">
          <label class="col-form-label col-lg-2" for="theme">Тема проверки</label>
          <div class="col-lg-10">
            <input class="form-control" id="theme" maxlength="250" name="theme" required type="text" v-model="storeProfile.itemForm['theme']">
          </div>
        </div>
        <div class="mb-3 row required">
          <label class="col-form-label col-lg-2" for="info">Информация</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="info" name="info" required v-model="storeProfile.itemForm['info']"></textarea>
          </div>
        </div>
        <div class=" row">
          <div class="offset-lg-2 col-lg-10">
            <div class="btn-group" role="group">
                <button class="btn btn-outline-primary" type="submit">Принять</button>
                <button class="btn btn-outline-primary" type="reset">Очистить</button>
                <button class="btn btn-outline-primary" type="button" @click="storeProfile.cancelEdit">Отмена</button>
              </div>
            </div>
        </div>
      </form>
    </template>

    <template v-else>
      <table v-if="storeProfile.inquisition?.length" v-for="tbl in storeProfile.inquisition" :key="tbl['id']" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
            <th>
              <a href="#" @click="storeProfile.deleteItem(tbl['id' as keyof typeof tbl].toString(), 'investigation')"
                           title="Удалить">
                          <i class="bi bi-trash"></i></a>
                          &nbsp;
              <a href="#" @click="storeProfile.action = 'update'; 
                                  storeProfile.flag = 'investigation';
                                  storeProfile.itemId = tbl['id' as keyof typeof tbl].toString(); 
                                  storeProfile.itemForm = tbl"
                title="Изменить"><i class="bi bi-pencil-square"></i>
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
      <a @click="storeProfile.action = 'create';
                 storeProfile.flag = 'investigation';
                 storeProfile.itemForm = {}" 
        class="btn btn-outline-primary" type="button">Добавить запись</a>
    </template>
  </div>
</template>