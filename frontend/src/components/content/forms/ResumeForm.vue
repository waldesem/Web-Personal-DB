<script setup lang="ts">
// компонент формы добавления или редактирования резюе

import { profileStore } from '@/store/profile';
import { authStore } from '@/store/token';
import { alertStore } from '@store/alert';
import { loginStore } from '@/store/login';
import router from '@/router/router';
import server from '@/store/server';

const storeProfile = profileStore();
const storeAuth = authStore()
const storeAlert = alertStore();
const storeLogin = loginStore();

  /**
   * Submits the data to the server to create a new resume.
   *
   * @return {Promise<void>} A promise that resolves when the data has been 
   * successfully submitted.
   */
   async function submitResume(): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.post(
        `${server}/resume/${storeProfile.action}`, storeProfile.itemForm
        );
      const { message } = response.data;

      storeAlert.setAlert(storeProfile.action === "create" 
                            ? "alert-success" : "alert-info", 
                            storeProfile.action === "create"
                            ? 'Анкета успешно добавлена' 
                            : 'Анкета успешно обновлена');

      storeProfile.action === 'create' 
        ? router.push({ name: 'profile', params: { id: message } })
        : storeProfile.getItem('resume');
      
        storeProfile.cancelEdit();
      
    } catch (error) {
      console.error(error);
    }
  };

  /**
   * Redirects to the main page.
   *
   * @return {void} No return value.
   */
   function redirectMain(): void {
    router.push({ name: 'persons', params: { group: storeLogin.pageIdentity } })
  };

</script>
<template>
  <div class="py-3">
    <form @submit.prevent="submitResume" class="form form-check" role="form">
      <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="category">Категория</label>
        <div class="col-lg-10">
          <select class="form-select" required id="category" name="category" 
                  v-model="storeProfile.itemForm['category']">
            <option value="Кандидат">Кандидат</option>
            <option value="Проверяемое лицо">Проверяемое лицо</option>
          </select>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="fullname">Полное ФИО*</label>
        <div class="col-lg-10">
            <input class="form-control" maxlength="250" id="fullname" name="fullname" type="text"
                   v-model="storeProfile.itemForm['fullname']" required>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="previous">Изменение имени</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="250" id="previous" name="previous" type="text"
                 v-model="storeProfile.itemForm['previous']">
        </div>
        </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="birthday">Дата рождения*</label>
        <div class="col-lg-10">
          <input class="form-control" id="birthday" name="birthday" required type="date"
                 v-model="storeProfile.itemForm['birthday']" 
                 :max="new Date().toISOString().split('T')[0]">
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="birthplace">Место рождения</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="250" id="birthplace" name="birthplace" type="text"
                 v-model="storeProfile.itemForm['birthplace']" >
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="country">Гражданство</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="50" id="country" name="country" type="text"
                 v-model="storeProfile.itemForm['country']" >
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="snils">СНИЛС</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="11" minlength="11" id="snils" name="snils" type="text"
                 v-model="storeProfile.itemForm['snils']" >
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="inn">ИНН</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="12" minlength="12" id="inn" name="inn" type="text"
                 v-model="storeProfile.itemForm['inn']" >
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="education">Образование</label>
        <div class="col-lg-10">
          <input class="form-control" maxlength="250" id="education" name="education" type="text"
                 v-model="storeProfile.itemForm['education']" >
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="addition">Дополнительно</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="addition" name="addition"
                    v-model="storeProfile.itemForm['addition']" ></textarea>
        </div>
      </div>
      <div class=" row">
        <div class="offset-lg-2 col-lg-10">
          <div class="btn-group" role="group">
            <button class="btn btn-outline-primary" type="submit">Принять</button>
            <button class="btn btn-outline-primary" type="reset">Очистить</button>
            <button v-if="storeProfile.action !== 'update'" 
                    class="btn btn-outline-primary" type="button"       
                    @click="redirectMain">Отмена</button>
            <button v-else class="btn btn-outline-primary" type="button" 
                    @click="storeProfile.cancelEdit">Отмена</button>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>
