<script setup lang="ts">
// компонент для отображения и редактирования данных расследований

import { ref } from 'vue';

const emit = defineEmits(['updateItem', 'deleteItem']);

const props = defineProps({
  table: Array as () => Array<TableItem>,
  candId: String
});

type TableItem = {
  id: string;
  theme: string;
  info: string;
  officer: string;
  deadline: Date;
};

// реактивные данные для показа в форме
const investigation = ref({});
  
const action = ref(''); // action для редактирования

//const isHovered = ref(false); // переменная для ховеров


function updateItem(
  event: Event,
  id = props.candId, 
  url = 'investigation', 
  actions = action.value, 
  item_id = investigation['id' as keyof typeof investigation],
  item = investigation
  ): void {
    event.preventDefault();
    emit('updateItem', id, url, actions, item_id, item);
    action.value = '';
    investigation.value = {};
  };

</script>

<template>
  <div class="py-3">
    <template v-if="action">
      <form @submit.prevent="event => updateItem(event)" class="form form-check" role="form"  id="investigationFormId">
        <div class="mb-3 row required">
          <label class="col-form-label col-lg-2" for="theme">Тема проверки</label>
          <div class="col-lg-10">
            <input class="form-control" id="theme" maxlength="250" name="theme" required type="text" v-model="investigation['theme' as keyof typeof investigation]">
          </div>
        </div>
        <div class="mb-3 row required">
          <label class="col-form-label col-lg-2" for="info">Информация</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="info" name="info" required v-model="investigation['info' as keyof typeof investigation]"></textarea>
          </div>
        </div>
        <div class=" row">
          <div class="offset-lg-2 col-lg-10">
            <div class="btn-group" role="group">
                <button class="btn btn-outline-primary" type="submit">Принять</button>
                <button class="btn btn-outline-primary" type="reset">Очистить</button>
                <button class="btn btn-outline-primary" type="button" @click="action = ''; investigation = {}">Отмена</button>
              </div>
            </div>
        </div>
      </form>
    </template>

    <template v-else>
      <table v-if="props.table?.length" v-for="tbl in props.table" class="table table-responsive">
        <thead>
          <tr>
            <th width="25%">{{ `#${tbl['id' as keyof typeof tbl]}` }}</th>
            <th>
              <a href="#" @click="emit('deleteItem', tbl['id' as keyof typeof tbl].toString(), 'investigation')"
                           data-bs-toggle="tooltip" data-bs-placement="right" title="Удалить">
                          <i class="bi bi-trash"></i></a>
                          &nbsp;
              <a href="#" @click="action = 'update'; investigation = tbl"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Изменить" >
                          <i class="bi bi-pencil-square"></i></a>
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
      <a @click="action = 'create'" class="btn btn-outline-primary" type="button">Добавить запись</a>
    </template>
  </div>
</template>