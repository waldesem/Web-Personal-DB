import { ref } from 'vue';
import { defineStore } from 'pinia';
import { classifyStore } from '@store/classify';
import { authStore } from '@/store/token';
import { alertStore } from '@store/alert';
import { loginStore } from './login';
import { server, clearItem } from '@share/utilities';
import router from '@/router/router';
import {
  Resume, 
  Document, 
  Address, 
  Contact, 
  Work, 
  Staff, 
  Relation, 
  Affilation,
  Verification, 
  Register, 
  Pfo, 
  Inquisition, 
  Needs,
  OneS
} from '@share/interfaces'


export const profileStore = defineStore('profileStore', () => {
  
  const storeAuth = authStore()
  const storeAlert = alertStore();
  const classifyApp = classifyStore();
  const storeLogin = loginStore();

  const profile = ref<{
    resume: Resume;
    docums: Document[];
    addrs: Address[];
    conts: Contact[];
    works: Work[];
    staffs: Staff[];
    relate: Relation[];
    affilation: Affilation[];
    verification: Verification[];
    register: Register[];
    pfo: Pfo[];
    inquisition: Inquisition[];
    needs: Needs[],
    ones: OneS[]
  }>({
    resume: {
      id: '',
      category: '',
      region_id: '',
      fullname: '',
      previous: '',
      birthday: '',
      birthplace: '',
      country: '',
      ext_country: '',
      snils: '',
      inn: '',
      education: '',
      marital: '',
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
      reason: '',
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
    }],
    affilation: [{
      id: '',
      view: '',
      name: '',
      inn: '',
      position: '',
      deadline: ''
    }],
    verification: [{
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
      path: '',
      pfo: false, 
      conclusion: '', 
      comments: '', 
      deadline: '', 
      officer: '',
    }],
    register: [{
      id: '',
      comments: '',
      decision: '',
      supervisor: '',
      deadline: '',
    }],
    pfo: [{
      id: '',
      theme: '',
      path: '',
      results: '',
      officer: '',
      deadline: '',
    }],
    inquisition: [{
      id: '',
      theme: '',
      info: '',
      path: '',
      officer: '',
      deadline: ''
    }],
    needs: [{
      id: '',
      info: '',
      initiator: '',
      source: '',
      officer: '',
      deadline: '',
    }],
    ones: [{
      id: '',
      full_name: '',
      birth_date: '',
      start_date: '',
      end_date: '',
      start_position: '',
      end_position: ''
    }]
  });

  const dataProfile = ref({
    itemForm: <Record<string, any>>({}),
    candId: '',
    itemId: '',
    flag: '',
    action: '',
    urlImage: '',
    spinner: false
  });

  /**
   * Retrieves an item from the server.
   *
   * @param {string} item - The item to retrieve.
   * @param {string} [action='get'] - The action to perform on the item.
   * @param {string} [id=candId.value] - The ID of the item.
   * @return {Promise<void>} - A promise that resolves with no value.
   */
  async function getItem(
    item: string, action: string = 'get', id: string = dataProfile.value.candId
    ): Promise<void> {

    if (item === 'check' && action === 'add'){
      if (profile.value.resume['status'] === classifyApp.classifyItems.status['save'] || 
          profile.value.resume['status'] === classifyApp.classifyItems.status['manual'] ||
          profile.value.resume['status'] === classifyApp.classifyItems.status['robot']) {
        
        storeAlert.setAlert('alert-warning', 'Нельзя добавить проверку к текущему статусу');
        return
      };
    };
    
    if (item === 'check' && action === 'self'){
      if (!confirm('Вы действительно делегировать анкету себе?')) {
      return
      };
    };
    if (item === 'resume' && action === 'status'){
      if (!confirm('Вы действительно хотите изменить статус резюме]?')) {
      return
      };
    };

    try {
      const response = await storeAuth.axiosInstance.get(
        `${server}/${item}/${action}/${id}`
        );
      switch (item){
        case 'resume':
          profile.value.resume = response.data;
          break;
        case 'staff': 
          profile.value.staffs = response.data;
          break;
        case 'document': 
          profile.value.docums = response.data;
          break;
        case 'address': 
          profile.value.addrs = response.data;
          break;
        case 'contact': 
          profile.value.conts = response.data;
          break;
        case 'workplace': 
          profile.value.works = response.data;
          break;
        case 'relation': 
          profile.value.relate = response.data;
          break;
        case 'affilation': 
          profile.value.affilation = response.data;
          break;
        case 'check': 
          profile.value.verification = response.data;
          break;
        case 'registry': 
          profile.value.register = response.data;
          break;
        case 'poligraf': 
          profile.value.pfo = response.data;
          break;
        case 'investigation':
          profile.value.inquisition = response.data;
           break;
        case 'inquiry': 
          profile.value.needs = response.data;
          break;
        case 'ones': 
          profile.value.ones = response.data;
          break;
        default:
           console.log(profile.value);
          break;
      };

      if (action === 'status'){
        storeAlert.setAlert('alert-info', 'Статус анкеты обновлен');
      
      } else if (action === 'send'){
        storeAlert.setAlert('alert-success', 'Анкета отправлена на проверку');
        dataProfile.value.spinner = false
        window.scrollTo(0, 0);
        getItem('check', 'get', dataProfile.value.candId);
      
      } else if (item === 'check' && (action === 'add' || action === 'self')){
        getItem('check', 'get', dataProfile.value.candId);
      }

    } catch (error) {
      console.error(error)
      storeAlert.setAlert('alert-danger', `Ошибка обработки ${error}`);
    }
  };

  /**
   * Updates an item.
   *
   * @return {Promise<void>} A promise that resolves with no value.
   */
  async function updateItem(): Promise<void> {

    dataProfile.value.flag === 'registry' 
      ? dataProfile.value.spinner = true 
      : dataProfile.value.spinner = false;

      try {
      const response = dataProfile.value.action === 'create' 
        ? await storeAuth.axiosInstance.post(
          `${server}/${dataProfile.value.flag}/${dataProfile.value.action}/${dataProfile.value.candId}`, 
          dataProfile.value.itemForm
          )
        : await storeAuth.axiosInstance.patch(
          `${server}/${dataProfile.value.flag}/${dataProfile.value.action}/${dataProfile.value.itemId}`, 
          dataProfile.value.itemForm
          );

      console.log(response.status);

      storeAlert.setAlert('alert-success', 'Данные успешно обновлены');
      
      if (['registry', 'check', 'poligraf'].includes(dataProfile.value.flag)) {
        getItem('resume', 'get', dataProfile.value.candId)
      };
      getItem(dataProfile.value.flag, dataProfile.value.action, dataProfile.value.candId);

    } catch (error) {
      storeAlert.setAlert('alert-danger', `Возникла ошибка ${error}`);
    }
    clearItem(dataProfile.value.itemForm);
    dataProfile.value.action = '';
    dataProfile.value.flag = '';
    dataProfile.value.spinner = false;
  };
  
  function openForm (item: string, handle: string, idItem = '', formItem = {}) {
    dataProfile.value.flag = item;
    dataProfile.value.action = handle; 
    if (handle == 'create') {
      dataProfile.value.itemForm.value = {}
    } else {
      dataProfile.value.itemId = idItem; 
      dataProfile.value.itemForm.value = formItem
    };
  };

  /**
   * Deletes an item.
   *
   * @param {string} item - The item to delete.
   * @param {string} action - The action to perform on the item. Default is 'delete'.
   * @param {string} id - The ID of the item. Default is the value of candId.
   * @return {Promise<void>} A promise that resolves when the item is deleted.
   */
  async function deleteItem(
    item: string, action: string = 'delete', id: string = dataProfile.value.candId
    ): Promise<void> {

    if ([classifyApp.classifyItems.status['robot'], 
        classifyApp.classifyItems.status['finish']].includes(profile.value.resume['status']) 
      && (item === 'check' || item === 'resume')) {

      storeAlert.setAlert('alert-warning', 'Нельзя удалить запись с текущим статусом');
      return
    };

    if (confirm(`Вы действительно хотите удалить запись?`)) {
      try {
        const response = await storeAuth.axiosInstance.delete(
          `${server}/${item}/${action}/${id}`
          );
        console.log(response.status);
        item === 'resume' 
          ? router.push({ name: 'persons', params: { group: storeLogin.pageIdentity } }) 
          : getItem(item);

         storeAlert.setAlert('alert-info', `Запись с ID ${id} удалена`);
      
        } catch (error) {
        console.error(error)
      }
    }
  };

  /**
   * Submits a file for upload.
   *
   * @param {Event} event - The event object.
   * @return {Promise<void>} A promise that resolves when the file is successfully uploaded.
   */
  async function submitFile(
    event: Event, flag: string, idItem: string = '0'
    ): Promise<void> {

    const inputElement = event.target as HTMLInputElement;
    
    if (inputElement && inputElement.files && inputElement.files.length > 0) {

      const file = inputElement.files[0];
      const maxSizeInBytes = 1024 * 1024; // 1MB
      
      if (file.size > maxSizeInBytes) {
        storeAlert.setAlert(
          'alert-warning', 
          'File size exceeds the limit. Please select a smaller file.'
          );
        inputElement.value = ''; // Reset the input field
        return;
      }

      const formData = new FormData();
      formData.append('file', inputElement.files[0]);
      
      try {
        const response = await storeAuth.axiosInstance.post(
          `${server}/file/${flag}/${idItem}`, formData
          );
        const { message } = response.data;

        if (flag === 'anketa'){
          storeAlert.setAlert("alert-success", "Данные успешно загружены");
          dataProfile.value.candId = message
          router.push({ name: 'profile', params: { id: message } })
        
        } else if (flag === 'image'){
          getImage();
          
        } else {
          storeAlert.setAlert("alert-success", 
                              "Файл или файлы успешно загружен/добавлены");
          getItem(flag, 'get', idItem);
        };
      
      } catch (error) {
        console.error(error);
      }
    
    } else {
      storeAlert.setAlert("alert-warning", "Ошибка при загрузке файла");
    }
  };
  
  /**
   * Retrieves an image from the server and assigns it to the urlImage variable.
   *
   * @return {Promise<void>} A Promise that resolves when the image has been retrieved and assigned.
   */
  async function getImage(): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.get(
        `${server}/file/get/${dataProfile.value.candId}`, 
          { responseType: 'blob' }
        );
      dataProfile.value.urlImage = window.URL.createObjectURL(new Blob([response.data]));
    
    } catch (error) {
      console.error(error);
    }
  };
  
  /**
   * Cancels the current edit operation.
   *
   * @return {void} 
   */
  function cancelEdit(): void {
    clearItem(dataProfile.value.itemForm);
    dataProfile.value.action = '';
    dataProfile.value.flag = '';
    dataProfile.value.itemId = ''
  };

  return {
    profile,
    dataProfile,
    getItem, 
    openForm,
    submitFile, 
    cancelEdit,
    updateItem, 
    deleteItem, 
    getImage
  };
})