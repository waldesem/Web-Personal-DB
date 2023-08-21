import { defineStore } from 'pinia';
import { ref } from 'vue';
import router from '@/router/router';
import { appClassify } from '@store/classify';
import { appAuth } from '@store/auth';
import { appAlert } from '@store/alert';
import { appProfile } from '@/store/profile';
import server from '@store/server';


const storeAuth = appAuth()

const classifyApp = appClassify();

const storeAlert = appAlert();

const storeProfile = appProfile();


export const appAnketa = defineStore('appAnketa', () => {

  const flag = ref('');

  const action = ref('');

  const file = ref(null);

  const itemForm: Record<string, any> = ref({});

  const itemId = ref('');

  async function updateStatus(): Promise<any> {
    if (confirm("Вы действительно обновить статус?")) {
      const response = await storeAuth.axiosInstance.get(`${server}/anketa/status/${storeProfile.candId}`);
      const { message } = response.data;
      
      storeProfile.getProfile();
      
      storeAlert.alertAttr = message == classifyApp.status['update'] 
          ? "alert-success" 
          : "alert-warning";
      storeAlert.alertText = message == classifyApp.status['update'] 
          ? "Статус обновлен" 
          : "Анкету с текущим статусом обновить нельзя";
    }
  };

  /**
   * Sends the resume for verification.
   *
   * @return {Promise<void>} A promise that resolves when the resume is sent for verification.
   */
  async function sendResume(): Promise<void> {
    if (confirm("Вы действительно хотите отправить анкету на проверку?")) {

      const resp = await storeAuth.axiosInstance.get(`${server}/anketa/send/${storeProfile.candId}`);
      const { msg } = resp.data;
      const textMessage = {
        robot: ['Анкета отправлена на проверку', "alert-success"],
        error: ['Отправка анкеты кандидата не удалась, либо анкета взята в работу', "alert-info"],
      };
      storeAlert.alertAttr = textMessage[msg as keyof typeof textMessage][1];
      storeAlert.alertText = textMessage[msg as keyof typeof textMessage][0];
    }
  };

  /**
   * Updates an item and emits an event.
   *
   * @return {void} This function does not return anything.
   */
  function updateItem(): void {
    storeProfile.updateItem(storeProfile.candId, flag.value, action.value, itemId.value, itemForm.value);
    cancelEdit();
  };

  const clearItem = () => {
    itemForm.value = {};
    itemId.value = '';
  };

  /**
   * Cancels the current edit operation.
   *
   * @return {void} 
   */
  const cancelEdit = (): void => {
    clearItem();
    itemId.value = '';
    itemForm.value = {}
  };

  const redirectMain = (): void => {
    router.push({ name: 'persons' })
  }
    
/**
 * Submits the data to the server to create a new resume.
 *
 * @return {Promise<void>} A promise that resolves when the data has been successfully submitted.
 */
async function submitResume(): Promise<void> {
  try {
    const response = await storeAuth.axiosInstance.post(`${server}/resume/create`, storeProfile.anketa.resume);
    const { result, person_id } = response.data;
    
    storeAlert.alertAttr = result ? "alert-info" : "alert-success";
    storeAlert.alertText = result ? 'Анкета уже существует. Данные обновлены' : 'Анкета успешно добавлена';
    
    if (action.value === 'update') {
      cancelEdit();
      storeProfile.getProfile()
    } else router.push({ name: 'profile', params: { id: person_id } });
  
  } catch (error) {
    console.error(error);
  }
}

  /**
   * Submits a file for upload.
   *
   * @param {Event} event - The event object.
   * @return {Promise<void>} A promise that resolves when the file is successfully uploaded.
   */
  async function submitFile(event: Event): Promise<void> {
    event.preventDefault();
    
    const formData = new FormData();
    const fileInput = file.value as HTMLInputElement | null;
    if (fileInput && fileInput.files) {
      formData.append('file', fileInput.files[0]);
      
      try {
        const response = await storeAuth.axiosInstance.post(`${server}/resume/upload`, formData);
        const { result, person_id } = response.data;
        // Отправка сообщения
        storeAlert.alertAttr = result ? "alert-info" : "alert-success";
        storeAlert.alertText = result ? 'Анкета уже существует. Данные обновлены' : 'Анкета успешно добавлена';
        // Загрузка профиля и переход на страницу профиля
        router.push({ name: 'profile', params: { id: person_id } })
      
      } catch (error) {
        console.error(error);
      }
    
    } else {
      storeAlert.alertAttr = "alert-warning";
      storeAlert.alertText = "Ошибка при загрузке файла";
    }
  };


  async function addCheck() {
    if (storeProfile.anketa.resume['status'] === classifyApp.status['save'] || 
      storeProfile.anketa.resume['status'] === classifyApp.status['manual'] ||
      storeProfile.anketa.resume['status'] === classifyApp.status['robot']) {
      
      storeAlert.alertAttr = 'alert-warning';
      storeAlert.alertText = 'Нельзя добавить проверку к текущему статусу';

    } else {
      try {
        const response = await storeAuth.axiosInstance.get(`${server}/check/add/${storeProfile.candId}`);
        const { message } = response.data;
        
        if (message === "manual") {
          storeAlert.alertAttr = 'alert-info';
          storeAlert.alertText = 'Начата ручная проверка';
          storeProfile.getProfile();

        } else {
          cancelEdit();

          storeAlert.alertAttr = 'alert-warning';
          storeAlert.alertText = 'Проверка кандидата уже начата';
        }

      } catch (error) {
        console.error(error)
      }
    }
  };

  function deleteCheck(id: string, flag: string): void {
    if ([classifyApp.status['robot'], classifyApp.status['finish']].includes(storeProfile.anketa.resume['status'])) {
      storeAlert.alertAttr = 'alert-warning';
      storeAlert.alertText = 'Нельзя удалить проверку с текущим статусом';

    } else {
      storeProfile.deleteItem(id, flag)
    }
  };

  async function cancelCheck() {
    if (storeProfile.anketa.resume['status'] === classifyApp.status['save']) {
      cancelEdit();
    } else {
      const response = await storeAuth.axiosInstance.get(`${server}/anketa/status/${storeProfile.candId}`);
      const { message } = response.data;
      storeAlert.alertAttr = message == 'update' ? "alert-success" : "alert-warning";
      storeAlert.alertText = message == 'update' ? "Отмена. Статус обновлен" : "Текущий статус обновить нельзя";
    }
  }

  return { flag, action, itemForm, itemId, file, updateStatus, sendResume, updateItem, cancelEdit, clearItem, submitResume, submitFile, redirectMain, addCheck, deleteCheck, cancelCheck};
});
