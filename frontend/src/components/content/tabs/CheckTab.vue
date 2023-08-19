<script setup lang="ts">
// компонент для отображения и редактирования проверок кандидата

import { ref } from 'vue';
import { appAuth } from '@store/auth';
import { appClassify } from '@store/classify';
import { appAlert } from '@/store/alert';
import { appProfile } from '@/store/profile';
import server from '@store/server';

const storeAuth = appAuth();

const classifyApp = appClassify();

const storeAlert = appAlert();

const storeProfile = appProfile();


// реактивные данные для показа в форме
const check = ref({
  workplace: '',
  employee: '',
  document: '',
  inn: '',
  debt: '',
  bankruptcy: '',
  bki: '',
  courts: '',
  affiliation: '',
  terrorist: '',
  mvd: '',
  internet: '',
  cronos: '',
  cros: '',
  addition: '',
  pfo: false,
  conclusion: '',
  comments: ''
});
  
const check_id = ref('');

const action = ref(''); // action для редактирования


async function addCheck() {
  if (storeProfile.status === classifyApp.status['save'] || 
    storeProfile.status === classifyApp.status['manual'] ||
    storeProfile.status === classifyApp.status['robot']) {
    
    storeAlert.alertAttr = 'alert-warning';
    storeAlert.alertText = 'Нельзя добавить проверку к текущему статусу';

  } else {
    try {
      const response = await storeAuth.axiosInstance.get(`${server}/check/add/${storeProfile.candId}`);
      const { message } = response.data;
      if (message === "manual") {
        storeAlert.alertAttr = 'alert-info';
        storeAlert.alertText = 'Начата ручная проверка';
        storeProfile.getProfile();
        
        // if (props.table) {
        //   console.log(props.table);

        //   action.value = 'update';
        //   const added_check = props.table[props.table.length - 1];
        //   if (added_check) {
        //     check_id.value = added_check['id' as keyof typeof added_check] as string;
        //     check.value = added_check as TableItem;
        //   }
        // }
      } else {
        action.value = '';

        storeAlert.alertAttr = 'alert-warning';
        storeAlert.alertText = 'Проверка кандидата уже начата';
      }

    } catch (error) {
      console.error(error)
    }
  }
};

/**
 * Updates an item.
 *
 * @return {void} This function does not return anything.
 */
 function updateItem(): void {
  storeProfile.updateItem(storeProfile.candId, 'check', action.value, check_id.value, {
      'workplace': check.value.workplace,
      'employee': check.value.employee,
      'document': check.value.document,
      'inn': check.value.inn,
      'debt': check.value.debt,
      'bankruptcy': check.value.bankruptcy,
      'bki': check.value.bki,
      'courts': check.value.courts,
      'affiliation': check.value.affiliation,
      'terrorist': check.value.terrorist,
      'mvd': check.value.mvd,
      'internet': check.value.internet,
      'cronos': check.value.cronos,
      'cros': check.value.cros,
      'addition': check.value.addition,
      'pfo': check.value.pfo,
      'conclusion': check.value.conclusion,
      'comments': check.value.comments
    })
    action.value = '';
  };


function deleteItem(id: string, flag: string): void {
  if ([classifyApp.status['robot'], classifyApp.status['finish']].includes(storeProfile.status)) {
    storeAlert.alertAttr = 'alert-warning';
    storeAlert.alertText = 'Нельзя удалить проверку с текущим статусом';

  } else {
    storeProfile.deleteItem(id, flag)
  }
};

async function cancelCheck() {
  if (storeProfile.status === classifyApp.status['save']) {
    action.value = '';
  } else {
    const response = await storeAuth.axiosInstance.get(`${server}/anketa/status/${storeProfile.candId}`);
    const { message } = response.data;
    storeAlert.alertAttr = message == 'update' ? "alert-success" : "alert-warning";
    storeAlert.alertText = message == 'update' ? "Отмена. Статус обновлен" : "Текущий статус обновить нельзя";
    window.scrollTo(0,0)
  }
}

