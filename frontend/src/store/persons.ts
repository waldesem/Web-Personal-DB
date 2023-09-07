import { defineStore } from 'pinia';
import { appAuth } from '@store/auth';
import { ref } from 'vue';
import server from '@store/server';


export const appPersons = defineStore('appPersons',  () => {

  const storeAuth = appAuth();
  
  const data = ref({
    candidates: [],
    hasPrev: false,
    hasNext: false
  });

  const searchData = ref({
    fullname: '',
    birthday: ''
  });
  
  const currenData = ref({
    currentPage: 1,
    currentPath: 'new'
  });


  /**
   * Retrieves candidates from the specified URL and updates the data store.
   *
   * @param {string} url - The URL to retrieve candidates from.
   * @param {number} [page=1] - The page number of the candidates to retrieve. Default is 1.
   * @return {Promise<void>} - A promise that resolves when the candidates are retrieved and the data store is updated.
   */
  async function getCandidates(url: string=currenData.value.currentPath, page: number=1): Promise<void> {
    currenData.value.currentPage = page;
    currenData.value.currentPath = url;

    try {
      const response = url === 'search' 
        ? await storeAuth.axiosInstance.post(`${server}/index/${url}/${page}`, {
            "fullname": searchData.value.fullname, 
            "birthday": searchData.value.birthday
          }) 
        : await storeAuth.axiosInstance.get(`${server}/index/${url}/${page}`);

      const [ datas, metadata ] = response.data;
      Object.assign(data.value, {
        candidates: datas,
        hasPrev: metadata.has_prev,
        hasNext: metadata.has_next
      })

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
      getCandidates(currenData.value.currentPath, currenData.value.currentPage);
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
      getCandidates(currenData.value.currentPath, currenData.value.currentPage);
    }
  };

  return { data, searchData, currenData, getCandidates, prevPage, nextPage };
});