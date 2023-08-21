<script setup lang="ts">
// компонент для отображения и редактирования проверок кандидата

import { appClassify } from '@store/classify';
import { appProfile } from '@/store/profile';
import { appAnketa } from '@/store/anketa';

const classifyApp = appClassify();

const storeProfile = appProfile();

const storeAnketa = appAnketa();

</script>

<template>
  <div class="py-3">

    <template v-if="storeAnketa.action === 'update'">
      <form @submit.prevent="storeAnketa.updateItem" class="form form-check" role="form"  id="checkFormId">
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="workplace">Проверка по месту работы</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="workplace" name="workplace" v-model="storeAnketa.itemForm.workplace"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="employee">Проверка по кадровому учету</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="employee" name="employee" v-model="storeAnketa.itemForm.employee"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="document">Проверка документов</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="document" name="document" v-model="storeAnketa.itemForm.document"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="inn">Проверка ИНН</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="inn" name="inn" v-model="storeAnketa.itemForm.inn"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="debt">Проверка задолженностей</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="debt" name="debt" v-model="storeAnketa.itemForm.debt"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="bankruptcy">Проверка банкротства</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="bankruptcy" name="bankruptcy" v-model="storeAnketa.itemForm.bankruptcy"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="bki">Проверка кредитной истории</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="bki" name="bki" v-model="storeAnketa.itemForm.bki"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="courts">Проверка по решениям судов</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="courts" name="courts" v-model="storeAnketa.itemForm.courts"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="affiliation">Проверка аффилированности</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="affiliation" name="affiliation" v-model="storeAnketa.itemForm.affiliation"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="terrorist">Проверка списка террористов</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="terrorist" name="terrorist" v-model="storeAnketa.itemForm.terrorist"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="mvd">Проверка учетам МВД</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="mvd" name="mvd" v-model="storeAnketa.itemForm.mvd"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="internet">Проверка по открытым источникам</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="internet" name="internet" v-model="storeAnketa.itemForm.internet"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="cronos">Проверка Кронос</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="cronos" name="cronos" v-model="storeAnketa.itemForm.cronos"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="cros">Проверка Крос</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="cros" name="cros" v-model="storeAnketa.itemForm.cros"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="addition">Дополнительная информация</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="addition" name="addition" v-model="storeAnketa.itemForm.addition"></textarea>
          </div>
        </div>
        <div class=" row">
          <div class="offset-lg-2 col-lg-10">
            <div class="mb-3 form-check">
              <input class="form-check-input" id="pfo" name="pfo" v-model="storeAnketa.itemForm['pfo']" type="checkbox" value="y">
              <label class="form-check-label" for="pfo">Полиграф</label>
            </div>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="conclusion">Результат</label>
          <div class="col-lg-10">
            <select class="form-select" id="conclusion" name="conclusion" v-model="storeAnketa.itemForm['conclusion']">
              <option v-for="(name, value) in classifyApp.conclusion" :key="value" :value="name">{{ name }}</option>
            </select>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="comments">Комментарий</label>
          <div class="col-lg-10">
            <input class="form-control" id="comments" name="comments" maxlength="250" v-model="storeAnketa.itemForm['comments']" type="text">
          </div>
        </div>
        <div class=" row">
          <div class="offset-lg-2 col-lg-10">
            <div class="btn-group" role="group">
              <button class="btn btn-outline-primary" type="submit">Принять</button>
              <button class="btn btn-outline-primary" type="reset">Очистить</button>
              <button class="btn btn-outline-primary" type="button" @click="storeAnketa.cancelCheck">Отмена</button>
            </div>
          </div>
        </div>
      </form>
    </template>

    <template v-else>
      <table v-if="storeProfile.verification?.length" v-for="tbl in storeProfile.verification" :key="tbl['id']" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
            <th>
              <a href="#" :disabled="classifyApp.status 
                          && (storeProfile.anketa.resume['status'] === classifyApp.status['finish'])" 
                          @click="storeAnketa.deleteCheck(tbl['id' as keyof typeof tbl].toString(), 'check')"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Удалить">
                          <i class="bi bi-trash"></i></a>
                          &nbsp;
              <a href="#" :disabled="classifyApp.status 
                          && (storeProfile.anketa.resume['status'] !== classifyApp.status['save'] 
                          && storeProfile.anketa.resume['status'] !== classifyApp.status['cancel'] 
                          && storeProfile.anketa.resume['status'] !== classifyApp.status['manual'])" 
                          @click="storeAnketa.action = 'update'; storeAnketa.itemId = tbl['id' as keyof typeof tbl].toString(); storeAnketa.itemForm = tbl"
                          title="Изменить" >
                          <i class="bi bi-pencil-square"></i></a>
            </th>
          </tr>
        </thead>   
        <tbody>
          <tr><td width="25%">Проверка по местам работы</td><td>{{ tbl['workplace' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Бывший работник МТСБ</td><td>{{ tbl['employee' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Проверка паспорта</td><td>{{ tbl['document' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Проверка ИНН</td><td>{{ tbl['inn' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Проверка ФССП</td><td>{{ tbl['debt' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Проверка банкротства</td><td>{{ tbl['bankruptcy' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Проверка БКИ</td><td>{{ tbl['bki' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Проверка судебных дел</td><td>{{ tbl['courts' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Проверка аффилированности</td><td>{{ tbl['affiliation' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Проверка по списку террористов</td><td>{{ tbl['terrorist' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Проверка нахождения в розыске</td><td>{{ tbl['mvd' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Проверка в открытых источниках</td><td>{{ tbl['internet' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Проверка Кронос</td><td>{{ tbl['cronos' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Проверка Крос</td><td>{{ tbl['cros' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Дополнительная информация</td><td>{{ tbl['addition' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Материалы проверки</td><td>{{ tbl['path' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">ПФО</td><td>{{ tbl['pfo' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Комментарии</td><td>{{ tbl['comments' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Результат проверки</td><td>{{ tbl['conclusion' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Сотрудник</td><td>{{ tbl['officer' as keyof typeof tbl] }}</td></tr>
          <tr><td width="25%">Дата</td><td>{{ new Date(String(tbl['deadline' as keyof typeof tbl])).toLocaleDateString('ru-RU') }}</td></tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
      <button 
        @click="storeAnketa.addCheck; 
                storeAnketa.flag = 'check'" 
        :disabled="classifyApp.status 
        && (storeProfile.anketa.resume['status'] !== classifyApp.status['new'] 
        && storeProfile.anketa.resume['status'] !== classifyApp.status['update'])" 
        class="btn btn-outline-primary">Добавить проверку
      </button>
    </template>

  </div>
</template>