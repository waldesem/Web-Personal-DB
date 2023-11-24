<script setup lang="ts">

import { ref, defineAsyncComponent } from 'vue';
import { profileStore } from '@/store/profile';
import { classifyStore } from '@store/classify';

const TextLabel = defineAsyncComponent(() => import('@components/elements/TextLabel.vue'));
const SelectDiv = defineAsyncComponent(() => import('@components/elements/SelectDiv.vue'));
const BtnGroupForm = defineAsyncComponent(() => import('@components/elements/BtnGroupForm.vue'));

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

<template v-if="(storeProfile.action === 'update' || storeProfile.action === 'create')
               && storeProfile.flag === 'check'">
  <div class="form-check form-switch">
    <input class="form-check-checkbox" role="switch" id="checkbox" name="check" type="checkbox"
           v-model="noNegative">
    <label class="form-check-label" for="checkbox">Негатива нет</label>
  </div>

  <form @submit.prevent="storeProfile.dataProfile.updateItem" 
        class="form form-check" role="form"  id="checkFormId">
    <TextLabel :name="'workplace'" :label="'Проверка по местам работы'"
                :model="storeProfile.dataProfile.form['workplace']"/>
    <TextLabel :name="'employee'" :label="'Проверка по кадровому учету'"
                :model="storeProfile.dataProfile.form['employee']"/>
    <TextLabel :name="'document'" :label="'Проверка документов'"
                :model="storeProfile.dataProfile.form['document']"/>
    <TextLabel :name="'inn'" :label="'Проверка ИНН'"
                :model="storeProfile.dataProfile.form['inn']"/>
    <TextLabel :name="'debt'" :label="'Проверка задолженностей'"
                :model="storeProfile.dataProfile.form['debt']"/>
    <TextLabel :name="'bankruptcy'" :label="'Проверка решений о признании банкротом'"
                :model="storeProfile.dataProfile.form['bankruptcy']"/>
    <TextLabel :name="'bki'" :label="'Проверка кредитной истории'"
                :model="storeProfile.dataProfile.form['bki']"/>
    <TextLabel :name="'courts'" :label="'Проверка судебных дел'"
                :model="storeProfile.dataProfile.form['courts']"/>
    <TextLabel :name="'affiliation'" :label="'Проверка аффилированности'"
                :model="storeProfile.dataProfile.form['affiliation']"/>
    <TextLabel :name="'terrorist'" :label="'Проверка в списке террористов'"
                :model="storeProfile.dataProfile.form['terrorist']"/>
    <TextLabel :name="'mvd'" :label="'Проверка в розыск'"
                :model="storeProfile.dataProfile.form['mvd']"/>
    <TextLabel :name="'internet'" :label="'Проверка в открытых источниках'"
                :model="storeProfile.dataProfile.form['internet']"/>
    <TextLabel :name="'cronos'" :label="'Проверка в Кронос'"
                :model="storeProfile.dataProfile.form['cronos']"/>
    <TextLabel :name="'cros'" :label="'Проверка в Крос'"
                :model="storeProfile.dataProfile.form['cros']"/>
    <TextLabel :name="'addition'" :label="'Дополнительная информация'"
                :model="storeProfile.dataProfile.form['addition']"/>
    <div class=" row">
      <div class="offset-lg-2 col-lg-10">
        <div class="mb-3 form-check">
          <input class="form-check-input" id="pfo" name="pfo" 
                  v-model="storeProfile.dataProfile.form['pfo']" type="checkbox" value="y">
          <label class="form-check-label" for="pfo">Полиграф</label>
        </div>
      </div>
    </div>
    <SelectDiv :name="'conclusion'" :label="'Результат'"
               :select="storeClassify.classData.conclusion"
               :model="storeProfile.dataProfile.form['conclusion']"/>
    <TextLabel :name="'comments'" :label="'Комментарий'"
                :model="storeProfile.dataProfile.form['comments']"/>
    <BtnGroupForm>
      <button class="btn btn-outline-primary" type="submit">Принять</button>
      <button class="btn btn-outline-primary" type="reset">Очистить</button>
      <button class="btn btn-outline-primary" type="button" 
              @click="cancelCheck">Отмена</button>
    </BtnGroupForm>
  </form>
</template>