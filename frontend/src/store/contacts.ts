import { defineStore } from 'pinia';
import { ref } from 'vue';
import { authStore } from '@/store/token';
import { alertStore } from '@store/alert';
import { loginStore } from '@store/login';
import { clearItem, server } from '@share/utilities';


export const contactStore = defineStore('contactStore', () => {

  const storeAuth = authStore();
  const storeLogin = loginStore();
  const storeAlert = alertStore();

  const itemForm: Record<string, any> = ref({});

  const contactsData = ref({
    searchData: '',
    currentPage: 1,
    itemAction: '',
    itemId: '',
  });
  
  const responseData = ref({
    contacts: [],
    companies: [],
    cities: [],
    hasPrev: false,
    hasNext: false
  });

  /**
   * Retrieves contacts from the server and updates the data value with the response.
   *
   * @return {Promise<void>} A Promise that resolves when the contacts have 
   * been retrieved and the data value has been updated.
   */
  async function getContacts(page = contactsData.value.currentPage): Promise<void> {

    try {
      const response = await storeAuth.axiosInstance.post(
        `${server}/connects/${storeLogin.pageIdentity}/${page}`, {
          'search': contactsData.value.searchData
        }
      );
      const [ datas, has_prev, has_next, companies, cities ] = response.data;

      Object.assign(responseData.value, {
        contacts: datas,
        hasPrev: has_prev.has_prev,
        hasNext: has_next.has_next,
        companies: companies.companies,
        cities: cities.cities,
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
    event: Event, 
    flag: string=contactsData.value.itemAction, 
    contactId: string=contactsData.value.itemId
    ): Promise<void> {
    
    event.preventDefault();
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
      contactsData.value.itemAction = '';
      contactsData.value.itemId = '';
      clearItem(itemForm.value);

    } catch (error) {
      console.log(error)
    }
  };

  /**
   * Deletes a contact.
   *
   * @param {string} contactId - the ID of the contact to delete
   * @return {Promise<void>} a Promise that resolves when the contact is deleted
   */
  async function deleteContact(contactId: string=contactsData.value.itemId): Promise<void> {
    if (confirm("Вы действительно хотите удалить контакт?")) {
      try {
        const response = await storeAuth.axiosInstance.delete(`${server}/connect/${contactId}`);
        console.log(response.status);
        storeAlert.setAlert('alert-success', `Контакт с ID ${contactId} удален`);
        contactsData.value.currentPage = 1; // reset page
        getContacts();

      } catch (error) {
        console.log(error)
        
        storeAlert.setAlert('alert-danger', `Ошибка при удалении контакта с ID ${contactId}`);
      }
    }
  };

  return { 
    responseData, 
    contactsData,
    itemForm,
    getContacts, 
    updateContact,
    deleteContact
  };
});