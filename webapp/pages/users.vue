<script setup lang="ts">
import { computed, onBeforeMount, ref } from "vue";
import { debounce } from "@/utils/utilities";
import { server, stateAlert, stateClassify } from "@/state/state";
import type { User } from "@/utils/interfaces";
import { useFetchAuth } from "@/utils/auth";

const classifyState = stateClassify();
const alertState = stateAlert();

onBeforeMount(async() => {
  await getUsers();
});

const users = computed(() => {
  return dataUsers.value.users.filter(
    (user: User) => user.deleted == dataUsers.value.viewDeleted
  );
});

const dataUsers = ref({
  search: "",
  users: <User[]>[],
  profile: <User>{},
  form: <User>{},
  viewDeleted: false,
});

async function getUsers() {
  try {
    const fetchAuth = useFetchAuth();
    const data = await fetchAuth(`${server}/users`, {
      params: {
        search: dataUsers.value.search,
      },
    });
    dataUsers.value.users = data as unknown as User[];
  } catch (error: any) {
    console.error(error);
  }
}

const searching = debounce(() => {
  getUsers();
}, 500);

async function userAction(item: String): Promise<void> {
  if (item === "delete") {
    if (
      !confirm("Вы действительно хотите удалить/восстановить пользователя?")
    ) {
      return;
    }
  }
  try {
    const fetchAuth = useFetchAuth();
    const response = await fetchAuth(
      `${server}/users/${dataUsers.value.profile.id}`,
      {
        params: {
          item: item,
        },
      }
    );
    console.log(response);
    getUsers();
  } catch (error: any) {
    alertState.setAlert("alert-warning", "Невозможно выполнить операцию");
    console.error(error);
  }
}

async function submitUser(): Promise<void> {
  try {
    const fetchAuth = useFetchAuth();
    const response = await fetchAuth(
      `${server}/users`,
      dataUsers.value.form
    );
    console.log(response);
    alertState.setAlert("alert-success", "Пользователь успешно создан");
    cancelOperations();
    getUsers();
  } catch (error) {
    alertState.setAlert("alert-warning", "Возможно, пользователь уже существует");
    console.error(error);
  }
}

function cancelOperations() {
  Object.keys(dataUsers.value.profile).forEach(
    (key) => delete dataUsers.value[key as keyof typeof dataUsers.value]
  );
}
</script>

