import { ref } from 'vue';
import { defineStore } from 'pinia';
import { appAuth } from '@/store/auth';
import { appAlert } from '@/store/alert';
import server from '@/store/server';

const storeAuth = appAuth();

const storeAlert = appAlert();

export const appProfile = defineStore('appProfile', () => {

  const candId = ref('');

  const anketa = ref({
    resume: {
      id: '',
      category: '',
      region_id: '',
      fullname: '',
      previous: '',
      birthday: '',
      birthplace: '',
      country: '',
      snils: '',
      inn: '',
      education: '',
      addition: '',
      path: '',
      status: '',
      create: '',
      update: '',
      request_id: '',
    },
    docums: [{
      id: '',
      view: '',
      series: '',
      number: '',
      agency: '',
      issue: '',
    }],
    addrs: [{
      id: '',
      view: '',
      region: '',
      address: '',
    }],
    conts: [{
      id: '',
      view: '',
      contact: '',
    }],
    works: [{
      id: '',
      start_date: '',
      end_date: '',
      workplace: '',
      address: '',
      position: '',
    }],
    staffs: [{
      id: '',
      position: '',
      department: ''
    }],
    relate: [{
      id: '',
      relation: '',
      relation_id: ''
    }]
  });

  const verification = ref([{
    id: '',
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
    comments: '',
    deadline: '',
    officer: '',
  }]);

  const register = ref([{
    id: '',
    comments: '',
    decision: '',
    supervisor: '',
    deadline: '',
  }]);

  const pfo = ref([{
    id: '',
    theme: '',
    results: '',
    officer: '',
    deadline: '',
  }]);

  const inquisition = ref([{
    id: '',
    theme: '',
    info: '',
    officer: '',
    deadline: ''
  }]);
  
  const needs = ref([{
    id: '',
    info: '',
    initiator: '',
    source: '',
    officer: '',
    deadline: '',
  }]);

  
/**
 * Fetches the profile information for a given ID.
 *
 * @param {string} id - The ID of the profile. Defaults to the value of candId if not provided.
 * @return {Promise<void>} - Resolves when the profile information is successfully fetched.
 */
  async function getProfile(id: string = candId.value): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.get(`${server}/profile/${id}`);
      const {resume, documents, addresses, contacts, relations, workplaces, staffs, 
        checks, registries, pfos, invs, inquiries} = response.data;
  
      Object.assign(anketa.value, {
        resume: resume,
        docums: documents,
        addrs: addresses,
        conts: contacts,
        works: workplaces,
        staffs: staffs,
        relate: relations
      });

      verification.value = checks;
      register.value = registries;
      pfo.value = pfos;
      inquisition.value = invs;
      needs.value = inquiries;
      
    } catch (error) {
      console.error(error)
    }
  }
  
  /**
   * Updates an item.
   *
   * @param {string} person_id - The ID of the person.
   * @param {string} url - The URL of the item.
   * @param {string} actions - The actions to be performed on the item.
   * @param {string} item_id - The ID of the item.
   * @param {Object} item - The item object to be updated.
   * @return {Promise<void>} A promise that resolves with no value.
   */
  async function updateItem(
    person_id: string, 
    url: string, 
    actions: string, 
    item_id: string, 
    item: Object
    ): Promise<void> {
  
    try {
      const response = actions === 'create' 
      ? await storeAuth.axiosInstance.post(`${server}/profile/${url}/${actions}/${person_id}`, item)
      : await storeAuth.axiosInstance.post(`${server}/profile/${url}/${actions}/${item_id}`, item);
      const { table, action, id, message } = response.data;
      
      const matches = {
        'staff': 'Должность',
        'relation': 'Связи',
        'document': 'Документы',
        'address': 'Адреса',
        'workplace': 'Места работы',
        'contact': 'Контакты',
        'region': 'Персона',
        'inquiry': 'Запросы',
        'investigation': 'Расследования',
        'poligraf': 'ПФО',
      };
  
      // Обновляем сообщение
      if (table === 'check') {
        const alert = {
          'save': ['alert-info', 'Проверка сохранена'],
          'cancel': ['alert-warning', 'Проверка отменена'],
          'poligraf': ['alert-info', 'Окончено. Назначено проведение ПФО'],
          'result': ['alert-success', 'Проверка окончена']
        };
        storeAlert.alertAttr = alert[message as keyof typeof alert][0];
        storeAlert.alertText = alert[message as keyof typeof alert][1];
      
      } else if (table === 'registry') {
        const alert = {
          'finish': ['alert-info', 'Согласование успешно отправлено/сохранено'],
          'cancel': ['alert-danger', 'Ошибка при отправке согласования'],
          'reply': ['alert-warning', 'Вы не имеете прав на отправку согласования'],
          'error': ['alert-warning', 'Неизвестная ошибка']
        };
        storeAlert.alertAttr = alert[message as keyof typeof alert][0];
        storeAlert.alertText = alert[message as keyof typeof alert][1];
      
      } else {
        switch (action) {
          
          case 'create':
            storeAlert.alertAttr = 'alert-success';
            storeAlert.alertText =  `Для ID ${id} добавлена запись в таблицу ${matches[table as keyof typeof matches]}`;
            break;
          
            case 'update':
              storeAlert.alertAttr = 'alert-success';
              storeAlert.alertText = `Изменена запись ${id} в таблице ${matches[table as keyof typeof matches]}`;
            break;
  
          default:
            break;
        }
      }
      // Обновляем данные кандидата
      getProfile();
    
    } catch (error) {
  
      storeAlert.alertAttr = 'alert-danger';
      storeAlert.alertText = `Возникла ошибка ${error}`;
    }
  };
  
  /**
   * Deletes an item from the server based on its ID and flag.
   *
   * @param {string} id - The ID of the item to be deleted.
   * @param {string} flag - The flag indicating the type of item to be deleted.
   * @return {Promise} A promise that resolves with the result of the deletion.
   */
   async function deleteItem(id: string, flag: string): Promise<any> {
    if (confirm(`Вы действительно хотите удалить запись?`)) {
      const response = await storeAuth.axiosInstance.delete(`${server}/profile/${flag}/delete/${id}`);
      const {message} = response.data;
      storeAlert.alertAttr = 'alert-info';
      storeAlert.alertText = message === flag 
        ? `Запись с ID ${id} из таблицы ${message} удалена`
        : message;
        
      getProfile();
    }
  }
  return { candId, anketa, verification, register, pfo, inquisition, needs, getProfile, updateItem, deleteItem }
})