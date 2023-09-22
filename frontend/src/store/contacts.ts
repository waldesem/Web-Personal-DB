import { defineStore } from 'pinia';
import { appAuth } from '@/store/token';
import { appLogin } from '@store/login';
import { appAlert } from '@store/alert';
import { ref } from 'vue';
import server from '@store/server';
import debounce from '@store/debounce';

export const storeContact = defineStore('storeContact',  () => {

  const storeAuth = appAuth();
  const storeLogin = appLogin();
  const storeAlert = appAlert();

  const data = ref({
    contacts: [],
    companies: [],
    cities: [],
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
    company: '',
    city: '',
    fullname: '',
    contact: '',
    comment: ''
  });

  async function getContacts(url: string=currenData.value.currentPath, page: number=1): Promise<void> {
    currenData.value.currentPage = page;
    currenData.value.currentPath = url;
    
    try {
      const response = url === 'search' 
        ? await storeAuth.axiosInstance.post(`${server}/contacts/${storeLogin.pageIdentity}/${url}/${page}`, {
          'company': searchData.value
        })
        : await storeAuth.axiosInstance.get(`${server}/contacts/${storeLogin.pageIdentity}/${url}/${page}`);
      const [ datas, has_prev, has_next, companies, cities ] = response.data;

      Object.assign(data.value, {
        contacts: datas,
        hasPrev: has_prev['has_prev'],
        hasNext: has_next['has_next'],
        companies: companies['companies'],
        cities: cities['cities'],
      });

    } catch (error) {
      console.error(error);
    }
  };

  /**
   * Moves to the previous page if it exists.
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
  async function updateItem(_event: Event, flag: string=itemAction.value, contactId: string=itemId.value): Promise<void> {

    try {
      const response = flag === 'create' || flag === 'edit'
      ? await storeAuth.axiosInstance.post(`${server}/contact/${storeLogin.pageIdentity}/${flag}/${contactId}`, {
        'company': itemForm.value.company,
        'city': itemForm.value.city,
        'fullname': itemForm.value.fullname,
        'contact': itemForm.value.contact,
        'comment': itemForm.value.comment
        }
      )
      : await storeAuth.axiosInstance.delete(`${server}/contact/${storeLogin.pageIdentity}/${flag}/${contactId}`);

      const { action, item_id } = response.data;

      const alert = {
        'create': ['alert-success', `Создан контакт с ID ${item_id}`],
        'edit': ['alert-info', `Контакт с ID ${item_id} обновлен`],
        'delete': ['alert-warning', `Контакт с ID ${item_id} удален`]
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

  const searchContacts = debounce(getContacts, 500);

  return { data, searchData, currenData, itemAction, itemId, itemForm, getContacts, prevPage, nextPage, updateItem, searchContacts };
});