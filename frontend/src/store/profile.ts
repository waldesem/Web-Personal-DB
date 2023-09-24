import { ref } from 'vue';
import { defineStore } from 'pinia';
import { appClassify } from '@store/classify';
import { appAuth } from '@/store/token';
import { appAlert } from '@store/alert';
import { anketa, verification, register, pfo, inquisition, needs } from '@store/interfaces'
import server from '@/store/server';
import router from '@/router/router';
import { appLogin } from './login';


export const appProfile = defineStore('appProfile', () => {
  
  const storeAuth = appAuth()
  const storeAlert = appAlert();
  const classifyApp = appClassify();
  const storeLogin = appLogin();

  const candId = ref('');
  const flag = ref('');
  const action = ref('');
  const itemId = ref('');
  const itemForm: Record<string, any> = ref({});
  const spinner = ref(false);
  const printPdf = ref(false);
  const mappingItems = {
    'resume': anketa.value.resume,
    'staff': anketa.value.staffs,
    'document': anketa.value.docums,
    'address': anketa.value.addrs,
    'contact': anketa.value.conts,
    'workplace': anketa.value.works,
    'relation': anketa.value.relate,
    'check': verification.value,
    'registry': register.value,
    'poligraf': pfo.value,
    'investigation': inquisition.value,
    'inquiry': needs.value
  };

  async function getProfile() {
    await Promise.all([
      Object.keys(mappingItems).map(async (key) => await getItem(key))
    ]);
  };

  async function getItem(item: string, action: string = 'get', id: string = candId.value): Promise<void> {

    if (item === 'check' && action === 'add'){
      if (anketa.value.resume['status'] === classifyApp.status['save'] || 
        anketa.value.resume['status'] === classifyApp.status['manual'] ||
        anketa.value.resume['status'] === classifyApp.status['robot']) {
        
        storeAlert.setAlert('alert-warning', 'Нельзя добавить проверку к текущему статусу');
        return
      };
    };

    try {
      const response = await storeAuth.axiosInstance.get(`${server}/${item}/${action}/${id}`);
      
      mappingItems[item as keyof typeof mappingItems] = response.data;
      
      if (action === 'status'){
        storeAlert.setAlert('alert-info', 'Статус анкеты обновлен');
      
      } else if (action === 'send'){
        storeAlert.setAlert('alert-success', 'Анкета отправлена на проверку');
        spinner.value = false
        window.scrollTo(0, 0);
      };

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
      
      await Promise.all([
        await getItem(flag.value, action.value, candId.value),
        await getItem('resume', 'get', candId.value)
      ])
      cancelEdit();

    } catch (error) {
      storeAlert.setAlert('alert-danger', `Возникла ошибка ${error}`);
    }
    spinner.value = false;
  };
  

  async function deleteItem(item: string, action: string = 'delete', id: string = candId.value): Promise<void> {

    if ([classifyApp.status['robot'], classifyApp.status['finish']].includes(anketa.value.resume['status']) 
      && (item === 'check' || item === 'resume')) {

      storeAlert.setAlert('alert-warning', 'Нельзя удалить запись с текущим статусом');
      return
    };

    if (confirm(`Вы действительно хотите удалить запись?`)) {
      try {
        const response = await storeAuth.axiosInstance.delete(`${server}/${item}/${action}/${id}`);
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
   * Submits the data to the server to create a new resume.
   *
   * @return {Promise<void>} A promise that resolves when the data has been successfully submitted.
   */
  async function submitResume(): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.post(`${server}/resume/${action.value}`, itemForm.value);
      const { message } = response.data;
      
      storeAlert.setAlert(action.value === "create" 
                            ? "alert-success" : "alert-info", 
                          action.value === "create"
                            ? 'Анкета успешно добавлена' 
                            : 'Анкета успешно обновлена');

      action.value === 'update' ? getItem('resume')
        : router.push({ name: 'profile', params: { id: message } });
      
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
  async function submitFile(event: Event, flag: string, idItem: string = '0'): Promise<void> {

    const inputElement = event.target as HTMLInputElement;
    if (inputElement && inputElement.files && inputElement.files.length > 0) {
      const formData = new FormData();
      formData.append('file', inputElement.files[0]);
      
      try {
        const response = await storeAuth.axiosInstance.post(`${server}/file/${flag}/${idItem}`, formData);
        const { result, item_id } = response.data;

        if (flag === 'anketa'){
          storeAlert.setAlert(result ? "alert-info" : "alert-success",
                              result ? 'Анкета уже существует. Данные обновлены' : 'Анкета успешно добавлена');

          router.push({ name: 'profile', params: { id: item_id } })
        } else {
          storeAlert.setAlert("alert-success", "Файл или файлы успешно загружен/добавлены");
        };
      
      } catch (error) {
        console.error(error);
      }
    
    } else {
      storeAlert.setAlert("alert-warning", "Ошибка при загрузке файла");
    }
  };

  /**
   * Cancels the check.
   *
   * @return {Promise<void>} Returns a promise that resolves when the check is cancelled.
   */
  async function cancelCheck(): Promise<void> {
    if (anketa.value.resume['status'] !== classifyApp.status['save']) {
      getItem('resume', 'status', candId.value);
    };
    cancelEdit();
  };

  /**
   * Clears the item form and sets the itemId value to an empty string.
   */
  function clearItem(): void {
    itemId.value = '';
      Object.keys(itemForm.value).forEach(key => {
        itemForm.value[key] = '';
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
    candId, anketa, verification, register, pfo, inquisition, needs, 
    flag, action, itemForm, itemId, spinner, printPdf,
    getItem, submitResume, submitFile, clearItem, cancelEdit,
    redirectMain, updateItem, deleteItem, cancelCheck, getProfile
  };
})