</script>

<template>
  <div class="py-3">

    <template v-if="action">
      <form @submit.prevent="updateItem" class="form form-check" role="form"  id="checkFormId">
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="workplace">Проверка по месту работы</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="workplace" name="workplace" v-model="check.workplace"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="employee">Проверка по кадровому учету</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="employee" name="employee" v-model="check.employee"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="document">Проверка документов</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="document" name="document" v-model="check.document"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="inn">Проверка ИНН</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="inn" name="inn" v-model="check.inn"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="debt">Проверка задолженностей</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="debt" name="debt" v-model="check.debt"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="bankruptcy">Проверка банкротства</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="bankruptcy" name="bankruptcy" v-model="check.bankruptcy"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="bki">Проверка кредитной истории</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="bki" name="bki" v-model="check.bki"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="courts">Проверка по решениям судов</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="courts" name="courts" v-model="check.courts"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="affiliation">Проверка аффилированности</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="affiliation" name="affiliation" v-model="check.affiliation"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="terrorist">Проверка списка террористов</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="terrorist" name="terrorist" v-model="check.terrorist"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="mvd">Проверка учетам МВД</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="mvd" name="mvd" v-model="check.mvd"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="internet">Проверка по открытым источникам</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="internet" name="internet" v-model="check.internet"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="cronos">Проверка Кронос</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="cronos" name="cronos" v-model="check.cronos"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="cros">Проверка Крос</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="cros" name="cros" v-model="check.cros"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="addition">Дополнительная информация</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="addition" name="addition" v-model="check.addition"></textarea>
          </div>
        </div>
        <div class=" row">
          <div class="offset-lg-2 col-lg-10">
            <div class="mb-3 form-check">
              <input class="form-check-input" id="pfo" name="pfo" v-model="check['pfo' as keyof typeof check]" type="checkbox" value="y">
              <label class="form-check-label" for="pfo">Полиграф</label>
            </div>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="conclusion">Результат</label>
          <div class="col-lg-10">
            <select class="form-select" id="conclusion" name="conclusion" v-model="check['conclusion' as keyof typeof check]">
              <option v-for="(name, value) in classifyApp.conclusion" :key="value" :value="name">{{ name }}</option>
            </select>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="comments">Комментарий</label>
          <div class="col-lg-10">
            <input class="form-control" id="comments" name="comments" maxlength="250" v-model="check['comments' as keyof typeof check]" type="text">
          </div>
        </div>
        <div class=" row">
          <div class="offset-lg-2 col-lg-10">
            <div class="btn-group" role="group">
              <button class="btn btn-outline-primary" type="submit">Принять</button>
              <button class="btn btn-outline-primary" type="reset">Очистить</button>
              <button class="btn btn-outline-primary" type="button" @click="cancelCheck">Отмена</button>
            </div>
          </div>
        </div>
      </form>
    </template>

    <template v-else>
      <table v-if="storeProfile.verification?.length" v-for="tbl in storeProfile.verification" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
            <th>
              <a href="#" :disabled="classifyApp.status 
                          && (storeProfile.status === classifyApp.status['finish'])" 
                          @click="deleteItem(tbl['id' as keyof typeof tbl].toString(), 'check')"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Удалить">
                          <i class="bi bi-trash"></i></a>
                          &nbsp;
              <a href="#" :disabled="classifyApp.status 
                          && (storeProfile.status !== classifyApp.status['save'] 
                          && storeProfile.status !== classifyApp.status['cancel'] 
                          && storeProfile.status !== classifyApp.status['manual'])" 
                          @click="action = 'update'; check_id = tbl['id' as keyof typeof tbl].toString(); check = tbl"
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
        @click="addCheck" 
        :disabled="classifyApp.status 
        && (storeProfile.status !== classifyApp.status['new'] 
        && storeProfile.status !== classifyApp.status['update'])" 
        class="btn btn-outline-primary">Добавить проверку
      </button>
    </template>

  </div>
</template>