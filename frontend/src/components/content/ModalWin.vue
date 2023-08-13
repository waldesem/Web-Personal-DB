<script setup lang="ts">
// компонент для отображения модального окна

import { computed, ref } from 'vue';
import { locationStore } from '@/store/location';

const storeLocation = locationStore();

const emit = defineEmits(['updateItem']);

// данные из родительского компонента
const props = defineProps({
    candId: String,
    path: String,
    modal: Object,
    action: String
});

const modal = ref({}); // содержимое модального окна

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
  url = props.path, 
  actions = props.action, 
  item_id = modal['id' as keyof typeof modal],
  item = modal
  
  ): void {
    event.preventDefault();
    emit('updateItem', id, url, actions, item_id, item);
    modal.value = {};
  };


const name = computed(() => {
  // Матчинг заголовков модального окна
  const actionHeader = {
  'staff': 'должность',
  'document': 'документ',
  'address': 'адрес',
  'contact': "контакт",
  'workplace': "место работы", 
  'relation': 'связь',
  'location': 'регион'
  }
  return actionHeader[props.path as keyof typeof actionHeader]
});

</script>

<template>
  <div class="modal fade" id="modalWin" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="modalWinLabel" aria-hidden="true">
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="modalWinLabel">{{name === 'регион' ? 'Изменить регион' : 'Добавить ' + name}}</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">

          <form v-if="path == 'staff'" @submit.prevent="event => updateItem(event)" class="form form-check" role="form">
            <div class="mb-3 row required">
              <label class="col-form-label col-lg-2" for="position">Должность</label>
              <div class="col-lg-10">
                <input class="form-control" id="position" maxlength="250" name="position" required type="text" v-model="modal['position']">
              </div>
            </div>
            <div class="mb-3 row">
              <label class="col-form-label col-lg-2" for="department">Деператамент/Кластер</label>
              <div class="col-lg-10">
                <input class="form-control" id="department" maxlength="250" name="department" type="text" v-model="modal['department']">
              </div>
            </div>
            <div class=" row">
              <div class="offset-lg-2 col-lg-10">
                <button class="btn btn-primary btn-md" data-bs-dismiss="modal" name="submit" type="submit">Принять</button>
              </div>
            </div>
          </form>

          <form v-else-if="path == 'document'" @submit.prevent="event => updateItem(event)" class="form form-check" role="form">
            <div class="mb-3 row">
              <label class="col-form-label col-lg-2" for="view">Выбрать</label>
              <div class="col-lg-10">
                <select class="form-select" id="view" name="view" v-model="modal['view']">
                  <option value="Паспорт гражданина России">Паспорт гражданина России</option>
                  <option value="Иностранный документ">Иностранный документ</option>
                  <option value="Другое">Другое</option>
                </select>
              </div>
            </div>
            <div class="mb-3 row">
              <label class="col-form-label col-lg-2" for="series">Серия документа</label>
              <div class="col-lg-10">
                <input class="form-control" id="series" maxlength="25" name="series" type="text" v-model="modal['series']">
              </div>
            </div>
            <div class="mb-3 row required">
              <label class="col-form-label col-lg-2" for="number">Номер документа</label>
              <div class="col-lg-10">
                <input class="form-control" id="number" maxlength="25" name="number" required type="text" v-model="modal['number']">
              </div>
            </div>
            <div class="mb-3 row">
              <label class="col-form-label col-lg-2" for="agency">Орган выдавший</label>
              <div class="col-lg-10">
                <input class="form-control" id="agency" maxlength="250" name="agency" type="text" v-model="modal['agency']">
              </div>
            </div>
            <div class="mb-3 row required">
              <label class="col-form-label col-lg-2" for="issue">Дата выдачи</label>
              <div class="col-lg-10">
                <input class="form-control" id="issue" name="issue" required type="date" v-model="modal['issue']">
              </div>
            </div>
            <div class=" row">
              <div class="offset-lg-2 col-lg-10">
                <button class="btn btn-primary btn-md" data-bs-dismiss="modal" name="submit" type="submit">Принять</button>
              </div>
            </div>
          </form>
          
          <form v-else-if="path == 'address'" @submit.prevent="event => updateItem(event)" class="form form-check" role="form">
            <div class="mb-3 row">
              <label class="col-form-label col-lg-2" for="view">Выбрать</label>
              <div class="col-lg-10">
                <select class="form-select" id="view" name="view" v-model="modal['view']">
                  <option value="Адрес регистрации">Адрес регистрации</option>
                  <option value="Адрес проживания">Адрес проживания</option>
                  <option value="Другое">Другое</option>
                </select>
              </div>
            </div>
            <div class="mb-3 row">
              <label class="col-form-label col-lg-2" for="region">Регион</label>
              <div class="col-lg-10">
                <input class="form-control" id="region" maxlength="250" name="region" type="text" v-model="modal['region']">
              </div>
            </div>
            <div class="mb-3 row required">
              <label class="col-form-label col-lg-2" for="address">Полный</label>
              <div class="col-lg-10">
                <input class="form-control" id="address" maxlength="250" name="address" required type="text" v-model="modal['address']">
              </div>
            </div>
            <div class=" row">
              <div class="offset-lg-2 col-lg-10">
                <button class="btn btn-primary btn-md" data-bs-dismiss="modal" name="submit" type="submit">Принять</button>
              </div>
            </div>
          </form>

          <form v-else-if="path == 'contact'" @submit.prevent="event => updateItem(event)" class="form form-check" role="form">
            <div class="mb-3 row">
              <label class="col-form-label col-lg-2" for="view">Выбрать</label>
              <div class="col-lg-10">
                <select class="form-select" id="view" name="view" v-model="modal['view']">
                  <option value="Телефон">Телефон</option>
                  <option value="E-mail">E-mail</option>
                  <option value="Другое">Другое</option>
                </select>
              </div>
            </div>
            <div class="mb-3 row required">
              <label class="col-form-label col-lg-2" for="contact">Контакт</label>
              <div class="col-lg-10">
                <input class="form-control" id="contact" maxlength="250" name="contact" required type="text" v-model="modal['contact']">
              </div>
            </div>
            <div class=" row">
              <div class="offset-lg-2 col-lg-10">
                <button class="btn btn-primary btn-md" data-bs-dismiss="modal" name="submit" type="submit">Принять</button>
              </div>
            </div>
          </form>
          
          <form v-else-if="path == 'workplace'" @submit.prevent="event => updateItem(event)" class="form form-check" role="form">
            <div class="mb-3 row">
              <label class="col-form-label col-lg-2" for="period">Период работы</label>
              <div class="col-lg-10">
                <input class="form-control" id="period" maxlength="25" name="period" type="text" v-model="modal['period']">
              </div>
            </div>
            <div class="mb-3 row required">
              <label class="col-form-label col-lg-2" for="workplace">Место работы</label>
              <div class="col-lg-10">
                <input class="form-control" id="workplace" maxlength="250" name="workplace" required type="text" v-model="modal['workplace']">
              </div>
            </div>
            <div class="mb-3 row">
              <label class="col-form-label col-lg-2" for="address">Адрес организации</label>
              <div class="col-lg-10">
                <input class="form-control" id="address" maxlength="250" name="address" type="text" v-model="modal['address']">
              </div>
            </div>
            <div class="mb-3 row">
              <label class="col-form-label col-lg-2" for="position">Должность</label>
              <div class="col-lg-10">
                <input class="form-control" id="position" maxlength="250" name="position" type="text" v-model="modal['position']">
              </div>
            </div>
            <div class=" row">
              <div class="offset-lg-2 col-lg-10">
                <button class="btn btn-primary btn-md" data-bs-dismiss="modal" name="submit" type="submit">Принять</button>
              </div>
            </div>
          </form>

          <form v-else-if="path == 'relation'" @submit.prevent="event => updateItem(event)" class="form form-check" role="form">
            <div class="mb-3 row">
              <label class="col-form-label col-lg-2" for="relation">Тип связи</label>
              <div class="col-lg-10">
                <input class="form-control" id="relation" maxlength="250" name="relation" type="text" v-model="modal['relation']">
              </div>
            </div>
            <div class="mb-3 row">
              <label class="col-form-label col-lg-2" for="relation_id">ID связи</label>
              <div class="col-lg-10">
                <input class="form-control" id="relation_id" maxlength="25" name="relation_id" type="text" v-model="modal['relation_id']">
              </div>
            </div>
            <div class=" row">
              <div class="offset-lg-2 col-lg-10">
                <button class="btn btn-primary btn-md" data-bs-dismiss="modal" name="submit" type="submit">Принять</button>
              </div>
            </div>
          </form>
          
          <form v-else-if="path == 'location'" @submit.prevent="event => updateItem(event)" class="form form-check" role="form">
            <div class="mb-3 row">
              <label class="col-form-label col-lg-2" for="region">Регион</label>
              <div class="col-lg-10">
                <select class="form-select" required id="region" name="region" v-model="modal['region']">
                  <option v-for="name, value in storeLocation.regionsObject" :value="value">{{name}}</option>                
                </select>
              </div>
            </div>
            <div class=" row">
              <div class="offset-lg-2 col-lg-10">
                <button class="btn btn-primary btn-md" data-bs-dismiss="modal" name="submit" type="submit">Принять</button>
              </div>
            </div>
          </form>
    
        </div>
      </div>
    </div>
  </div>
</template>

<style>
      html,
      body {
          scrollbar-gutter: stable;
      }
</style>