<template>
  <LayoutsMenu>
    <ElementsHeaderDiv
      :page-header="'Список пользователей'"
      :cls="'text-secondary py-5'"
    />
    <div class="row mb-3">
      <input
        @input.prevent="searching"
        class="form-control mb-3"
        name="search"
        id="search"
        type="text"
        placeholder="Поиск по имени пользователя"
        v-model="dataUsers.search"
      />
    </div>
    <div class="d-flex justify-content-between">
      <ElementsSwitchBox
        :name="'viewDeleted'"
        :label="'Показать удаленные'"
        v-model="dataUsers.viewDeleted"
      />
      <div class="dropdown">
        <button
          class="btn btn-link text-secondary dropdown-toogle"
          type="button"
          data-bs-toggle="dropdown"
        >
          Добавить пользователя
        </button>
        <div class="dropdown-menu">
          <form @submit.prevent="submitUser" class="form form-check" role="form">
            <div class="p-3">
              <div class="mb-3">
                <ElementsInputElement
                  :name="'fullname'"
                  :place="'Имя пользователя'"
                  :need="true"
                  v-model="dataUsers.form['fullname']"
                />
              </div>
              <div class="mb-3">
                <ElementsInputElement
                  :name="'username'"
                  :place="'Учетная запись'"
                  :pattern="'[a-z_]+'"
                  :need="true"
                  v-model="dataUsers.form['username']"
                />
              </div>
              <ElementsBtnGroup :offset="false" />
            </div>
          </form>
        </div>
      </div>
    </div>
    <ElementsTableSlots :tbl-class="'table align-middle'">
      <template v-slot:thead>
        <tr>
          <th width="5%">#</th>
          <th>Имя пользователя</th>
          <th width="15%">Логин</th>
          <th width="10%">Блокировка</th>
          <th width="15%">Создан</th>
          <th width="15%">Роль</th>
          <th width="20%">Регион</th>
        </tr>
      </template>
      <template v-slot:tbody>
        <tr>
          <td colspan="7">
            <ElementsTableSlots
              id="overflow"
              :tbl-class="'table table-hover align-middle no-bottom-border'"
            >
              <template v-slot:tbody>
                <tr height="50px" v-for="user in users" :key="user.id">
                  <td width="5%">{{ user.id }}</td>
                  <td>{{ user.fullname }}</td>
                  <td width="15%">
                    <button
                      class="btn btn-link text-secondary"
                      type="button"
                      data-bs-toggle="modal"
                      data-bs-target="#user-modal"
                      @click="dataUsers.profile = user"
                    >
                      {{ user.username }}
                    </button>
                  </td>
                  <td width="10%">{{ user.blocked ? "Да" : "Нет" }}</td>
                  <td width="15%">
                    {{ new Date(user.pswd_create).toLocaleString() }}
                  </td>
                  <td width="15%">
                    {{ user.role }}
                  </td>
                  <td width="20%">{{ user.region }}</td>
                </tr>
              </template>
            </ElementsTableSlots>
          </td>
        </tr>
      </template>
    </ElementsTableSlots>
    <ElementsModalWin :elem-id="'user-modal'">
      <div class="p-3">
        <ElementsLabelSlot
          :label-class="'col-5'"
          :input-class="'col-7'"
          :label="'ID'"
        >
          {{ dataUsers.profile.id }}
        </ElementsLabelSlot>
        <ElementsLabelSlot 
          :label="'Регион'"
          :label-class="'col-5'"
          :input-class="'col-7'"
          >
          <ElementsSelectDiv
            :name="'region'"
            :select="classifyState.classes.value.regions"
            v-model="dataUsers.profile.region"
            @submit-data="userAction(dataUsers.profile.region)"
          />
        </ElementsLabelSlot>
        <ElementsLabelSlot 
          :label="'Роль'"
          :label-class="'col-5'"
          :input-class="'col-7'"
          >
          <ElementsSelectDiv
            :name="'role'"
            :select="classifyState.classes.value.roles"
            v-model="dataUsers.profile['role']"
            @submit-data="userAction(dataUsers.profile.role)"
          />
        </ElementsLabelSlot>
        <ElementsLabelSlot
          :label-class="'col-5'"
          :input-class="'col-7'"
          :label="'Имя пользователя'"
        >
          {{ dataUsers.profile.fullname }}
        </ElementsLabelSlot>
        <ElementsLabelSlot
          :label-class="'col-5'"
          :input-class="'col-7'"
          :label="'Логин'"
        >
          {{ dataUsers.profile.username }}
        </ElementsLabelSlot>
        <ElementsLabelSlot
          :label-class="'col-5'"
          :input-class="'col-7'"
          :label="'Дата создания пароля'"
        >
          {{
            new Date(dataUsers.profile.pswd_create + " UTC").toLocaleString(
              "ru-RU"
            )
          }}
        </ElementsLabelSlot>
        <ElementsLabelSlot
          :label-class="'col-5'"
          :input-class="'col-7'"
          :label="'Требует смены пароля'"
        >
          {{ dataUsers.profile.change_pswd ? "Да" : "Нет" }}
        </ElementsLabelSlot>
        <ElementsLabelSlot
          :label-class="'col-5'"
          :input-class="'col-7'"
          :label="'Попытки входа'"
        >
          {{ dataUsers.profile.attempt }}
        </ElementsLabelSlot>
        <ElementsLabelSlot
          :label-class="'col-5'"
          :input-class="'col-7'"
          :label="'Заблокирован'"
        >
          {{ dataUsers.profile.blocked ? "Заблокирован" : "Разблокирован" }}
        </ElementsLabelSlot>
        <ElementsLabelSlot
          :label-class="'col-5'"
          :input-class="'col-7'"
          :label="'Активность'"
        >
          {{ dataUsers.profile.deleted ? "Удален" : "Активен" }}
        </ElementsLabelSlot>
        <ElementsLabelSlot
          :label-class="'col-5'"
          :input-class="'col-7'"
          :label="'Роль'"
        >
          {{ dataUsers.profile.role }}
        </ElementsLabelSlot>
        <ElementsLabelSlot
          :label-class="'col-5'"
          :input-class="'col-7'"
          :label="'Дата создания профиля'"
        >
          {{
            new Date(dataUsers.profile.created + " UTC").toLocaleString(
              "ru-RU"
            )
          }}
        </ElementsLabelSlot>
      </div>
      <div class="btn-group p-3" role="group">
        <button
          @click="userAction('drop')"
          type="button"
          class="btn btn-outline-secondary"
        >
          Сбросить пароль
        </button>
        <button
          @click="userAction('delete')"
          type="button"
          class="btn btn-outline-danger"
        >
          {{ dataUsers.profile.deleted ? "Восстановить" : "Отметить к удалению" }}
        </button>
        <button
          type="button"
          class="btn btn-outline-primary"
          data-bs-dismiss="modal"
        >
          Закрыть
        </button>
      </div>
    </ElementsModalWin>
  </LayoutsMenu>
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
