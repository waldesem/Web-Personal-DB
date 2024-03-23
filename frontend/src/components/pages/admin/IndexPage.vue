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
const SwitchBox = defineAsyncComponent(
  () => import("@components/elements/SwitchBox.vue")
);
const TableSlots = defineAsyncComponent(
  () => import("@components/elements/TableSlots.vue")
);

const storeAlert = alertStore();
const storeAuth = authStore();

const searchUsers = debounce(() => {
  getUsers();
}, 500);

onBeforeMount( async () => {
  await getUsers();
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
});

async function getUsers() {
  try {
    const response = await storeAuth.axiosInstance.get(`${server}/users`, {
      params: {
        search: dataUsers.value.search,
      }
    });
    dataUsers.value.users = response.data;
  } catch (error) {
    storeAlert.alertMessage.setAlert("alert-success", error as string);
  }
};
</script>

<template>
  <div class="container py-1">
    <HeaderDiv :page-header="'Список пользователей'" :cls="'text-secondary'" />
    <form @input.prevent="searchUsers" class="form form-check" role="form">
      <div class="row mb-5">
        <input
          class="form-control"
          name="search"
          id="search"
          type="text"
          placeholder="Поиск по имени пользователя"
          v-model="dataUsers.search"
        />
      </div>
    </form>
    <div class="row">
      <div class="col-md-6">
        <SwitchBox
          :name="'viewDeleted'"
          :label="'Показать удаленные'"
          v-model="dataUsers.viewDeleted"
        />
      </div>
      <div class="col-md-6 text-end">
        <a
          class="link link-secondary"
          type="button"
          @click="dataUsers.action === '' 
            ? dataUsers.action = 'create' 
            : dataUsers.action = ''"
        >
          {{ dataUsers.action === '' ? 'Добавить пользователя' : 'Закрыть' }}
        </a>
      </div>
    </div>
    <UserForm v-if="dataUsers.action"
      :action="dataUsers.action"
      @update="dataUsers.action = ''; getUsers()"
    />
    <TableSlots 
      :tbl-caption="'Список пользователей'"
      :tbl-class="'table align-middle'"
    >
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
            <TableSlots id="overflow"
              :tbl-class="'table table-hover align-middle no-bottom-border'"            
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
  </div>
</template>

<style scoped>
#overflow {
  max-height: 50vh;
  overflow-y: auto;
}
.no-bottom-border td {
  border-bottom: none;
}
</style>
