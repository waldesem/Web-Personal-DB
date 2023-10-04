import { defineStore } from 'pinia';
import { authStore } from '@/store/token';
import { loginStore } from '@store/login';
import { ref } from 'vue';
import server from '@store/server';


export const contactStore = defineStore('contactStore', () => {

  const storeAuth = authStore();
  const storeLogin = loginStore();

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
   * @return {Promise<void>} A Promise that resolves when the contacts have been retrieved and the data value has been updated.
   */
  async function getContacts(): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.post(
        `${server}/connects/${storeLogin.pageIdentity}/${currentPage.value
        }`, {
          'company': searchData.value
        });
      const [ datas, has_prev, has_next, companies, cities ] = response.data;

      Object.assign(responseData.value, {
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

  return { 
    responseData, 
    searchData, 
    itemAction, 
    itemId, 
    itemForm, 
    currentPage,
    getContacts, 
  };
});