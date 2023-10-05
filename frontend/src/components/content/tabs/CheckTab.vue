<script setup lang="ts">

import { classifyStore } from '@store/classify';
import { profileStore } from '@/store/profile';
import { loginStore } from '@store/login';

const classifyApp = classifyStore();
const storeProfile = profileStore();
const storeLogin = loginStore();

/**
 * Cancels the check.
 *
 * @return {Promise<void>} Returns a promise that resolves when the check is cancelled.
 */
  async function cancelCheck(): Promise<void> {
  if (storeProfile.profile.resume['status'] !== classifyApp.classifyItems.status['save']) {
    storeProfile.getItem('resume', 'status', storeProfile.candId);
  };
  storeProfile.cancelEdit();
};

</script>

<template>
  <div class="py-3">

    <template v-if="storeProfile.action === 'update' && storeProfile.flag === 'check'">

      <form @submit.prevent="storeProfile.updateItem" 
          class="form form-check" role="form"  id="checkFormId">
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="workplace">
            Проверка по месту работы
          </label>
          <div class="col-lg-10">
            <textarea class="form-control" id="workplace" name="workplace" 
                      v-model="storeProfile.itemForm['workplace']"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="employee">
            Проверка по кадровому учету
          </label>
          <div class="col-lg-10">
            <textarea class="form-control" id="employee" name="employee" 
                      v-model="storeProfile.itemForm['employee']"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="document">
            Проверка документов
          </label>
          <div class="col-lg-10">
            <textarea class="form-control" id="document" name="document" 
                      v-model="storeProfile.itemForm['document']"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="inn">
            Проверка ИНН
          </label>
          <div class="col-lg-10">
            <textarea class="form-control" id="inn" name="inn" 
                      v-model="storeProfile.itemForm['inn']"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="debt">
            Проверка задолженностей
          </label>
          <div class="col-lg-10">
            <textarea class="form-control" id="debt" name="debt" 
                      v-model="storeProfile.itemForm['debt']"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="bankruptcy">
            Проверка банкротства
          </label>
          <div class="col-lg-10">
            <textarea class="form-control" id="bankruptcy" name="bankruptcy" 
                      v-model="storeProfile.itemForm['bankruptcy']"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="bki">
            Проверка кредитной истории
          </label>
          <div class="col-lg-10">
            <textarea class="form-control" id="bki" name="bki" 
                      v-model="storeProfile.itemForm['bki']"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="courts">
            Проверка по решениям судов
          </label>
          <div class="col-lg-10">
            <textarea class="form-control" id="courts" name="courts" 
                      v-model="storeProfile.itemForm['courts']"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="affiliation">
            Проверка аффилированности
          </label>
          <div class="col-lg-10">
            <textarea class="form-control" id="affiliation" name="affiliation" 
                      v-model="storeProfile.itemForm['affiliation']"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="terrorist">
            Проверка списка террористов
          </label>
          <div class="col-lg-10">
            <textarea class="form-control" id="terrorist" name="terrorist" 
                      v-model="storeProfile.itemForm['terrorist']"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="mvd">
            Проверка учетам МВД
          </label>
          <div class="col-lg-10">
            <textarea class="form-control" id="mvd" name="mvd" 
                      v-model="storeProfile.itemForm['mvd']"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="internet">
            Проверка по открытым источникам
          </label>
          <div class="col-lg-10">
            <textarea class="form-control" id="internet" name="internet" 
                      v-model="storeProfile.itemForm['internet']"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="cronos">
            Проверка Кронос
          </label>
          <div class="col-lg-10">
            <textarea class="form-control" id="cronos" name="cronos" 
                      v-model="storeProfile.itemForm['cronos']"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="cros">
            Проверка Крос
          </label>
          <div class="col-lg-10">
            <textarea class="form-control" id="cros" name="cros" 
                      v-model="storeProfile.itemForm['cros']"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="addition">
            Дополнительная информация
          </label>
          <div class="col-lg-10">
            <textarea class="form-control" id="addition" name="addition" 
                      v-model="storeProfile.itemForm['addition']"></textarea>
          </div>
        </div>
        <div class=" row">
          <div class="offset-lg-2 col-lg-10">
            <div class="mb-3 form-check">
              <input class="form-check-input" id="pfo" name="pfo" 
                     v-model="storeProfile.itemForm['pfo']" type="checkbox" value="y">
              <label class="form-check-label" for="pfo">Полиграф</label>
            </div>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="conclusion">
            Результат</label>
          <div class="col-lg-10">
            <select class="form-select" id="conclusion" name="conclusion" 
                    v-model="storeProfile.itemForm['conclusion']">
              <option v-for="(name, value) in classifyApp.classifyItems.conclusion" 
                      :key="value" :value="name">{{ name }}</option>
            </select>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="comments">Комментарий</label>
          <div class="col-lg-10">
            <input class="form-control" id="comments" name="comments" maxlength="250" 
                   v-model="storeProfile.itemForm['comments']" type="text">
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

    <template v-else>
      <table v-if="storeProfile.profile.verification?.length" 
             v-for="tbl in storeProfile.profile.verification" 
              :key="tbl['id']" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
            <th v-if="!storeProfile.printPdf">
              <a href="#" :disabled="classifyApp.classifyItems.status 
                          && (storeProfile.profile.resume['status'] === 
                              classifyApp.classifyItems.status['finish'])" 
                          @click="storeProfile.deleteItem(
                            'check', 'delete', tbl['id' as keyof typeof tbl].toString()
                            )"
                           title="Удалить">
                          <i class="bi bi-trash"></i></a>
                          &nbsp;
              <a href="#" :disabled="classifyApp.classifyItems.status 
                            && (storeProfile.profile.resume['status'] !== classifyApp.classifyItems.status['save'] 
                            && storeProfile.profile.resume['status'] !== classifyApp.classifyItems.status['cancel'] 
                            && storeProfile.profile.resume['status'] !== classifyApp.classifyItems.status['manual'])
                            || storeLogin.userData.region_id !== '1'" 
                          @click="storeProfile.action = 'update'; 
                                  storeProfile.flag = 'check';
                                  storeProfile.itemId = tbl['id' as keyof typeof tbl].toString(); 
                                  storeProfile.itemForm = tbl"
                          title="Изменить" >
                          <i class="bi bi-pencil-square"></i></a>
            </th>
            <th v-else></th>
          </tr>
        </thead>   
        <tbody>
          <tr>
            <td>Проверка по местам работы</td>
            <td>{{ tbl['workplace' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Бывший работник МТСБ</td>
            <td>{{ tbl['employee' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Проверка паспорта</td>
            <td>{{ tbl['document' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Проверка ИНН</td>
            <td>{{ tbl['inn' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Проверка ФССП</td>
            <td>{{ tbl['debt' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Проверка банкротства</td>
            <td>{{ tbl['bankruptcy' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Проверка БКИ</td>
            <td>{{ tbl['bki' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Проверка судебных дел</td>
            <td>{{ tbl['courts' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Проверка аффилированности</td>
            <td>{{ tbl['affiliation' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Проверка по списку террористов</td>
            <td>{{ tbl['terrorist' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Проверка нахождения в розыске</td>
            <td>{{ tbl['mvd' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Проверка в открытых источниках</td>
            <td>{{ tbl['internet' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Проверка Кронос</td>
            <td>{{ tbl['cronos' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Проверка Крос</td>
            <td>{{ tbl['cros' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Дополнительная информация</td>
            <td>{{ tbl['addition' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Материалы проверки</td>
            <td>{{ tbl['path' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>ПФО</td>
            <td>{{ tbl['pfo' as keyof typeof tbl] ? "Назначено" : "Не назначено" }}</td>
          </tr>
          <tr>
            <td>Комментарии</td>
            <td>{{ tbl['comments' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Результат проверки</td>
            <td>{{ tbl['conclusion' as keyof typeof tbl] }}</td>
          </tr>
          <tr>
            <td>Сотрудник</td>
            <td>
              <a href="#" @click="storeProfile.getItem('check', 'self', tbl['id' as keyof typeof tbl].toString())">
                {{ tbl['officer' as keyof typeof tbl] }}</a>
            </td>
          </tr>
          <tr>
            <td>Дата</td>
            <td>{{ new Date(String(tbl['deadline' as keyof typeof tbl])).toLocaleDateString('ru-RU') }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
      <button v-if="!storeProfile.printPdf" 
              @click="storeProfile.getItem('check', 'add')" 
              :disabled="![classifyApp.classifyItems.status['new'], 
                          classifyApp.classifyItems.status['update'], 
                          classifyApp.classifyItems.status['save'], 
                          classifyApp.classifyItems.status['repeat']].includes(storeProfile.profile.resume['status'])" 
        class="btn btn-outline-primary">Добавить проверку
      </button>
    </template>

  </div>
</template>