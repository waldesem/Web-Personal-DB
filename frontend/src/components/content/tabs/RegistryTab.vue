<script setup lang="ts">
// компонент для отображения данных согласования кандидата

import { ref } from 'vue';
import { appClassify } from '@store/classify';

const emit = defineEmits(['updateItem']);

const classifyApp = appClassify();

// Данные из родительского компонента: все согласования кандидата и ID
const props = defineProps({
  table: Array as () => Array<TableItem>,
  candId: String
});

type TableItem = {
  id: string;
  comments: string;
  decision: string;
  supervisor: string;
  deadline: Date;
};

// реактивные данные для показа в форме
const registry = ref({});
  
const action = ref(''); // action для редактирования

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
  url = 'registry', 
  actions = action.value, 
  item_id = registry['id' as keyof typeof registry],
  item = registry
  ): void {
    event.preventDefault();
    emit('updateItem', id, url, actions, item_id, item);
    action.value = '';
    registry.value = {};
  };

</script>

<template>
  <div class="py-3">

    <template v-if="action">
      <form @submit.prevent="event => updateItem(event)" class="form form-check" role="form"  id="registryFormId">
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="comments">Комментарий</label>
          <div class="col-lg-10">
            <textarea class="form-control" id="comments" name="comments" v-model="registry['comments' as keyof typeof registry]"></textarea>
          </div>
        </div>
        <div class="mb-3 row">
          <label class="col-form-label col-lg-2" for="decision">Решение</label>
          <div class="col-lg-10">
            <select class="form-select" id="decision" name="decision" v-model="registry['decision' as keyof typeof registry]">
              <option v-for="(name, value) in classifyApp.decision" :key="name"  :value="value">{{ value }}</option>
            </select>
          </div>
        </div>
        <div class=" row">
          <div class="offset-lg-2 col-lg-10">
            <div class="btn-group" role="group">
              <button class="btn btn-outline-primary" type="submit">Принять</button>
              <button class="btn btn-outline-primary" type="reset">Очистить</button>
              <button class="btn btn-outline-primary" type="button" @click="action = ''; registry = {}">Отмена</button>
            </div>
          </div>
        </div>
      </form>
    </template>

    <template v-else>
      <table v-if="props.table?.length" v-for="tbl in props.table" class="table table-responsive">
        <thead>
          <tr><th width="25%">{{ `#${tbl['id']}` }}</th><th></th></tr>
        </thead>
        <tbody>
          <tr><td>Комментарий</td><td>{{ tbl['comments'] }}</td></tr>
          <tr><td>Решение</td><td>{{ tbl['decision'] }}</td></tr>
          <tr><td>Согласующий</td><td>{{ tbl['supervisor'] }}</td></tr>
          <tr><td>Дата</td><td>{{ new Date(tbl['deadline']).toLocaleDateString('ru-RU') }}</td></tr>
        </tbody>
      </table>
      <p v-else >Данные отсутствуют</p>
      <button @click="action = 'create'" class="btn btn-outline-primary" type="button">Добавить запись</button>
    </template>
  
  </div>
</template>