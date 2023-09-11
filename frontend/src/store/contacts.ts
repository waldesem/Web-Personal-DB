import { defineStore } from 'pinia';
import { appAuth } from '@store/auth';
import { appLogin } from '@store/login';
import { ref } from 'vue';
import server from '@store/server';


export const storeContact = defineStore('storeContact',  () => {

  const storeAuth = appAuth();
  const storeLogin = appLogin();
  
  const contactId = ref('');
  
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

  const contactData = ref({
    organization: '', 
    locations: [], 
    connects: [], 
    contacts: []
  })


  /**
   * Retrieves candidates from the specified URL and updates the data store.
   *
   * @param {string} url - The URL to retrieve candidates from.
   * @param {number} [page=1] - The page number of the candidates to retrieve. Default is 1.
   * @return {Promise<void>} - A promise that resolves when the candidates are retrieved and the data store is updated.
   */
  async function getContacts(url: string=currenData.value.currentPath, page: number=1): Promise<void> {
    currenData.value.currentPage = page;
    currenData.value.currentPath = url;

    try {
      const response = url === 'search' 
        ? await storeAuth.axiosInstance.post(`${server}/contacts/${storeLogin.pageIdentity}/${url}/${page}`, searchData.value) 
        : await storeAuth.axiosInstance.get(`${server}/contacts/${storeLogin.pageIdentity}/${url}/${page}`);

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

async function viewContact() {
  try{
    const response = await storeAuth.axiosInstance.get(`${server}/contact/${contactId.value}`);
    const { org, location, connect, contact } = response.data
    Object.assign(contactData.value, {
      organization: org,
      locations: location,
      connects: connect,
      contacts: contact
    })
  } catch (error) {
    console.error(error);
  }
};

  return { data, searchData, currenData, contactId, contactData, getContacts, prevPage, nextPage, viewContact };
});