<script setup lang="ts">

import { classifyStore } from '@/store/classify';
import { adminStore } from '@store/admin';
import { alertStore } from '@store/alert';
import { authStore } from '@/store/token';
import { server } from '@share/utilities';
import UserForm from '@components/forms/UserForm.vue'

const storeAdmin = adminStore();
const storeClassify = classifyStore();
const storeAlert = alertStore();
const storeAuth = authStore();

async function userDelete(): Promise<void>{
  if (confirm("Вы действительно хотите удалить пользователя?")){
    try {
      const response = await storeAuth.axiosInstance.delete(
        `${server}/user/${storeAdmin.userData.userId}`
        );
      console.log(response.status);

      storeAlert.setAlert('alert-danger', 'Пользователь удалён');
      storeAdmin.getUsers();

    } catch (error) {
      console.error(error);
    }
  }
};

async function addGroupRole(item: string, value: string): Promise<void> {
  if (value !== '') {
    try {
      const response = await storeAuth.axiosInstance.get(
        `${server}/${item}/${value}/${storeAdmin.userData.userId}`
        );
      console.log(response.status);
    
    } catch (error) {
      console.error(error);
      storeAlert.setAlert('alert-danger', 'Ошибка');
    };
    storeAdmin.userAction('view', storeAdmin.userData.userId);
  }
};

async function delRoleGroup(item: string, value: string): Promise<void> {
  
  try {
    const response = await storeAuth.axiosInstance.delete(
      `${server}/${item}/${value}/${storeAdmin.userData.userId}`
      );
    console.log(response.status);

  } catch (error) {
    console.error(error);
    storeAlert.setAlert('alert-danger', 'Ошибка удаления');
  }
  storeAdmin.userAction('view', storeAdmin.userData.userId);
};

</script>

<template>
  <div class="modal" id="modalUser" data-bs-backdrop="static" data-bs-keyboard="false" 
       tabindex="-1" aria-labelledby="modalWinLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="modalUserLabel">Профиль пользователян</h1>
          <button @click="storeAdmin.userData.userAct = ''"
                  type="button" class="btn-close" data-bs-dismiss="modal" 
                  aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="py-2">

            <UserForm v-if="['create', 'edit'].includes(storeAdmin.userData.userAct)" />

            <div v-else>
              <table class="table table-responsive">
                <thead>
                  <tr><th colspan="2"># {{ storeAdmin.profileData.id }}</th></tr>
                </thead>
                <tbody>
                  <tr>
                    <td width="35%">Имя пользователя</td>
                    <td>{{storeAdmin.profileData.fullname }}</td>
                  </tr>
                  <tr>
                    <td>Логин</td>
                    <td>{{ storeAdmin.profileData.username }}</td>
                  </tr>
                  <tr>
                    <td>E-mail</td>
                    <td>{{ storeAdmin.profileData.email }}</td>
                  </tr>
                  <tr>
                    <td>Регион</td>
                    <td>{{ storeClassify.classifyItems.regions[storeAdmin.profileData.region_id] }}</td>
                  </tr>
                  <tr>
                    <td>Создан</td>
                    <td>{{ new Date(storeAdmin.profileData.pswd_create).toLocaleString('ru-RU') }}</td>
                  </tr>
                  <tr>
                    <td>Изменен</td>
                    <td>{{ new Date(storeAdmin.profileData.pswd_change).toLocaleString('ru-RU') }}</td>
                  </tr>
                  <tr>
                    <td>Вход</td>
                    <td>{{ new Date(storeAdmin.profileData.last_login).toLocaleString('ru-RU')}}</td>
                  </tr>
                  <tr><td>Группы</td>
                    <td>
                      <ul v-for="(group, index) in storeAdmin.profileData.groups" :key=index>
                        <li>{{ storeClassify.classifyItems.groups[group['group']] }}
                          <a href="#" @click="delRoleGroup('group', group['group'])">
                            <i class="bi bi-dash-circle"></i>
                          </a>
                        </li>
                      </ul>
                      <form class="form form-check" role="form">
                        <select class="form-select" id="group" name="group" 
                                v-model="storeAdmin.userData.userGroup" 
                                @change="addGroupRole('group', storeAdmin.userData.userGroup)">
                          <option value="" selected>Добавить группу</option>
                          <option v-for="(val, name) in storeClassify.classifyItems.groups" 
                                  :key="name" :value="name">
                            {{ val }}</option>
                        </select>
                      </form>
                    </td>
                  </tr>
                  <tr><td>Роли</td>
                    <td>
                      <ul v-for="(role, index) in storeAdmin.profileData.roles" :key=index>
                        <li>{{ role['role'] }}
                          <a href="#" @click="delRoleGroup('role',role['role'])">
                            <i class="bi bi-dash-circle"></i>
                          </a>
                        </li>
                      </ul>
                      <form class="form form-check" role="form">
                        <select class="form-select" id="role" name="role" 
                            v-model="storeAdmin.userData.userRole" 
                            @change="addGroupRole('role', storeAdmin.userData.userRole)">
                          <option value="" selected>Добавить роль</option>
                          <option v-for="(val, name) in storeClassify.classifyItems.roles" 
                                  :key="name" :value="val">
                            {{ val }}</option>
                        </select>
                      </form>
                    </td>
                  </tr>
                  <tr>
                    <td>Попыток входа</td>
                    <td>{{ storeAdmin.profileData.attempt }}</td>
                  </tr>
                  <tr>
                    <td>Блокировка</td>
                    <td>{{ storeAdmin.profileData.blocked ? 'Заблокирован' : 'Разблокирован' }}</td>
                  </tr>
                </tbody>
              </table>
              <div class="btn-group py-3" role="group">
                <button @click="storeAdmin.userAction('block')" class="btn btn-outline-primary">
                  {{storeAdmin.profileData.blocked ? "Разблокировать" : 'Заблокировать' }}
                </button>
                <button @click="storeAdmin.userData.userAct = 'edit';
                        storeAdmin.formData.fullname = storeAdmin.profileData.fullname;
                        storeAdmin.formData.email = storeAdmin.profileData.email;
                        storeAdmin.formData.username = storeAdmin.profileData.username;
                        storeAdmin.formData.region_id = storeAdmin.profileData.region_id;" 
                        class="btn btn-outline-primary">
                    Редактировать</button>
                <button @click="storeAdmin.userAction('drop')" class="btn btn-outline-primary">
                    Сбросить пароль</button>
                <button @click="userDelete" class="btn btn-outline-primary" data-bs-dismiss="modal" >
                    Удалить</button>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>

  html,
  body {
      scrollbar-gutter: stable;
  }

ul, li {
  padding: 0;
  list-style: none;
}

</style>