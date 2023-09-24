import { defineStore } from 'pinia';
import { appAuth } from '@/store/token';
import { ref } from 'vue';
import server from '@store/server';
import debounce from '@store/debounce';

export const appPersons = defineStore('appPersons',  () => {

  const storeAuth = appAuth();
  
  const candidates = ref<Candidate[]>([]);
  const has_prev = ref(false);
  const has_next = ref(false);
  const searchData = ref('');
  const currentPage = ref(1);
  const currentPath = ref('new');

interface Candidate {
  id: number;
  fullname: string;
  region_id: number;
  birthday: string;
  status: string;
  create: string;
}

  /**
   * Retrieves candidates from the specified URL and updates the data store.
   *
   * @param {string} url - The URL to retrieve candidates from.
   * @param {number} [page=1] - The page number of the candidates to retrieve. Default is 1.
   * @return {Promise<void>} - A promise that resolves when the candidates are retrieved and the data store is updated.
   */
  async function getCandidates(url: string=currentPath.value): Promise<void> {

    try {
      const response = await storeAuth.axiosInstance.post(`${server}/index/${url}/${currentPage.value}`, {'fullname': searchData.value});

      const [ datas, metadata ] = response.data;
      candidates.value = datas;
      has_prev.value = metadata.has_prev;
      has_next.value = metadata.has_next;

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
    if (has_prev.value) {
      currentPage.value -= 1;
      getCandidates(currentPath.value);
    }
  };

  /**
   * Moves to the next page if there is one available.
   *
   * @return {Promise<void>} A promise that resolves when the operation is complete.
   */
  function nextPage(): undefined {
    if (has_next.value) {
      currentPage.value += 1;
      getCandidates(currentPath.value);
    }
  };

  const searchPerson = debounce(getCandidates, 500);

  return { candidates, searchData, currentPath, has_next, has_prev,
     getCandidates, prevPage, nextPage, searchPerson };
});