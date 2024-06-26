<script setup lang="ts">
import { computed, defineAsyncComponent, onBeforeMount, ref } from "vue";
import { authErrorHandler, axiosAuth } from "@/auth";
import { debounce, timeSince } from "@/utilities";
import { User } from "@/interfaces";
import { server } from "@/state";
import { AxiosError } from "axios";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/content/elements/HeaderDiv.vue")
);
const UserForm = defineAsyncComponent(
  () => import("@components/content/forms/UserForm.vue")
);
const SwitchBox = defineAsyncComponent(
  () => import("@components/content/elements/SwitchBox.vue")
);
const TableSlots = defineAsyncComponent(
  () => import("@components/content/elements/TableSlots.vue")
);

const searchUsers = debounce(() => {
  getUsers();
}, 500);

onBeforeMount(() => {
  getUsers();
});

const users = computed(() => {
  return dataUsers.value.users.filter(
    (user: User) => user.deleted == dataUsers.value.viewDeleted
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
    const response = await axiosAuth.get(`${server}/users`, {
      params: {
        search: dataUsers.value.search,
      },
    });
    dataUsers.value.users = response.data;

  } catch (error: AxiosError | any) {
    authErrorHandler(error);
  }
}
</script>

<template>
  <HeaderDiv 
    :page-header="'Список пользователей'" 
    :cls="'text-secondary py-5'"
  />
  <div class="row mb-3">
    <input
      @input.prevent="searchUsers"
      class="form-control mb-3"
      name="search"
      id="search"
      type="text"
      placeholder="Поиск по имени пользователя"
      v-model="dataUsers.search"
    />
  </div>
  <div class="d-flex justify-content-between mb-3">
    <SwitchBox
      :name="'viewDeleted'"
      :label="'Показать удаленные'"
      v-model="dataUsers.viewDeleted"
    />
  </div>
  <UserForm
    v-show="dataUsers.action"
    :action="dataUsers.action"
    @update="
      dataUsers.action = '';
      getUsers();
    "
    @cancel="dataUsers.action = ''"
  />
  <TableSlots 
    v-show="dataUsers.action === ''"
    :tbl-class="'table align-middle'">
    <template v-slot:caption>
      <button
        class="btn btn-link text-secondary"
        type="button"
        @click="
          dataUsers.action === ''
            ? (dataUsers.action = 'create')
            : (dataUsers.action = '')
        "
      >
        Добавить пользователя
      </button>
    </template>
    <template v-slot:thead>
      <tr>
        <th width="5%">#</th>
        <th>Имя пользователя</th>
        <th width="15%">Логин</th>
        <th width="10%">Блокировка</th>
        <th width="15%">Создан</th>
        <th width="15%">Вход</th>
        <th width="15%">Регион</th>
      </tr>
    </template>
    <template v-slot:tbody>
      <tr>
        <td colspan="7">
          <TableSlots
            id="overflow"
            :tbl-class="'table table-hover align-middle no-bottom-border'"
          >
            <template v-slot:tbody>
              <tr height="50px" v-for="user in users" :key="user.id">
                <td width="5%">{{ user.id }}</td>
                <td>{{ user.fullname }}</td>
                <td width="15%">
                  <router-link :to="{ name: 'user', params: { id: user.id } }">
                    {{ user.username }}
                  </router-link>
                </td>
                <td width="10%">{{ user.blocked ? "Да" : "Нет" }}</td>
                <td width="15%">
                  {{ timeSince(user.pswd_create) }}
                </td>
                <td width="15%">
                  {{ timeSince(user.last_login) }}
                </td>
                <td width="15%">
                  {{ user.region }}
                </td>
              </tr>
            </template>
          </TableSlots>
        </td>
      </tr>
    </template>
  </TableSlots>
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
