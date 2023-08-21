<script setup lang="ts">
// компонент для отображения и редактирования данных полиграфа

import { appAnketa } from '@/store/anketa';
import { appProfile } from '@/store/profile';

const storeAnketa = appAnketa();

const storeProfile = appProfile();

</script>

<template>
  <div class="py-3">
    
    <template v-if="storeAnketa.action">
      <form @submit.prevent="storeAnketa.updateItem" class="form form-check" role="form"  id="poligrafFormId">
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="theme">Тема проверки</label>
          <div class="col-lg-10">
            <select class="form-select" id="theme" name="theme" required v-model="storeAnketa.itemForm.poligraf['theme']">
              <option value="Проверка кандидата">Проверка кандидата</option>
              <option value="Служебная проверка">Служебная проверка</option>
              <option value="Служебное расследование">Служебное расследование</option>
              <option value="Другое">Другое</option>
            </select>
          </div>
        </div>
        <div class="mb-3 row required">
          <label class="col-form-label col-lg-2" for="results">Результат</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="results" name="results" required v-model="storeAnketa.itemForm.poligraf['results']"></textarea>
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
      <table v-if="storeProfile.pfo.length" v-for="tbl in storeProfile.pfo" :key="tbl['id' as keyof typeof tbl]" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
            <th>
              <a href="#" @click="storeProfile.deleteItem(tbl['id'].toString(), 'poligraf')" title="Удалить">
                <i class="bi bi-trash"></i>
              </a>
              &nbsp;
              <a href="#" @click="storeAnketa.action = 'update'; storeAnketa.itemId = tbl['id']; storeAnketa.itemForm = tbl"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Изменить" >
                          <i class="bi bi-pencil-square"></i></a>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Тема</td><td>{{ tbl['theme' as keyof typeof tbl] }}</td></tr>
          <tr><td>Результат</td><td>{{ tbl['results' as keyof typeof tbl] }}</td></tr>
          <tr><td>Полиграфолог</td><td>{{ tbl['officer' as keyof typeof tbl] }}</td></tr>
          <tr>
            <td>Дата</td>
            <td>{{ new Date(String(tbl['deadline' as keyof typeof tbl])).toLocaleDateString('ru-RU') }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
      <button @click="storeAnketa.action = 'create'; storeAnketa.itemForm = {}; storeAnketa.itemId = ''" class="btn btn-outline-primary" type="button">Добавить запись</button>
    </template>
  
  </div>
</template>