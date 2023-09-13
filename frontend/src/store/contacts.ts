import { defineStore } from 'pinia';
import { appAuth } from '@store/auth';
import { appLogin } from '@store/login';
import { appAlert } from '@store/alert';
import { ref } from 'vue';
import server from '@store/server';


export const storeContact = defineStore('storeContact',  () => {

  const storeAuth = appAuth();
  const storeLogin = appLogin();
  const storeAlert = appAlert();

  const data = ref({
    сontacts: [],
    hasPrev: false,
    hasNext: false
  });

  const searchData = ref('');
  
  const currenData = ref({
    currentPage: 1,
    currentPath: 'list'
  });
  
  const itemAction = ref('');
  const itemId = ref('');
  const itemForm = ref({
    id: '',
    company: '',
    city: '',
    fullname: '',
    contact: '',
    comment: '',
    data: ''
  });

  async function getContacts(url: string=currenData.value.currentPath, page: number=1): Promise<void> {
    currenData.value.currentPage = page;
    currenData.value.currentPath = url;

    try {
      const response = url === 'search' 
        ? await storeAuth.axiosInstance.post(`${server}/connects/${storeLogin.pageIdentity}/${url}/${page}`, searchData.value)
        : await storeAuth.axiosInstance.get(`${server}/connects/${storeLogin.pageIdentity}/${url}/${page}`);

      const [ datas, metadata ] = response.data;
      Object.assign(data.value, {
        contacts: datas,
        hasPrev: metadata.has_prev,
        hasNext: metadata.has_next
      });

    } catch (error) {
      console.error(error);
    }
  };

  /**
   * Asynchronously moves to the previous page if it exists.
   *
   * @return {undefined} No return value.
   */
  //
  function prevPage(): undefined {
    if (data.value.hasPrev) {
      currenData.value.currentPage -= 1;
      getContacts(currenData.value.currentPath, currenData.value.currentPage);
    }
  };

  /**
   * Moves to the next page if there is one available.
   *
   * @return {Promise<void>} A promise that resolves when the operation is complete.
   */
  function nextPage(): undefined {
    if (data.value.hasNext) {
      currenData.value.currentPage += 1;
      getContacts(currenData.value.currentPath, currenData.value.currentPage);
    }
  };

  /**
   * Updates an item.
   *
   * @return {Promise<void>} A promise that resolves with no value.
   */
  async function updateItem(flag: string = itemAction.value, contactId: string = itemId.value): Promise<void> {
    
    try {
      const response = flag === 'create' || flag === 'update'
      ? await storeAuth.axiosInstance.post(`${server}/contact/${flag}/${contactId}`, itemForm.value)
      : await storeAuth.axiosInstance.delete(`${server}/contact/$${flag}/${contactId}`);

      const { action, item_id } = response.data;

      const alert = {
        'create': ['alert-success', `Создан контакт ${item_id}`],
        'edit': ['alert-info', `Контакт ${item_id} обновлен`],
        'delete': ['alert-warning', `Контакт ${item_id} удален`]
      };
      storeAlert.setAlert(alert[action as keyof typeof alert][0], alert[action as keyof typeof alert][1]);

      Object.keys(itemForm.value).forEach(key => {
        delete itemForm.value[key as keyof typeof itemForm.value];
      });
      itemAction.value = '';
      itemId.value = '';
      getContacts(currenData.value.currentPath, currenData.value.currentPage);

    } catch (error) {
      console.log(error)
    }
  };

  return { data, searchData, currenData, itemAction, itemId, itemForm, getContacts, prevPage, nextPage, updateItem };
});