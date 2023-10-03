import { defineStore } from 'pinia';
import { authStore } from '@/store/token';
import { ref } from 'vue';
import server from '@store/server';
import debounce from '@store/debounce';

export const personStore = defineStore('personStore', () => {

  const storeAuth = authStore();
  
  interface Candidate {
    id: number;
    fullname: string;
    region_id: number;
    birthday: string;
    status: string;
    create: string;
  };

  const personData = ref({
    candidates: <Candidate[]>([]),
    has_prev: false,
    has_next: false,
    searchData: '',
    currentPage: 1,
    currentPath: 'new'
  });

  /**
   * Retrieves candidates from the specified URL and updates the data store.
   *
   * @param {string} url - The URL to retrieve candidates from.
   * @return {Promise<void>} - A promise that resolves when the candidates are 
   * retrieved and the data store is updated.
   */
  async function getCandidates(url: string=personData.value.currentPath): Promise<void> {

    try {
      const response = await storeAuth.axiosInstance.post(
        `${server}/index/${url}/${personData.value.currentPage}`, 
          {'fullname': personData.value.searchData}
        );

      const [ datas, metadata ] = response.data;
      personData.value.candidates = datas;
      personData.value.has_prev = metadata.has_prev;
      personData.value.has_next = metadata.has_next;

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
    if (personData.value.has_prev) {
      personData.value.currentPage -= 1;
      getCandidates(personData.value.currentPath);
    }
  };

  /**
   * Moves to the next page if there is one available.
   *
   * @return {Promise<void>} A promise that resolves when the operation is complete.
   */
  function nextPage(): undefined {
    if (personData.value.has_next) {
      personData.value.currentPage += 1;
      getCandidates(personData.value.currentPath);
    }
  };

  const searchPerson = debounce(getCandidates, 500);

  return { personData, getCandidates, prevPage, nextPage, searchPerson };
});