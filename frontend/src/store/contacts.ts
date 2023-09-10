import { defineStore } from 'pinia';
import { appAuth } from '@store/auth';
import { ref } from 'vue';
import server from '@store/server';


export const storeContact = defineStore('storeContact',  () => {

  const storeAuth = appAuth();
  
  const contactId = ref('');
  
  const data = ref({
    сontacts: [],
    hasPrev: false,
    hasNext: false
  });

  const organization = ref('');
  
  const currenData = ref({
    currentPage: 1,
    currentPath: 'list'
  });


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
        ? await storeAuth.axiosInstance.post(`${server}/contact/${url}/${page}`, organization.value) 
        : await storeAuth.axiosInstance.get(`${server}/contact/${url}/${page}`);

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

  return { data, organization, currenData, contactId, getContacts, prevPage, nextPage };
});