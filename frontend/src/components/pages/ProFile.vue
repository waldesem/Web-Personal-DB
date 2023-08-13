<script setup lang="ts">

import { onBeforeMount, ref } from 'vue';
import { useRoute } from 'vue-router';
import { appAuth } from '@store/auth';
import server from '@store/server';
import AnketaTab from '@content/tabs/AnketaTab.vue';
import CheckTab from '@content/tabs/CheckTab.vue';
import RegistryTab from '@content/tabs/RegistryTab.vue';
import PoligrafTab from '@content/tabs/PoligrafTab.vue';
import InvestigateTab from '@content/tabs/InvestigateTab.vue';
import InquiryTab from '@content/tabs/InquiryTab.vue';
import PhotoTab from '@content/tabs/PhotoTab.vue';

const storeAuth = appAuth()

const route = useRoute();

const emit = defineEmits(['updateMessage']);

const data = ref({
  candId: route.params.id.toString(), 
  resume: {},
  docums: [],
  addrs: [],
  conts: [],
  works: [],
  relate: [],
  staffs: [],
  verification: [], 
  register: [], 
  pfo: [], 
  inquisition: [], 
  needs: [], 
  status: '', 
  header: '',
  path: '',
  lastCheck: {}, 
  print: false
});


onBeforeMount(() => {
  getProfile(data.value.candId)
});

async function getProfile(id=data.value.candId) {
  data.value.candId = id;
  if (id === '0') {
    emit('updateMessage', {attr: 'alert-info', text: 'Заполните форму'})
    data.value.header = 'Новая анкета'

  } else {
    const response = await storeAuth.axiosInstance.get(`${server}/profile/${id}`);
    const {resume, documents, addresses, contacts, relations, workplaces, staffs, 
      checks, registries, pfos, invs, inquiries} = response.data;

    Object.assign(data.value, {
      resume: resume,
      docums: documents,
      addrs: addresses,
      conts: contacts,
      works: workplaces,
      staffs: staffs,
      relate: relations,
      verification: checks,
      register: registries,
      pfo: pfos,
      inquisition: invs,
      needs: inquiries,
      header: resume['fullname'],
      path: resume['path'],
      status: resume['status']
    })
  }
}

/**
 * Updates an item.
 *
 * @param {Event} event - The event object.
 * @param {string} id - The ID of the person.
 * @param {string} url - The URL of the item.
 * @param {string} actions - The actions to be performed on the item.
 * @param {string} item_id - The ID of the item.
 * @param {Object} item - The item object to be updated.
 * @return {Promise<void>} A promise that resolves with no value.
 */
async function updateItem(
  event: Event, 
  id: string, 
  url: string, 
  actions: string, 
  item_id: string, 
  item: Object
  ): Promise<void> {

  event.preventDefault();
  try {
    const response = !item_id 
    ? await storeAuth.axiosInstance.post(`${server}/${url}/${actions}/${id}`, item)
    : await storeAuth.axiosInstance.post(`${server}/${url}/${actions}/${item_id}`, item);
    const { message } = response.data;
    // Обновляем сообщение

    if (actions === 'check') {
      const alert = {
        'save': ['alert-info', 'Проверка сохранена'],
        'cancel': ['alert-warning', 'Проверка отменена'],
        'poligraf': ['alert-info', 'Окончено. Назначено проведение ПФО'],
        'result': ['alert-success', 'Проверка окончена']
      };
      emit('updateMessage', {
        attr: alert[message as keyof typeof alert][0],
        text: alert[message as keyof typeof alert][1]
      })
    
    } else {
      emit('updateMessage', {
        attr: 'alert-success',
        text: !item_id 
          ? `Запись  ID ${message} добавлена для таблицы ${url}` 
          : `Запись ID ${message} изменена для таблицы ${url}`
      })
    };
    // Обновляем данные кандидата
    getProfile()
  
  } catch (error) {

    emit('updateMessage', {
      attr: 'alert-danger',
      text: `Возникла ошибка ${error}`
    })
  }
}


