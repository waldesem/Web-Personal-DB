<script setup lang="ts">
// компонент для отображения и редактирования данных запросов

import { ref } from 'vue';

const emit = defineEmits(['updateItem', 'deleteItem']);

const props = defineProps({
  table: Array as () => Array<TableItem>,
  candId: String
});

type TableItem = {
  id: string;
  info: string;
  innitiator: string;
  source: string;
  officer: string;
  deadline: Date;
};

// реактивные данные для показа в форме
const inquiry = ref({});
  
const action = ref(''); // action для редактирования

const isHovered = ref(false); // переменная для ховеров

/**
 * Updates an item.
 *
 * @param {Event} event - The event that triggered the update.
 * @param {type} id - The ID of the person to be updated.
 * @param {string} url - The URL to be updated.
 * @param {type} actions - The actions to be performed during the update.
 * @param {type} item_id - The ID of the item to be updated.
 * @param {type} item - The item to be updated.
 * @return {void} This function does not return anything.
 */
function updateItem(
  event: Event,
  id = props.candId, 
  url = 'inquiry', 
  actions = action.value, 
  item_id = inquiry['id' as keyof typeof inquiry],
  item = inquiry
  ): void {
    event.preventDefault();
    emit('updateItem', id, url, actions, item_id, item);
    action.value = '';
    inquiry.value = {};
  };


</script>

<template>
  <div class="py-3">
    <template v-if="action">
      <form @submit.prevent="event => updateItem(event)" class="form form-check" role="form"  id="inquiryFormId">
        <div class="mb-3 row required">
          <label class="col-form-label col-lg-2" for="info">Информация</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="info" name="info" required v-model="inquiry['info' as keyof typeof inquiry]"></textarea>
          </div>
        </div>
        <div class="mb-3 row required">
          <label class="col-form-label col-lg-2" for="initiator">Инициатор</label>
          <div class="col-lg-10">
            <input class="form-control" id="initiator" maxlength="250" name="initiator" required type="text" v-model="inquiry['initiator' as keyof typeof inquiry]">
          </div>
        </div>
        <div class="mb-3 row required">
          <label class="col-form-label col-lg-2" for="source">Источник</label>
          <div class="col-lg-10">
            <input class="form-control" id="source" maxlength="250" name="source" required type="text" v-model="inquiry['source' as keyof typeof inquiry]">
          </div>
        </div>
        <div class=" row">
          <div class="offset-lg-2 col-lg-10">
            <div class="btn-group" role="group">
                <button class="btn btn-outline-primary" type="submit">Принять</button>
                <button class="btn btn-outline-primary" type="reset">Очистить</button>
                <button class="btn btn-outline-primary" type="button" @click="action = ''; inquiry = {}">Отмена</button>
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
            <th @mouseover="isHovered = true" @mouseout="isHovered = false">
              <a href="#" :class="{isHovered ? 'link-opacity-75' : 'd-none'}"
                           @click="emit('deleteItem', tbl['id' as keyof typeof tbl].toString(), 'inquiry')"
                           data-bs-toggle="tooltip" data-bs-placement="right" title="Удалить">
                          <i class="bi bi-trash"></i></a>
              <a href="#" :class="{isHovered ? 'link-opacity-75' : 'd-none'}"
                          @click="action = 'update'; inquiry = tbl"
                          data-bs-toggle="tooltip" data-bs-placement="right" title="Изменить" >
                          <i class="bi bi-pencil-square"></i></a>
            </th>
          </tr>
        </thead>        
        <tbody>
          <tr><td>Информация</td><td>{{ tbl['info' as keyof typeof tbl] }}</td></tr>
          <tr><td>Иннициатор</td><td>{{ tbl['initiator' as keyof typeof tbl] }}</td></tr>
          <tr><td>Источник</td><td>{{ tbl['source' as keyof typeof tbl] }}</td></tr>
          <tr><td>Сотрудник</td><td>{{ tbl['officer' as keyof typeof tbl] }}</td></tr>
          <tr>
            <td>Дата запроса</td>
            <td>{{ new Date(String(tbl['deadline' as keyof typeof tbl])).toLocaleDateString('ru-RU') }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
      <a @click="action = 'create'" class="btn btn-outline-primary" type="button">Добавить запись</a>
    </template>
  </div>
</template>