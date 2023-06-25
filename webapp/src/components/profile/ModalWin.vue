<template>
  <div class="modal fade" id="modalWin" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="modalWinLabel" aria-hidden="true">
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="modalWinLabel">Добавить запись</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">

          <form v-if="path == 'staff'" @submit.prevent="submitData" class="form form-check" role="form">
            <div class="mb-3 row required">
              <label class="col-form-label col-lg-2" for="position">Должность</label>
              <div class="col-lg-10">
                <input class="form-control" id="position" maxlength="250" name="position" required type="text" value="">
              </div>
            </div>
            <div class="mb-3 row">
              <label class="col-form-label col-lg-2" for="department">Деператамент/Кластер</label>
              <div class="col-lg-10">
                <input class="form-control" id="department" maxlength="250" name="department" type="text" value="">
              </div>
            </div>
            <div class=" row">
              <div class="offset-lg-2 col-lg-10">
                <input class="btn btn-primary btn-md" data-bs-dismiss="modal" name="submit" type="submit" value="Принять">
              </div>
            </div>
          </form>

          <form v-else-if="path == 'document'" @submit.prevent="submitData" class="form form-check" role="form">
            <div class="mb-3 row">
              <label class="col-form-label col-lg-2" for="view">Выбрать</label>
              <div class="col-lg-10">
                <select class="form-select" id="view" name="view"><option value="Паспорт гражданина России">Паспорт гражданина России</option><option value="Иностранный документ">Иностранный документ</option><option value="Другое">Другое</option></select>
              </div>
            </div>
            <div class="mb-3 row">
              <label class="col-form-label col-lg-2" for="series">Серия документа</label>
              <div class="col-lg-10">
                <input class="form-control" id="series" maxlength="25" name="series" type="text" value="">
              </div>
            </div>
            <div class="mb-3 row required">
              <label class="col-form-label col-lg-2" for="number">Номер документа</label>
              <div class="col-lg-10">
                <input class="form-control" id="number" maxlength="25" name="number" required type="text" value="">
              </div>
            </div>
            <div class="mb-3 row">
              <label class="col-form-label col-lg-2" for="agency">Орган выдавший</label>
              <div class="col-lg-10">
                <input class="form-control" id="agency" maxlength="250" name="agency" type="text" value="">
              </div>
            </div>
            <div class="mb-3 row required">
              <label class="col-form-label col-lg-2" for="issue">Дата выдачи</label>
              <div class="col-lg-10">
                <input class="form-control" id="issue" name="issue" required type="date" value="">
              </div>
            </div>
            <div class=" row">
              <div class="offset-lg-2 col-lg-10">
                <input class="btn btn-primary btn-md" data-bs-dismiss="modal" name="submit" type="submit" value="Принять">
              </div>
            </div>
          </form>
          
          <form v-else-if="path == 'address'" @submit.prevent="submitData" class="form form-check" role="form">
            <div class="mb-3 row">
              <label class="col-form-label col-lg-2" for="view">Выбрать</label>
              <div class="col-lg-10">
                <select class="form-select" id="view" name="view">
                  <option value="Адрес регистрации">Адрес регистрации</option>
                  <option value="Адрес проживания">Адрес проживания</option>
                  <option value="Другое">Другое</option>
                </select>
              </div>
            </div>
            <div class="mb-3 row">
              <label class="col-form-label col-lg-2" for="region">Регион</label>
              <div class="col-lg-10">
                <input class="form-control" id="region" maxlength="250" name="region" type="text" value="">
              </div>
            </div>
            <div class="mb-3 row required">
              <label class="col-form-label col-lg-2" for="address">Полный</label>
              <div class="col-lg-10">
                <input class="form-control" id="address" maxlength="250" name="address" required type="text" value="">
              </div>
            </div>
            <div class=" row">
              <div class="offset-lg-2 col-lg-10">
                <input class="btn btn-primary btn-md" data-bs-dismiss="modal" name="submit" type="submit" value="Принять">
              </div>
            </div>
          </form>

          <form v-else-if="path == 'contact'" @submit.prevent="submitData" class="form form-check" role="form">
            <div class="mb-3 row">
              <label class="col-form-label col-lg-2" for="view">Выбрать</label>
              <div class="col-lg-10">
                <select class="form-select" id="view" name="view">
                  <option value="Телефон">Телефон</option>
                  <option value="E-mail">E-mail</option>
                  <option value="Другое">Другое</option>
                </select>
              </div>
            </div>
            <div class="mb-3 row required">
              <label class="col-form-label col-lg-2" for="contact">Контакт</label>
              <div class="col-lg-10">
                <input class="form-control" id="contact" maxlength="250" name="contact" required type="text" value="">
              </div>
            </div>
            <div class=" row">
              <div class="offset-lg-2 col-lg-10">
                <input class="btn btn-primary btn-md" data-bs-dismiss="modal" name="submit" type="submit" value="Принять">
              </div>
            </div>
          </form>
          
          <form v-else-if="path == 'workplace'" @submit.prevent="submitData" class="form form-check" role="form">
            <div class="mb-3 row">
              <label class="col-form-label col-lg-2" for="period">Период работы</label>
              <div class="col-lg-10">
                <input class="form-control" id="period" maxlength="25" name="period" type="text" value="">
              </div>
            </div>
            <div class="mb-3 row required">
              <label class="col-form-label col-lg-2" for="workplace">Место работы</label>
              <div class="col-lg-10">
                <input class="form-control" id="workplace" maxlength="250" name="workplace" required type="text" value="">
              </div>
            </div>
            <div class="mb-3 row">
              <label class="col-form-label col-lg-2" for="address">Адрес организации</label>
              <div class="col-lg-10">
                <input class="form-control" id="address" maxlength="250" name="address" type="text" value="">
              </div>
            </div>
            <div class="mb-3 row">
              <label class="col-form-label col-lg-2" for="position">Должность</label>
              <div class="col-lg-10">
                <input class="form-control" id="position" maxlength="250" name="position" type="text" value="">
              </div>
            </div>
            <div class=" row">
              <div class="offset-lg-2 col-lg-10">
                <input class="btn btn-primary btn-md" data-bs-dismiss="modal" name="submit" type="submit" value="Принять">
              </div>
            </div>
          </form>

        </div>
      </div>
    </div>
  </div>
</template>
  
<script setup lang="ts">

import axios from 'axios';
import { toRefs } from 'vue';
import appUrl from '@/config';

const props = defineProps({
    candId: String,
    path: String
});

const { path, candId } = toRefs(props);
  
const emit = defineEmits(['updateMessage', 'updateItem']);

async function submitData(event: Event) {
  try {
    const formData = new FormData(event.target as HTMLFormElement);
    const response = await axios.post(`${appUrl}/update/${path?.value}/${candId?.value}`, formData, {
      headers: {'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`
      }
    });
    const { message } = response.data;
    emit('updateMessage', {
      attr: "alert-success",
      text: message
    });
    emit('updateItem', {candId: candId?.value});
  } catch (error) {
    console.error(error);
  }
}

</script>