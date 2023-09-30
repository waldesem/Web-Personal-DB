import { defineStore } from 'pinia';
import { ref } from 'vue'
import { appAuth } from '@/store/token';
import { appAlert } from '@store/alert';
import router from '@router/router';
import server from '@store/server';
import debounce from './debounce';


export const storeAdmin = defineStore('storeAdmin', () => {

  const storeAuth = appAuth();
  const storeAlert = appAlert();

  interface Group {
    id: string,
    group: string
  };

  interface Role {
    id: string,
    role: string
  };

  interface User {
    id: string,
    fullname: string,
    username: string,
    email: string,
    region_id: string,
    pswd_create: string,
    pswd_change: string,
    last_login: string,
    roles: Role[],
    groups: Group[],
    blocked: string,
    attempt: string
  };

  const userData = ref({
    userList: <User[]>([]),
    userId: '',
    userAct: '',
    userFlag: '',
    userRole: '',
    userGroup: '',
    currentPage: 1,
    hasNext: false,
    hasPrev: false,
  });

  const tableData = ref({
    table: '',
    tableItem: [],
    itemId: '',
    searchId: '',
    itemForm: <Record<string, any>>({}),
    itemAction: '',
    currentPage: 1,
    hasNext: false,
    hasPrev: false
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

  const tablesList = [
    'resume', 'staff', 'document', 'address', 'contact', 'workplace', 
    'relation', 'check', 'registry', 'poligraf','investigation',
    'inquiry', 'user'
  ];

  /**
   * Retrieves a list of users from the server.
   *
   * @return {Promise<void>} - A promise that resolves with the list of users 
   * retrieved from the server.
   */
  async function getUsers(): Promise<void>{
    try {
      const response = await storeAuth.axiosInstance.get(`${server}/users`);
      userData.value.userList = response.data;
    
    } catch (error) {
      console.error(error);
    }
  };

  /**
   * Fetches user data from the server based on the provided ID 
   * and updates the profile value.
   *
   * @param {String} id - The ID of the user to fetch data for.
   * @return {Promise<void>} - A promise that resolves when the user data 
   * is fetched and the profile value is updated.
   */
  async function userAction(action: String, id: string = userData.value.userId): Promise<void>{
    try {
      const response = await storeAuth.axiosInstance.get(`${server}/user/${action}/${id}`);
      profileData.value = response.data;
      
      if (action !== 'view') {
        const resp = {
          'block': ['alert-success', 'Пользователь (за/раз)блокирован'],
          'drop': ['alert-success', 'Пароль пользователя удален']
        };
        storeAlert.setAlert(resp[action as keyof typeof resp][0],
                            resp[action as keyof typeof resp][1]);
      };

    } catch (error) {
      console.error(error);
      userAction('view', userData.value.userId);
    }
  };

  async function userDelete(): Promise<void>{
    if (confirm("Вы действительно хотите удалить пользователя?")){
      try {
        const response = await storeAuth.axiosInstance.delete(
          `${server}/user/${userData.value.userId}`
          );
        console.log(response.status);

        storeAlert.setAlert('alert-danger', 'Пользователь удалён');
        router.push({ name: 'users', params: { group: 'admins' } });

      } catch (error) {
        console.error(error);
      }
    }
  };

  /**
   * Submits data to the server.
   *
   * @return {Promise<void>} A promise that resolves when the data is 
   * successfully submitted.
   */
  async function submitUserData(): Promise<void>{
    const formData = {
      'fullname': profileData.value.fullname,
      'username': profileData.value.username,
      'email': profileData.value.email,
      'region_id': profileData.value.region_id,
    };
    try {  
      const response = userData.value.userAct === 'edit' 
        ? await storeAuth.axiosInstance.patch(`${server}/user`, formData)
        : await storeAuth.axiosInstance.post(`${server}/user`, formData);
      const { message } = response.data;

      const resp = {
        'Created': ['alert-success', 'Пользователь успешно создан'],
        'Patched': ['alert-success', 'Пользователь успешно изменен'],
      }
      storeAlert.setAlert(resp[message as keyof typeof resp][0],
                          resp[message as keyof typeof resp][1]);
      userData.value.userAct === 'edit' 
        ? userAction('view', userData.value.userId): getUsers();
      userData.value.userId = '';
      userData.value.userAct = '';

    } catch (error) {
      console.error(error);
      storeAlert.setAlert('alert-danger', 'Ошибка сохранения данных');
    }
    Object.assign(profileData.value, {
      fullname: '',
      username: '',
      email: '',
      region_id: '',
    });
  };

  async function addGroupRole(item: string, value: string): Promise<void> {
    if (value !== '') {
      try {
        const response = await storeAuth.axiosInstance.get(
          `${server}/${item}/${value}/${userData.value.userId}`
          );
        console.log(response.status);
        storeAlert.setAlert('alert-success', 
                            'Пользователю добавлена роль \
                            либо он включен в группу');
        userAction('view', userData.value.userId);
      
      } catch (error) {
        console.error(error);
        storeAlert.setAlert('alert-danger', 'Ошибка');
        userAction('view', userData.value.userId);
      }
    }
  };

  async function delRoleGroup(item: string, value: string): Promise<void> {
    
    try {
      const response = await storeAuth.axiosInstance.delete(
        `${server}/${item}/${value}/${userData.value.userId}`
        );
      console.log(response.status);
      storeAlert.setAlert('alert-success', 'Группа или роль удалена');
      userAction('view', userData.value.userId);

    } catch (error) {
      console.error(error);
      storeAlert.setAlert('alert-danger', 'Ошибка удаления');
      userAction('view', userData.value.userId);
    }
  };

  /**
   * Retrieves a list of users from the server.
   *
   * @return {Promise<void>} - A promise that resolves with the list of users 
   * retrieved from the server.
   */
  async function getItem(): Promise<void>{
    try {
      const response = await storeAuth.axiosInstance.get(
        `${server}/table/${tableData.value.table}/${tableData.value.currentPage}`
      );
      const [ datas, has_prev, has_next ] = response.data;
      tableData.value.tableItem = datas;
      tableData.value.hasPrev = has_prev['has_prev'];
      tableData.value.hasNext = has_next['has_next'];

    } catch (error) {
      console.error(error);
    }
  };

  async function searchItem(): Promise<void> {
    if (tableData.value.searchId === '') {
      getItem();
      return
    }
    try {
      const response = await storeAuth.axiosInstance.post(
        `${server}/table/${tableData.value.table}/${tableData.value.currentPage}`, {
          'id': tableData.value.searchId
        }
        );
      const [ datas, has_prev, has_next ] = response.data;

        tableData.value.tableItem =  datas;
        tableData.value.hasPrev = has_prev['has_prev'];
        tableData.value.hasNext = has_next['has_next'];

    } catch (error) {
      console.error(error);
    }
  };

  async function deleteItem(idItem: string): Promise<void>{
    try {
      const response = await storeAuth.axiosInstance.delete(
        `${server}/table/${tableData.value.table}/${idItem}`);
      console.log(response.status);
      getItem();
    
    } catch (error) {
      console.error(error);
    }
  };

  async function updateItem(item: string): Promise<void>{
    try {
      const response = await storeAuth.axiosInstance.get(
        `${server}/table/${item}/${tableData.value.itemId}`
        );
      console.log(response.status);
      getItem();

    } catch (error) {
      console.error(error);
    }
  };

  function switchPage(
    hasPage: boolean, currPage: number, action: string, flag: string
    ): undefined {
    if (hasPage && action === 'previous') {
      currPage -= 1;
    } else if (hasPage && action === 'next'){
      currPage += 1;
    };
    flag === 'users' ? getUsers() : searchItem();
  };

  const idHandler = debounce(searchItem, 500);

  return { userData, tableData, profileData, tablesList,
    getUsers, submitUserData, userAction, userDelete, addGroupRole, 
    delRoleGroup, getItem, idHandler, switchPage, updateItem, deleteItem };
});
