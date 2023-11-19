import { defineStore } from 'pinia';
import { ref } from 'vue'
import { authStore } from '@/store/token';
import { alertStore } from '@store/alert';
import { server, clearItem } from '@share/utilities';
import { User } from '@share/interfaces';
import router from '@/router/router';


export const adminStore = defineStore('adminStore', () => {

  const storeAuth = authStore();
  const storeAlert = alertStore();

  const userData = ref({
    userList: <User[]>([]),
    userId: '',
    userAct: '',
    userFlag: '',
    userRole: '',
    userGroup: '',
    searchUser: ''
  });

  const profileData = ref<User>({
    id: '',
    fullname: '',
    region_id: '',
    username: '',
    email: '',
    pswd_create: '',
    pswd_change: '',
    last_login: '',
    roles: [],
    groups: [],
    blocked: '',
    attempt: ''
  });

  const tableData = ref({
    table: '',
    tableItem: [],
    searchId: '',
    currentPage: 1,
    hasNext: false,
    hasPrev: false
  });

  const formData: Record<string, any> = ref({});

  /**
   * Retrieves a list of users from the server.
   *
   * @return {Promise<void>} - A promise that resolves with the list of users 
   * retrieved from the server.
   */
  async function getUsers(): Promise<void>{
    try {
      const response = await storeAuth.axiosInstance.post(`${server}/users`,
      {
        'fullname': userData.value.searchUser 
      });
      userData.value.userList = response.data;
    
    } catch (error) {
      storeAlert.setAlert('alert-success', error as string)
    }
  };

  /**
   * Submits data to the server.
   *
   * @return {Promise<void>} A promise that resolves when the data is 
   * successfully submitted.
   */
  async function submitUser(): Promise<void>{
    try {  
      const response = userData.value.userAct === 'edit' 
        ? await storeAuth.axiosInstance.patch(`${server}/user`, formData.value)
        : await storeAuth.axiosInstance.post(`${server}/user`, formData.value);
      
      if (userData.value.userAct === 'edit') {
        profileData.value = response.data;
        storeAlert.setAlert('alert-success', 'Пользователь успешно изменен')
      } else {
        userData.value.userList = response.data;
        storeAlert.setAlert('alert-success', 'Пользователь успешно создан')
      };

    } catch (error) {
      console.error(error);
      storeAlert.setAlert('alert-danger', 'Ошибка сохранения данных');
    };
    clearItem(formData.value);
  };

  async function userAction(action: String): Promise<void>{
    try {
      const response = await storeAuth.axiosInstance.get(
        `${server}/user/${action}/${userData.value.userId}`
        );
      profileData.value = response.data;

      if (action === 'drop'){
        storeAlert.setAlert('alert-success', 'Пароль сброшен');
      } else if (action === 'block') {
        storeAlert.setAlert('alert-success', 
          `Пользователь ${profileData.value.blocked ? 'заблокирован' : 'разблокирован'}`);
      };
    } catch (error) {
      storeAlert.setAlert('alert-success', error as string)
    }
  };

  async function userDelete(): Promise<void>{
    if (confirm("Вы действительно хотите удалить пользователя?")){
      try {
        const response = await storeAuth.axiosInstance.delete(
          `${server}/user/${userData.value.userId}`
          );
        profileData.value = response.data;
        storeAlert.setAlert('alert-success', 'Пользователь удалён');
        router.push({ name: 'users' });
    
      } catch (error) {
        storeAlert.setAlert('alert-danger', error as string)
      }
    }
  };
  
  async function updateGroupRole(action: string, item: string, value: string): Promise<void> {
    if (value !== '') {
      try {
        const response = action === 'add' 
          ? await storeAuth.axiosInstance.get(
            `${server}/${item}/${value}/${userData.value.userId}`
            )
          : await storeAuth.axiosInstance.delete(
            `${server}/${item}/${value}/${userData.value.userId}`
            );
        profileData.value = response.data;
        
        storeAlert.setAlert(
          'alert-success', 
          `${item === 'role' ? "Роль" : "Группа"} ${value} ${action === 'add' ? "добавлена" : "удалена"}`
          );
  
      } catch (error) {
        storeAlert.setAlert('alert-danger', error as string);
      };
    }
  };
  
  async function getItem(page = tableData.value.currentPage): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.post(
        `${server}/table/${tableData.value.table}/${page}`, {
          'id': tableData.value.searchId
        }
      );
      const [ datas, metadata ] = response.data;

      tableData.value.tableItem = datas;
      tableData.value.hasNext = metadata.has_next;
      tableData.value.hasPrev = metadata.has_prev;
      
    } catch (error) {
      storeAlert.setAlert('alert-warning', error as string);
    }
  };

  async function deleteItem(idItem: string): Promise<void>{
    if (confirm(`Вы действительно хотите удалить запись?`)) {
      try {
        const response = await storeAuth.axiosInstance.delete(
          `${server}/table/${tableData.value.table}/${idItem}`);
        console.log(response.status);
        storeAlert.setAlert('alert-warning', 
                            `Запись ${idItem} из ${tableData.value.table} удалена`);
        getItem();
      } catch (error) {
        storeAlert.setAlert('alert-warning', error as string);
      }
    };
  };

  return {
    formData,
    userData, 
    profileData,
    tableData,
    getUsers, 
    submitUser,
    userAction,
    userDelete,
    updateGroupRole,
    getItem,
    deleteItem
  };
});
