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

  const searchData = ref('');
  const currentPage = ref(1);
  const itemAction = ref('');
  const itemId = ref('');
  const itemForm = ref({
    company: '',
    city: '',
    fullname: '',
    contact: '',
    comment: ''
  });
  const data = ref({
    contacts: [],
    companies: [],
    cities: [],
    hasPrev: false,
    hasNext: false
  });

  /**
   * Retrieves contacts from the server and updates the data value with the response.
   *
   * @return {Promise<void>} A Promise that resolves when the contacts have been retrieved and the data value has been updated.
   */
  async function getContacts(): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.post(`${server}/connects/${storeLogin.pageIdentity}/${currentPage.value}`, {
          'company': searchData.value
        });
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
   * Updates a contact based on the provided flag and contact ID.
   *
   * @param {Event} _event - The event triggering the update.
   * @param {string} flag - The flag indicating the action to perform (default: "itemAction.value").
   * @param {string} contactId - The ID of the contact to update (default: "itemId.value").
   * @return {Promise<void>} - A promise that resolves when the update is complete.
   */
  async function updateContact(
    _event: Event, flag: string=itemAction.value, contactId: string=itemId.value
    ): Promise<void> {
    try {
      const response = flag === 'create'
        ? await storeAuth.axiosInstance.post(
          `${server}/connect/${storeLogin.pageIdentity}`, itemForm.value
          )
        : await storeAuth.axiosInstance.patch(
          `${server}/connect/${contactId}`, itemForm.value
          );
      const { item_id } = response.data;

      const alert = {
        'create': ['alert-success', `Создан контакт ID ${item_id}`],
        'edit': ['alert-info', `Контакт ID ${item_id} обновлен`]
      };
      storeAlert.setAlert(alert[flag as keyof typeof alert][0], 
                                alert[flag as keyof typeof alert][1]);
      getContacts();
      itemAction.value = '';
      itemId.value = '';
      Object.assign(itemForm.value, {
        company: '',
        city: '',
        fullname: '',
        contact: '',
        comment: ''
      })

    } catch (error) {
      console.log(error)
    }
  };

  /**
   * Deletes a contact.
   *
   * @param {Event} _event - the event object
   * @param {string} contactId - the ID of the contact to delete
   * @return {Promise<void>} a Promise that resolves when the contact is deleted
   */
  async function deleteContact(_event: Event, contactId: string=itemId.value): Promise<void> {

    try {
      const response = await storeAuth.axiosInstance.delete(`${server}/connect/${contactId}`);
      console.log(response.status);
      storeAlert.setAlert('alert-success', `Контакт с ID ${contactId} удален`);

      getContacts();

    } catch (error) {
      console.log(error)
      
      storeAlert.setAlert('alert-danger', `Ошибка при удалении контакта с ID ${contactId}`);
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
      currentPage.value -= 1;
      getContacts();
    }
  };

  /**
   * Moves to the next page if there is one available.
   *
   * @return {Promise<void>} A promise that resolves when the operation is complete.
   */
  function nextPage(): undefined {
    if (data.value.hasNext) {
      currentPage.value += 1;
      getContacts();
    }
  };

  const searchContacts = debounce(getContacts, 500);

  return { data, searchData, itemAction, itemId, itemForm, getContacts, prevPage, nextPage, deleteContact, updateContact, searchContacts };
});