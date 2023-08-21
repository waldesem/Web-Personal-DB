import { ref } from 'vue';
import { defineStore } from 'pinia';
import { appAuth } from '@store/auth';
import { appAlert } from '@/store/alert';
import server from '@store/server';


const storeAuth = appAuth()

const storeAlert = appAlert();


export const appPersons = defineStore('appPersons',  () => {

  const data = ref({
    candidates: [],
    hasPrev: false,
    hasNext: false,
  });

  const searchData = ref({
    fullname: '',
    birthday: '',
  });

  const currenData = ref({
    currentPage: 1,
    currentPath: 'new'
  })

  /**
   * Retrieves candidates from the specified URL and updates the data store.
   *
   * @param {string} url - The URL to retrieve candidates from.
   * @param {number} [page=1] - The page number of the candidates to retrieve. Default is 1.
   * @return {Promise<void>} - A promise that resolves when the candidates are retrieved and the data store is updated.
   */
  async function getCandidates(url: string, page: number=1): Promise<void> {
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
  const prevPage = (): void => {
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
  const nextPage = (): void => {
    if (data.value.hasNext) {
      currenData.value.currentPage += 1;
      getCandidates(currenData.value.currentPath, currenData.value.currentPage);
    }
  };

  const dropData = () => {
    searchData.value = {
      fullname: '',
      birthday: '',
    }
  };

  /**
   * Deletes a person record.
   *
   * @param {String} id - The ID of the person to delete.
   * @return {Promise} A promise that resolves with the result of the deletion.
   */
  async function delPerson(id: String): Promise<any> {
    if (confirm(`Вы действительно хотите удалить анкету?`)) {
      const response = await storeAuth.axiosInstance.get(`${server}/person/delete/${id}`, {
      headers: {'Authorization': `Bearer ${localStorage.getItem('access_token')}`}
    });
      const  { person } = response.data;
      
      storeAlert.alertAttr = 'alert-success';
      storeAlert.alertText = `Анкета ${person} удален`;

      getCandidates(currenData.value.currentPath);
    }
  };
  return { data, searchData, currenData, getCandidates, delPerson, prevPage, nextPage, dropData }
});