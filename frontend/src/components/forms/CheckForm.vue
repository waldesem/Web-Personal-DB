<script setup lang="ts">

import { ref } from 'vue';
import { profileStore } from '@/store/profile';
import { classifyStore } from '@store/classify';

const storeProfile = profileStore();
const storeClassify = classifyStore();

const noNegative = ref(true);

if (noNegative.value) {
  Object.assign(storeProfile.dataProfile.form, {
    workplace: 'Негатива по местам работы не обнаружено', 
    employee: 'В числе бывших работников МТСБ не обнаружен', 
    document: 'Среди недействительных документов не обнаружен', 
    inn: 'ИНН соответствует паспорту', 
    debt: 'Задолженности не обнаружены', 
    bankruptcy: 'Решений о признании банкротом не имеется', 
    bki: 'Кредитная история не положительная', 
    courts: 'Судебные дела не обнаружены', 
    affiliation: 'Аффилированность не выявлена', 
    terrorist: 'В списке террористов не обнаружен', 
    mvd: 'В розыск не объявлен', 
    internet: 'В открытых источниках негатив не обнаружен', 
    cronos: 'В Кронос негатив не выявлен', 
    cros: 'В Крос негатив не выявлен', 
    addition: 'Дополнительная информация отсутствует', 
  });
};

/**
 * Cancels the check.
 *
 * @return {Promise<void>} Returns a promise that resolves when the check is cancelled.
 */
 async function cancelCheck(): Promise<void> {
  if (storeProfile.dataProfile.resume['status'] !== storeClassify.classData.status['save']) {
    storeProfile.dataProfile.getItem('resume', 'status', storeProfile.dataProfile.candId);
  };
  storeProfile.dataProfile.cancelEdit();
};

</script>

<template v-if="storeProfile.action === 'update'|| storeProfile.action === 'create' 
             && storeProfile.flag === 'check'">

  <div class="form-check form-switch">
    <input class="form-check-checkbox" role="switch" id="checkbox" name="check" type="checkbox"
           v-model="noNegative">
    <label class="form-check-label" for="checkbox">Негатива нет</label>
  </div>

  <form @submit.prevent="storeProfile.dataProfile.updateItem" 
      class="form form-check" role="form"  id="checkFormId">
    <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="workplace">
        Проверка по месту работы
      </label>
      <div class="col-lg-10">
        <textarea class="form-control" id="workplace" name="workplace" 
                  v-model="storeProfile.dataProfile.form['workplace']"></textarea>
      </div>
    </div>
    <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="employee">
        Проверка по кадровому учету
      </label>
      <div class="col-lg-10">
        <textarea class="form-control" id="employee" name="employee" 
                  v-model="storeProfile.dataProfile.form['employee']"></textarea>
      </div>
    </div>
    <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="document">
        Проверка документов
      </label>
      <div class="col-lg-10">
        <textarea class="form-control" id="document" name="document" 
                  v-model="storeProfile.dataProfile.form['document']"></textarea>
      </div>
    </div>
    <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="inn">
        Проверка ИНН
      </label>
      <div class="col-lg-10">
        <textarea class="form-control" id="inn" name="inn" 
                  v-model="storeProfile.dataProfile.form['inn']"></textarea>
      </div>
    </div>
    <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="debt">
        Проверка задолженностей
      </label>
      <div class="col-lg-10">
        <textarea class="form-control" id="debt" name="debt" 
                  v-model="storeProfile.dataProfile.form['debt']"></textarea>
      </div>
    </div>
    <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="bankruptcy">
        Проверка банкротства
      </label>
      <div class="col-lg-10">
        <textarea class="form-control" id="bankruptcy" name="bankruptcy" 
                  v-model="storeProfile.dataProfile.form['bankruptcy']"></textarea>
      </div>
    </div>
    <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="bki">
        Проверка кредитной истории
      </label>
      <div class="col-lg-10">
        <textarea class="form-control" id="bki" name="bki" 
                  v-model="storeProfile.dataProfile.form['bki']"></textarea>
      </div>
    </div>
    <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="courts">
        Проверка по решениям судов
      </label>
      <div class="col-lg-10">
        <textarea class="form-control" id="courts" name="courts" 
                  v-model="storeProfile.dataProfile.form['courts']"></textarea>
      </div>
    </div>
    <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="affiliation">
        Проверка аффилированности
      </label>
      <div class="col-lg-10">
        <textarea class="form-control" id="affiliation" name="affiliation" 
                  v-model="storeProfile.dataProfile.form['affiliation']"></textarea>
      </div>
    </div>
    <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="terrorist">
        Проверка списка террористов
      </label>
      <div class="col-lg-10">
        <textarea class="form-control" id="terrorist" name="terrorist" 
                  v-model="storeProfile.dataProfile.form['terrorist']"></textarea>
      </div>
    </div>
    <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="mvd">
        Проверка учетам МВД
      </label>
      <div class="col-lg-10">
        <textarea class="form-control" id="mvd" name="mvd" 
                  v-model="storeProfile.dataProfile.form['mvd']"></textarea>
      </div>
    </div>
    <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="internet">
        Проверка по открытым источникам
      </label>
      <div class="col-lg-10">
        <textarea class="form-control" id="internet" name="internet" 
                  v-model="storeProfile.dataProfile.form['internet']"></textarea>
      </div>
    </div>
    <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="cronos">
        Проверка Кронос
      </label>
      <div class="col-lg-10">
        <textarea class="form-control" id="cronos" name="cronos" 
                  v-model="storeProfile.dataProfile.form['cronos']"></textarea>
      </div>
    </div>
    <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="cros">
        Проверка Крос
      </label>
      <div class="col-lg-10">
        <textarea class="form-control" id="cros" name="cros" 
                  v-model="storeProfile.dataProfile.form['cros']"></textarea>
      </div>
    </div>
    <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="addition">
        Дополнительная информация
      </label>
      <div class="col-lg-10">
        <textarea class="form-control" id="addition" name="addition" 
                  v-model="storeProfile.dataProfile.form['addition']"></textarea>
      </div>
    </div>
    <div class=" row">
      <div class="offset-lg-2 col-lg-10">
        <div class="mb-3 form-check">
          <input class="form-check-input" id="pfo" name="pfo" 
                  v-model="storeProfile.dataProfile.form['pfo']" type="checkbox" value="y">
          <label class="form-check-label" for="pfo">Полиграф</label>
        </div>
      </div>
    </div>
    <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="conclusion">
        Результат</label>
      <div class="col-lg-10">
        <select class="form-select" id="conclusion" name="conclusion" 
                v-model="storeProfile.dataProfile.form['conclusion']">
          <option v-for="(name, value) in storeClassify.classData.conclusion" 
                  :key="value" :value="name">{{ name }}</option>
        </select>
      </div>
    </div>
    <div class="mb-3 row">
      <label class="col-form-label col-lg-2" for="comments">Комментарий</label>
      <div class="col-lg-10">
        <input class="form-control" id="comments" name="comments" maxlength="250" 
                v-model="storeProfile.dataProfile.form['comments']" type="text">
      </div>
    </div>
    <div class=" row">
      <div class="offset-lg-2 col-lg-10">
        <div class="btn-group" role="group">
          <button class="btn btn-outline-primary" type="submit">Принять</button>
          <button class="btn btn-outline-primary" type="reset">Очистить</button>
          <button class="btn btn-outline-primary" type="button" 
                  @click="cancelCheck">Отмена</button>
        </div>
      </div>
    </div>
  </form>
</template>