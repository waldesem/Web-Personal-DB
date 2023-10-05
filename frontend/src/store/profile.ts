import { ref } from 'vue';
import { defineStore } from 'pinia';
import { classifyStore } from '@store/classify';
import { authStore } from '@/store/token';
import { alertStore } from '@store/alert';
import { loginStore } from './login';
import server from '@/store/server';
import router from '@/router/router';


export const profileStore = defineStore('profileStore', () => {
  
  const storeAuth = authStore()
  const storeAlert = alertStore();
  const classifyApp = classifyStore();
  const storeLogin = loginStore();

  interface Resume {
    id: string;
    category: string;
    region_id: string;
    fullname: string;
    previous: string;
    birthday: string;
    birthplace: string;
    country: string;
    snils: string;
    inn: string;
    education: string;
    addition: string;
    path: string;
    status: string;
    create: string;
    update: string;
    request_id: string;
  };

  interface Document {
    id: string;
    view: string;
    series: string;
    number: string;
    agency: string;
    issue: string;
  };

  interface Address {
    id: string;
    view: string;
    region: string;
    address: string;
  };

  interface Contact {
    id: string;
    view: string;
    contact: string;
  };

  interface Work {
    id: string;
    start_date: string;
    end_date: string;
    now_work: boolean;
    workplace: string;
    address: string;
    position: string;
  };

  interface Staff {
    id: string;
    position: string;
    department: string;
  };

  interface Relation {
    id: string;
    relation: string;
    relation_id: string;
  };

  interface Verification {
    id: string;
    workplace: string;
    employee: string;
    document: string;
    inn: string;
    debt: string;
    bankruptcy: string;
    bki: string;
    courts: string;
    affiliation: string;
    terrorist: string;
    mvd: string;
    internet: string;
    cronos: string;
    cros: string;
    addition: string;
    pfo: boolean;
    conclusion: string;
    comments: string;
    deadline: string;
    officer: string;
  };

  interface Register {
    id: string;
    comments: string;
    decision: string;
    supervisor: string;
    deadline: string;
  };

  interface Pfo {
    id: string;
    theme: string;
    results: string;
    officer: string;
    deadline: string;
  };

  interface Inquisition {
    id: string;
    theme: string;
    info: string;
    officer: string;
    deadline: string;
  };

  interface Needs {
    id: string;
    info: string;
    initiator: string;
    source: string;
    officer: string;
    deadline: string;
  };

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
      results: '',
      officer: '',
      deadline: '',
    }],
    inquisition: [{
      id: '',
      theme: '',
      info: '',
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
  const printPdf = ref(false);

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
           profile.value = response.data;
          break;
      };

      if (action === 'status'){
        storeAlert.setAlert('alert-info', 'Статус анкеты обновлен');
      
      } else if (action === 'send'){
        storeAlert.setAlert('alert-success', 'Анкета отправлена на проверку');
        spinner.value = false
        window.scrollTo(0, 0);
      
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
    cancelEdit();
    spinner.value = false;
  };
  

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
      const formData = new FormData();
      formData.append('file', inputElement.files[0]);
      
      try {
        const response = await storeAuth.axiosInstance.post(
          `${server}/file/${flag}/${idItem}`, formData
          );
        const { message } = response.data;

        if (flag === 'anketa'){
          storeAlert.setAlert("alert-success", "Данные успешно загружены");

          router.push({ name: 'profile', params: { id: message } })
        } else {
          storeAlert.setAlert("alert-success", 
                              "Файл или файлы успешно загружен/добавлены");
        };
      
      } catch (error) {
        console.error(error);
      }
    
    } else {
      storeAlert.setAlert("alert-warning", "Ошибка при загрузке файла");
    }
  };
  
  async function deleteFile(flag: string, idItem: string): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.delete(
        `${server}/file/${flag}/${idItem}`
        );
      console.log(response.data);
    
    } catch (error) {
      console.error(error);
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

  return {
    candId, 
    profile, 
    flag, 
    action, 
    itemForm, 
    itemId, 
    spinner, 
    printPdf,
    getItem, 
    submitFile, 
    clearItem, 
    cancelEdit,
    updateItem, 
    deleteItem, 
    deleteFile
  };
})