/**
 * Deletes an item from the server based on its ID and flag.
 *
 * @param {string} id - The ID of the item to be deleted.
 * @param {string} flag - The flag indicating the type of item to be deleted.
 * @return {Promise} A promise that resolves with the result of the deletion.
 */
 async function deleteItem(id: string, flag: string): Promise<any> {
  if (confirm(`Вы действительно хотите удалить запись?`)) {
    const response = await storeAuth.axiosInstance.delete(`${server}/delete/${flag}/${id}`);
    const status = response.status;
    if (status === 200) {
      emit('updateMessage', {
        attr: 'alert-success',
        text: `Запись с ID ${id} из таблицы ${flag} удалена`
      })
      window.scrollTo(0,0);
      getProfile();
    
    } else {
      emit('updateMessage', {
        attr: 'alert-danger',
        text: 'Возникла ошибка при удалении записи'
      })
    }
  }
};

</script>

<template>
  <div class="container py-3">    
    <!--div v-if="data.candId !== '0'" class="row">
      <div class="col">
        <div class="text-end">
          <button @click="data.print=true" class="btn btn-outline-secondary btn-sm">Версия для печати</button>
        </div>
      </div>
    </div-->
    <div class="py-5"><h4>{{data.header}}</h4></div>

    <div class="nav nav-tabs nav-justified" role="tablist">
      <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#anketaTab" type="button" role="tab">Анкета</button>
      <button class="nav-link" data-bs-toggle="tab" data-bs-target="#checkTab" type="button" role="tab">Проверки</button>
      <button class="nav-link" data-bs-toggle="tab" data-bs-target="#registryTab" type="button" role="tab">Согласования</button>
      <button class="nav-link" data-bs-toggle="tab" data-bs-target="#poligrafTab" type="button" role="tab">Полиграф</button>
      <button class="nav-link" data-bs-toggle="tab" data-bs-target="#investigateTab" type="button" role="tab">Расследования</button>
      <button class="nav-link" data-bs-toggle="tab" data-bs-target="#inquiryTab" type="button" role="tab">Запросы</button>
      <button class="nav-link" data-bs-toggle="tab" data-bs-target="#photoTab" type="button" role="tab">Фото</button>
    </div>
    <div class="tab-content">
      <div class="tab-pane active py-1" role="tabpanel" id="anketaTab">
        <AnketaTab :resume="data.resume" 
                   :staffs="data.staffs" 
                   :docums="data.docums" 
                   :addrs="data.addrs" 
                   :conts="data.conts" 
                   :works="data.works" 
                   :relate="data.relate" 
                   :candId="data.candId" 
                   :status="data.status"
                   @deleteItem="deleteItem"
                   @updateItem="updateItem"
                   @updateMessage="emit('updateMessage')" 
                   @getProfile="getProfile"/>
      </div>
      <template v-if="data.candId !== '0'">
        <div class="tab-pane py-1" role="tabpanel" id="checkTab">
          <CheckTab 
                  :table="data.verification" 
                  :candId="data.candId" 
                  :status="data.status"
                  @deleteItem="deleteItem"
                  @updateItem="updateItem"
                  @updateMessage="emit('updateMessage')" 
                  @getProfile="getProfile" />
        </div>
        <div class="tab-pane py-1" role="tabpanel" id="registryTab">
          <RegistryTab 
                  :table="data.register" 
                  :candId="data.candId" 
                  @updateItem="updateItem" />
        </div>
        <div class="tab-pane py-1" role="tabpanel" id="poligrafTab">
          <PoligrafTab 
                  :table="data.pfo" 
                  :candId="data.candId" 
                  @deleteItem="deleteItem"
                  @updateItem="updateItem" />
        </div>
        <div class="tab-pane py-1" role="tabpanel" id="investigateTab">
          <InvestigateTab 
                  :table="data.inquisition" 
                  :candId="data.candId" 
                  @deleteItem="deleteItem"
                  @updateItem="updateItem"/>
        </div>
        <div class="tab-pane py-1" role="tabpanel" id="inquiryTab">
          <InquiryTab 
                  :table="data.needs" 
                  :candId="data.candId" 
                  @deleteItem="deleteItem"
                  @updateItem="updateItem"/>
        </div>
        <div class="tab-pane py-1" role="tabpanel" id="photoTab">
          <PhotoTab v-if="data.candId !== '0'"
                      :path="data.path" 
                      :candId="data.candId" 
                      @updateMessage="emit('updateMessage')" 
                      @getProfile="getProfile" />
        </div>
      </template>
    </div>
  </div>
  <!--button v-if="data.print" @click="data.print=false" class="btn btn-outline-secondary btn-sm d-print-none">Вернуться</button-->
</template>
