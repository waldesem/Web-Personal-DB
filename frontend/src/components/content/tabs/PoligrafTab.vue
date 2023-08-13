<script setup lang="ts">
// компонент для отображения и редактирования данных полиграфа

import { ref } from 'vue';

const emit = defineEmits(['updateItem', 'deleteItem']);

// данные из родительского компонента
const props = defineProps({
  table: Array as () => Array<TableItem>,
  candId: String
});

type TableItem = {
  id: string;
  theme: string;
  result: string;
  officer: string;
  deadline: Date;
};

// реактивные данные для показа в форме
const poligraf = ref({});
  
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
  url = 'poligraf', 
  actions = action.value, 
  item_id = poligraf['id' as keyof typeof poligraf],
  item = poligraf
  ): void {
    event.preventDefault();
    emit('updateItem', id, url, actions, item_id, item);
    action.value = '';
    poligraf.value = {};
  };

</script>

<template>
  <div class="py-3">
    
    <template v-if="action">
      <form @submit.prevent="event => updateItem(event)" class="form form-check" role="form"  id="poligrafFormId">
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="theme">Тема проверки</label>
          <div class="col-lg-10">
            <select class="form-select" id="theme" name="theme" required v-model="poligraf['theme' as keyof typeof poligraf]">
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
            <textarea class="form-control" id="results" name="results" required v-model="poligraf['results' as keyof typeof poligraf]"></textarea>
          </div>
        </div>
        <div class=" row">
          <div class="offset-lg-2 col-lg-10">
            <div class="btn-group" role="group">
              <button class="btn btn-outline-primary" type="submit">Принять</button>
              <button class="btn btn-outline-primary" type="reset">Очистить</button>
              <button class="btn btn-outline-primary" type="button" @click="action = ''; poligraf = {};">Отмена</button>
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
                           @click="emit('deleteItem', tbl['id' as keyof typeof tbl].toString(), 'poligraf')"
                           data-bs-toggle="tooltip" data-bs-placement="right" title="Удалить">
                          <i class="bi bi-trash"></i></a>
              <a href="#" :class="{isHovered ? 'link-opacity-75' : 'd-none'}"
                          @click="action = 'update'; poligraf = tbl"
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
      <button @click="action = 'create'" class="btn btn-outline-primary" type="button">Добавить запись</button>
    </template>
  
  </div>
</template>