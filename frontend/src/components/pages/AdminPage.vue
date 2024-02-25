<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { authStore } from "@/store/token";
import { alertStore } from "@store/alert";
import { server, debounce } from "@utilities/utils";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/layouts/HeaderDiv.vue")
);
const UserForm = defineAsyncComponent(
  () => import("@components/forms/UserForm.vue")
);

const storeAlert = alertStore();
const storeAuth = authStore();

interface Group {
  id: string;
  group: string;
}

interface Role {
  id: string;
  role: string;
}

interface User {
  id: string;
  fullname: string;
  username: string;
  email: string;
  pswd_create: string;
  pswd_change: string;
  last_login: string;
  roles: Role[];
  groups: Group[];
  blocked: boolean;
  deleted: boolean;
  attempt: string;
}

const searchUsers = debounce(() => {
  dataUsers.value.getUsers();
}, 500);

onBeforeMount( async() => {
  await  dataUsers.value.getUsers();
});

const dataUsers = ref({
  action: "",
  search: "",
  users: <User[]>[],

  getUsers: async function () {
    try {
      const response = await storeAuth.axiosInstance.get(`${server}/users`, {
        params: {
          search: this.search,
        }
      });
      this.users = response.data;
    } catch (error) {
      storeAlert.alertMessage.setAlert("alert-success", error as string);
    }
  },

  deactivateAction: function (){
    this.action = ""
  }
});
</script>

<template>
  <div class="container py-3">
    <HeaderDiv :page-header="'Список пользователей'" :cls="'text-secondary'" />
    <form @input.prevent="searchUsers" class="form form-check" role="form">
      <div class="row py-3">
        <input
          class="form-control"
          id="fullusername"
          name="fullusername"
          type="text"
          v-model="dataUsers.search"
        />
      </div>
    </form>
    <div class="overflow py-2">
      <table class="table table-responsive align-middle">
        <thead>
          <tr height="50px">
            <th width="5%">#</th>
            <th>Имя пользователя</th>
            <th width="20%">Логин</th>
            <th width="15%">Блокировка</th>
            <th width="15%">Создан</th>
            <th width="15%">Вход</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td colspan="6">
              <table
                class="table table-hover table-responsive align-middle no-bottom-border"
              >
                <tbody>
                  <tr
                    height="50px"
                    v-for="user in dataUsers.users"
                    :key="user.id"
                  >
                    <td width="5%">{{ user.id }}</td>
                    <td>{{ user.fullname }}</td>
                    <td width="20%">
                      <router-link
                        :to="{ name: 'user', params: { id: user.id } }"
                      >
                        {{ user.username }}
                      </router-link>
                    </td>
                    <td width="15%">{{ user.blocked }}</td>
                    <td width="15%">
                      {{ new Date(user.pswd_create).toLocaleString("ru-RU") }}
                    </td>
                    <td width="15%">
                      {{ new Date(user.last_login).toLocaleString("ru-RU") }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <button
      class="btn btn-outline-secondary"
      data-bs-toggle="modal"
      data-bs-target="#modalUser"
      @click="dataUsers.action = 'create'"
    >
      Добавить пользователя
    </button>
    <UserForm
      :action="dataUsers.action"
      :item="{}"
      :getUsers="dataUsers.getUsers"
      @deactivate="dataUsers.deactivateAction"
    />
  </div>
</template>

<style scoped>
.overflow {
  max-height: 75vh;
  overflow-y: auto;
}
.no-bottom-border td {
  border-bottom: none;
}
</style>
