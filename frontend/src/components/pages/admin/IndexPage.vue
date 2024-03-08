<script setup lang="ts">
import { computed, defineAsyncComponent, onBeforeMount, ref } from "vue";
import { authStore } from "@/store/auth";
import { alertStore } from "@store/alert";
import { server, debounce } from "@utilities/utils";
import { User } from "@/interfaces/interface";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/layouts/HeaderDiv.vue")
);
const UserForm = defineAsyncComponent(
  () => import("@components/content/admin/forms/UserForm.vue")
);
const ModalWin = defineAsyncComponent(
  () => import("@components/layouts/ModalWin.vue")
);

const storeAlert = alertStore();
const storeAuth = authStore();

const searchUsers = debounce(() => {
  dataUsers.value.getUsers();
}, 500);

onBeforeMount( async () => {
  await dataUsers.value.getUsers();
});

const users = computed(() => {
  return dataUsers.value.users.filter(
    (user: User) => user.deleted === dataUsers.value.viewDeleted
  );
});

const dataUsers = ref({
  action: "",
  search: "",
  viewDeleted: false,
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
});

async function getEmit () {
  dataUsers.value.action = '';
  await dataUsers.value.getUsers();
};
</script>

<template>
  <div class="container py-1">
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
    <div class="form-check form-switch d-flex justify-content-end">
      <input class="form-check-input" id="deleted" type="checkbox" v-model="dataUsers.viewDeleted" />&nbsp;
      <label class="form-check-label" for="deleted">Показать удаленные</label>
    </div>
    <div class="overflow py-2">
      <table class="table table-responsive align-middle">
        <thead>
          <tr height="50px">
            <th width="5%">#</th>
            <th>Имя пользователя</th>
            <th width="20%">Логин</th>
            <th width="10%">Блокировка</th>
            <th width="20%">Создан</th>
            <th width="20%">Вход</th>
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
                    v-for="user in users"
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
                    <td width="10%">{{ user.blocked }}</td>
                    <td width="20%">
                      {{ new Date(user.pswd_create).toLocaleString("ru-RU") }}
                    </td>
                    <td width="20%">
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
    <ModalWin
      :title="'Добавить пользователя'"
      :id="'modalUser'"
      @cancel="dataUsers.action = ''"
    >
      <UserForm
        :action="dataUsers.action"
        @update="getEmit"
      />
    </ModalWin>
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
