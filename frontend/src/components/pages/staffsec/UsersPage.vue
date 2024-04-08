<script setup lang="ts">
import { computed, defineAsyncComponent, onBeforeMount, ref } from "vue";
import { authStore } from "@/store/auth";
import { alertStore } from "@store/alert";
import { server, debounce, timeSince } from "@utilities/utils";
import { User } from "@/interfaces/interface";

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

const storeAlert = alertStore();
const storeAuth = authStore();

const searchUsers = debounce(() => {
  getUsers();
}, 500);

onBeforeMount(() => {
  getUsers();
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
  <div class="container py-3">
    <div class="row mb-5">
      <HeaderDiv :page-header="'Список пользователей'" :cls="'text-secondary'" />
    </div>
    <div class="row mb-3">
      <input
        @input.prevent="searchUsers" 
        class="form-control"
        name="search"
        id="search"
        type="text"
        placeholder="Поиск по имени пользователя"
        v-model="dataUsers.search"
      />
    </div>
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
        <tr>
          <th width="10%">#</th>
          <th>Имя пользователя</th>
          <th width="20%">Логин</th>
          <th width="15%">Блокировка</th>
          <th width="15%">Создан</th>
          <th width="15%">Вход</th>
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
                  <td width="10%">{{ user.id }}</td>
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
                    {{ timeSince(user.pswd_create) }}
                  </td>
                  <td width="15%">
                    {{ timeSince(user.last_login) }}
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