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
  Verification, 
  Register, 
  Pfo, 
  Inquisition, 
  Needs 
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
    verification: Verification[];
    register: Register[];
    pfo: Pfo[];
    inquisition: Inquisition[];
    needs: Needs[]
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
      now_work: false,
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
    }]
  });

  const itemForm: Record<string, any> = ref({});
  const candId = ref('');
  const flag = ref('');
  const action = ref('');
  const itemId = ref('');
  const spinner = ref(false);
  const urlImage = ref('');

  /**
   * Retrieves an item from the server.
   *
   * @param {string} item - The item to retrieve.
   * @param {string} [action='get'] - The action to perform on the item.
   * @param {string} [id=candId.value] - The ID of the item.
   * @return {Promise<void>} - A promise that resolves with no value.
   */
  async function getItem(
    item: string, action: string = 'get', id: string = candId.value
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
        default:
           console.log(profile.value);
          break;
      };

      if (action === 'status'){
        storeAlert.setAlert('alert-info', 'Статус анкеты обновлен');
      
      } else if (action === 'send'){
        storeAlert.setAlert('alert-success', 'Анкета отправлена на проверку');
        spinner.value = false
        window.scrollTo(0, 0);
        getItem('check', 'get', candId.value);
      
      } else if (item === 'check' && (action === 'add' || action === 'self')){
        getItem('check', 'get', candId.value);
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

    flag.value === 'registry' 
      ? spinner.value = true 
      : spinner.value = false;

      try {
      const response = action.value === 'create' 
        ? await storeAuth.axiosInstance.post(
          `${server}/${flag.value}/${action.value}/${candId.value}`, itemForm.value
          )
        : await storeAuth.axiosInstance.patch(
          `${server}/${flag.value}/${action.value}/${itemId.value}`, itemForm.value
          );

      console.log(response.status);

      storeAlert.setAlert('alert-success', 'Данные успешно обновлены');
      
      if (['registry', 'check', 'poligraf'].includes(flag.value)) {
        getItem('resume', 'get', candId.value)
      };
      getItem(flag.value, action.value, candId.value);

    } catch (error) {
      storeAlert.setAlert('alert-danger', `Возникла ошибка ${error}`);
    }
    clearItem(itemForm.value);
    action.value = '';
    flag.value = '';
    spinner.value = false;
  };
  
  function openForm (item: string, handle: string, idItem = '', formItem = {}) {
    flag.value = item;
    action.value = handle; 
    if (handle == 'create') {
      itemForm.value = {}
    } else {
      itemId.value = idItem; 
      itemForm.value = formItem
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
    item: string, action: string = 'delete', id: string = candId.value
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
          candId.value = message
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
        `${server}/file/get/${candId.value}`, 
          { responseType: 'blob' }
        );
      urlImage.value = window.URL.createObjectURL(new Blob([response.data]));
    
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
    clearItem(itemForm.value);
    action.value = '';
    flag.value = '';
    itemId.value = ''
  };

  return {
    candId, 
    profile, 
    flag, 
    action, 
    itemForm, 
    itemId, 
    spinner, 
    urlImage,
    getItem, 
    openForm,
    submitFile, 
    cancelEdit,
    updateItem, 
    deleteItem, 
    getImage
  };
})