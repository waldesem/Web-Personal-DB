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
const InputLabel = defineAsyncComponent(
  () => import("@components/elements/InputLabel.vue")
);
const CheckBox = defineAsyncComponent(
  () => import("@components/elements/CheckBox.vue")
);
const TableSlots = defineAsyncComponent(
  () => import("@components/elements/TableSlots.vue")
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
      <InputLabel
        :lbl-cls="'visually-hidden'"
        :cls-input="'col-lg-12'"
        :lbl="'Поиск'"
        :id="'fullusername'"
        :name="'fullusername'"
        v-model="dataUsers.search"
      />
    </form>
    <CheckBox
      :name="'viewDeleted'"
      :label="'Показать удаленные'"
      v-model="dataUsers.viewDeleted"
    />
    <TableSlots :tbl-caption="'Список пользователей'">
      <template v-slot:thead>
        <tr height="50px">
          <th width="5%">#</th>
          <th>Имя пользователя</th>
          <th width="20%">Логин</th>
          <th width="10%">Блокировка</th>
          <th width="20%">Создан</th>
          <th width="20%">Вход</th>
        </tr>
      </template>
      <template v-slot:tbody>
        <tr>
          <td colspan="6">
            <TableSlots
              :tbl-class="'table table-hover table-responsive align-middle no-bottom-border'"            
            >
              <template v-slot:tbody>
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
              </template>
            </TableSlots>
          </td>
        </tr>
      </template>
    </TableSlots>
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
