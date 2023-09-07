import { ref } from 'vue';
import { defineStore } from 'pinia';
import { appClassify } from '@store/classify';
import { appAuth } from '@store/auth';
import { appAlert } from '@store/alert';
import { anketa, verification, register, pfo, inquisition, needs } from '@store/interfaces'
import server from '@/store/server';
import router from '@/router/router';


export const appProfile = defineStore('appProfile', () => {
  
  const storeAuth = appAuth()
  const storeAlert = appAlert();
  const classifyApp = appClassify();

  const candId = ref('');
  const flag = ref('');
  const action = ref('');
  const itemId = ref('');
  const itemForm: Record<string, any> = ref({});
  const spinner = ref(false);
  const printPdf = ref(false);

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
  };

  /**
   * Submits the data to the server to create a new resume.
   *
   * @return {Promise<void>} A promise that resolves when the data has been successfully submitted.
   */
  async function submitResume(): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.post(`${server}/resume/${action.value}`, itemForm.value);
      const { result, person_id } = response.data;
      
      if (result) {
        storeAlert.setAlert(action.value === "create" ? "alert-info" : "alert-success", 
                            result ? 'Анкета добавлена повторно' : 'Анкета успешно обновлена');
      } else {
        storeAlert.setAlert("alert-success", "Анкета успешно добавлена");
      }
      if (action.value === 'update') {
        getProfile();
      } else {
        router.push({ name: 'profile', params: { id: person_id } })
      };
      cancelEdit();
      
    } catch (error) {
      console.error(error);
    }
  };

  /**
   * Submits a file for upload.
   *
   * @param {Event} event - The event object.
   * @return {Promise<void>} A promise that resolves when the file is successfully uploaded.
   */
  async function submitFile(event: Event): Promise<void> {

    const inputElement = event.target as HTMLInputElement;
    if (inputElement && inputElement.files && inputElement.files.length > 0) {
      const formData = new FormData();
      formData.append('file', inputElement.files[0]);
      
      try {
        const response = await storeAuth.axiosInstance.post(`${server}/anketa/upload`, formData);
        const { result, person_id } = response.data;

        storeAlert.setAlert(result ? "alert-info" : "alert-success",
                            result ? 'Анкета уже существует. Данные обновлены' : 'Анкета успешно добавлена');

        router.push({ name: 'profile', params: { id: person_id } })
      
      } catch (error) {
        console.error(error);
      }
    
    } else {
      storeAlert.setAlert("alert-warning", "Ошибка при загрузке файла");
    }
  };

  /**
   * Updates the status.
   *
   * @return {Promise<any>} The response from the server.
   */
  async function updateStatus(): Promise<any> {
    if (confirm("Вы действительно обновить статус?")) {
      const response = await storeAuth.axiosInstance.get(`${server}/anketa/status/${candId.value}`);
      const { message } = response.data;
      
      getProfile();
      
      storeAlert.setAlert(message == classifyApp.status['update'] ? "alert-success" : "alert-warning",
                          message == classifyApp.status['update'] 
                                      ? "Статус обновлен" 
                                      : "Анкету с текущим статусом обновить нельзя")
    }
  };

  /**
   * Sends the resume for verification.
   *
   * @return {Promise<void>} A promise that resolves when the resume is sent for verification.
   */
  async function sendResume(): Promise<void> {
    if (confirm("Вы действительно хотите отправить анкету на проверку?")) {
      spinner.value = true
      try {
        const resp = await storeAuth.axiosInstance.get(`${server}/anketa/send/${candId.value}`);
        const { message } = resp.data;
        
        const textMessage = {
          'robot': ['Анкета отправлена на проверку', "alert-success"],
          'error': ['Отправка анкеты кандидата не удалась, либо анкета уже взята в работу', "alert-info"],
        };
        storeAlert.setAlert(textMessage[message as keyof typeof textMessage][1],
                            textMessage[message as keyof typeof textMessage][0]);
  
        getProfile();
        window.scrollTo(0, 0);

      } catch (error) {
        console.error(error);
      }
    }
    spinner.value = false
  };

  /**
   * Updates an item.
   *
   * @return {Promise<void>} A promise that resolves with no value.
   */
  async function updateItem(): Promise<void> {

    flag.value === 'registry' ? spinner.value = true : spinner.value = false;
    try {
      const response = action.value === 'create' 
      ? await storeAuth.axiosInstance.post(`${server}/profile/${flag.value}/${action.value}/${candId.value}`, itemForm.value)
      : await storeAuth.axiosInstance.post(`${server}/profile/${flag.value}/${action.value}/${itemId.value}`, itemForm.value);

      const { table, actions, id, message } = response.data;
      
      const matches = {
        'staff': 'Должность',
        'relation': 'Связи',
        'document': 'Документы',
        'address': 'Адреса',
        'workplace': 'Места работы',
        'contact': 'Контакты',
        'region': 'Персона',
        'check': 'Проверка',
        'inquiry': 'Запросы',
        'investigation': 'Расследования',
        'poligraf': 'ПФО',
        'registry': 'Согласование',
        'location': 'Персона (регион)',
      };
  
      // Обновляем сообщение
      if (table === 'check') {
        const alert = {
          'save': ['alert-info', 'Проверка сохранена'],
          'cancel': ['alert-warning', 'Проверка отменена'],
          'poligraf': ['alert-info', 'Окончено. Назначено проведение ПФО'],
          'result': ['alert-success', 'Проверка окончена']
        };

        storeAlert.setAlert(alert[message as keyof typeof alert][0], alert[message as keyof typeof alert][1]);
      
      } else if (table === 'registry') {

        switch (message) {
          case 'finish':
            storeAlert.setAlert('alert-info', 'Согласование успешно отправлено');
            break;

          default:
            storeAlert.setAlert('alert-danger', message);
            break;
        };

      } else {
        switch (actions) {
          case 'create':
            storeAlert.setAlert('alert-success', `Для ID ${id} добавлена запись в таблицу ${matches[table as keyof typeof matches]}`);
            break;
          
            case 'update':
              storeAlert.setAlert('alert-success', `Изменена запись ${id} в таблице ${matches[table as keyof typeof matches]}`);
            break;
  
          default:
            break;
        }
      };
      cancelEdit();
      getProfile();
    
    } catch (error) {
      storeAlert.setAlert('alert-danger', `Возникла ошибка ${error}`);
    }
    spinner.value = false;
  };
  
  /**
   * Deletes an item from the server based on its ID and flag.
   *
   * @param {string} id - The ID of the item to be deleted.
   * @param {string} flag - The flag indicating the type of item to be deleted.
   * @return {Promise} A promise that resolves with the result of the deletion.
   */
   async function deleteItem(id: string, flag: string): Promise<any> {
    
    if ([classifyApp.status['robot'], classifyApp.status['finish']].includes(anketa.value.resume['status']) 
      && (flag === 'check' || flag === 'person')) {

      storeAlert.setAlert('alert-warning', 'Нельзя удалить запись с текущим статусом');
      return
    };

    if (confirm(`Вы действительно хотите удалить запись?`)) {
      const response = await storeAuth.axiosInstance.delete(`${server}/profile/${flag}/delete/${id}`);
      const {message} = response.data;
      
      storeAlert.setAlert('alert-info', storeAlert.alertText = message === flag 
                                                                ? `Запись с ID ${id} из таблицы ${message} удалена`
                                                                : message);
      flag === 'person' ? router.push({ name: 'staffsec' }) : getProfile();
    }
  };

  /**
   * Asynchronously adds a check.
   *
   * @return {Promise<void>} Promise that resolves when the check is added.
   */
  async function addCheck(): Promise<void> {
    if (anketa.value.resume['status'] === classifyApp.status['save'] || 
      anketa.value.resume['status'] === classifyApp.status['manual'] ||
      anketa.value.resume['status'] === classifyApp.status['robot']) {
      
      storeAlert.setAlert('alert-warning', 'Нельзя добавить проверку к текущему статусу');

    } else {
      try {
        const response = await storeAuth.axiosInstance.get(`${server}/check/add/${candId.value}`);
        const { message } = response.data;
        
        if (message === "manual") {
          storeAlert.setAlert('alert-info', 'Начата ручная проверка');
          getProfile();

        } else {
          cancelEdit();
          storeAlert.setAlert('alert-warning', 'Проверка кандидата уже начата');
        };

      } catch (error) {
        console.error(error)
      }
    }
  };

  /**
   * Cancels the check.
   *
   * @return {Promise<void>} Returns a promise that resolves when the check is cancelled.
   */
  async function cancelCheck(): Promise<void> {
    if (anketa.value.resume['status'] === classifyApp.status['save']) {
      cancelEdit();
    } else {
      const response = await storeAuth.axiosInstance.get(`${server}/anketa/status/${candId.value}`);
      const { message } = response.data;

      storeAlert.setAlert(message == 'update' ? "alert-success" : "alert-warning",
                          message == 'update' ? "Отмена. Статус обновлен" : "Текущий статус обновить нельзя");
      cancelEdit();
    }
  };

  /**
   * Clears the item form and sets the itemId value to an empty string.
   */
  function clearItem(): void {
    itemId.value = '';
    Object.keys(itemForm.value).forEach(key => {
      delete itemForm.value[key];
    });
  };

  /**
   * Cancels the current edit operation.
   *
   * @return {void} 
   */
  function cancelEdit(): void {
    clearItem();
    action.value = '';
    flag.value = '';
  };

  /**
   * Redirects to the main page.
   *
   * @return {void} No return value.
   */
  function redirectMain(): void {
    router.push({ name: 'staffsec' })
  };

  return {
    candId, anketa, verification, register, pfo, inquisition, needs, flag, action, itemForm, itemId, spinner, printPdf,
    submitResume, submitFile, updateStatus, sendResume, clearItem, cancelEdit,
    redirectMain, updateItem, deleteItem, addCheck, cancelCheck, getProfile
  };
})