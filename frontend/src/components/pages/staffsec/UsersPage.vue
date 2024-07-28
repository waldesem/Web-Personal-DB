<script setup lang="ts">
import { computed, defineAsyncComponent, onBeforeMount, ref } from "vue";
import { axiosAuth } from "@/auth";
import { debounce } from "@/utilities";
import { User } from "@/interfaces";
import { stateAlert, stateClassify, server } from "@/state";
import { AxiosError } from "axios";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/content/elements/HeaderDiv.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);
const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const SelectDiv = defineAsyncComponent(
  () => import("@components/content/elements/SelectDiv.vue")
);
const SwitchBox = defineAsyncComponent(
  () => import("@components/content/elements/SwitchBox.vue")
);
const TableSlots = defineAsyncComponent(
  () => import("@components/content/elements/TableSlots.vue")
);

onBeforeMount(() => {
  getUsers();
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
  viewDeleted: false,
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
    const response = await axiosAuth.get(
      `${server}/users/${dataUsers.value.profile.id}`,
      {
        params: {
          item: item,
        },
      }
    );
    console.log(response.status);
    getUsers();
  } catch (error: any) {
    console.error(error);
  }
}

async function submitUser(): Promise<void> {
  try {
    const response = await axiosAuth.post(
      `${server}/users`,
      dataUsers.value.profile
    );
    if (response.status === 205) {
      stateAlert.setAlert("alert-warning", "Пользователь уже существует");
    } else {
      stateAlert.setAlert("alert-success", "Запись успешно добавлена");
    }
    cancelOperations();
    getUsers();
  } catch (error) {
    console.error(error);
  }
}

function cancelOperations() {
  Object.keys(dataUsers.value.profile).forEach(
    (key) => delete dataUsers.value[key as keyof typeof dataUsers.value]
  );
  const collapse = document.getElementById("user-form");
  collapse?.setAttribute("class", "collapse card card-body mb-3");
}
</script>

<template>
  <HeaderDiv
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
  <div class="d-flex justify-content-between mb-3">
    <SwitchBox
      :name="'viewDeleted'"
      :label="'Показать удаленные'"
      v-model="dataUsers.viewDeleted"
    />
    <button
      class="btn btn-link text-secondary"
      type="button"
      data-bs-toggle="collapse"
      href="#user-form"
    >
      Добавить пользователя
    </button>
  </div>
  <div class="collapse card card-body" id="user-form">
    <form @submit.prevent="submitUser" class="form form-check" role="form">
      <div class="row">
        <div class="col-4">
          <InputElement
            :name="'fullname'"
            :place="'Имя пользователя'"
            :need="true"
            v-model="dataUsers.profile['fullname']"
          />
        </div>
        <div class="col-3">
          <InputElement
            :name="'username'"
            :place="'Учетная запись'"
            :pattern="'[a-z_]+'"
            :need="true"
            v-model="dataUsers.profile['username']"
          />
        </div>
        <div class="col-3">
          <SelectDiv
            :name="'region'"
            :place="'Регион'"
            :need="true"
            :select="stateClassify.classes.regions"
            v-model="dataUsers.profile['region']"
          />
        </div>
        <div class="col-1">
          <SwitchBox
            :name="'admin'"
            :title="'Администратор'"
            v-model="dataUsers.profile['has_admin']"
          />
        </div>
        <div class="col-1">
          <button
            class="btn btn-outline-secondary"
            name="submit"
            type="submit"
          >
            Сохранить
          </button>
        </div>
      </div>
    </form>
  </div>
  <TableSlots :tbl-class="'table align-middle'">
    <template v-slot:thead>
      <tr>
        <th width="5%">#</th>
        <th>Имя пользователя</th>
        <th width="15%">Логин</th>
        <th width="10%">Блокировка</th>
        <th width="15%">Создан</th>
        <th width="15%">Администратор</th>
        <th width="20%">Регион</th>
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
                  {{ user.has_admin ? "Да" : "Нет" }}
                </td>
                <td width="20%">{{ user.region }}</td>
              </tr>
            </template>
          </TableSlots>
        </td>
      </tr>
    </template>
  </TableSlots>
  <div class="modal modal fade" id="user-modal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-body">
          <div class="p-3">
            <LabelSlot
              :label-class="'col-5'"
              :input-class="'col-7'"
              :label="'ID'"
            >
              {{ dataUsers.profile.id }}
            </LabelSlot>
            <LabelSlot 
              :label="'Регион'"
              :label-class="'col-5'"
              :input-class="'col-7'"
              >
              <SelectDiv
                :name="'region'"
                :select="stateClassify.classes.regions"
                v-model="dataUsers.profile.region"
                @submit-data="userAction(dataUsers.profile.region)"
              />
            </LabelSlot>
            <LabelSlot
              :label-class="'col-5'"
              :input-class="'col-7'"
              :label="'Имя пользователя'"
            >
              {{ dataUsers.profile.fullname }}
            </LabelSlot>
            <LabelSlot
              :label-class="'col-5'"
              :input-class="'col-7'"
              :label="'Логин'"
            >
              {{ dataUsers.profile.username }}
            </LabelSlot>
            <LabelSlot
              :label-class="'col-5'"
              :input-class="'col-7'"
              :label="'Дата создания пароля'"
            >
              {{
                new Date(dataUsers.profile.pswd_create + " UTC").toLocaleString(
                  "ru-RU"
                )
              }}
            </LabelSlot>
            <LabelSlot
              :label-class="'col-5'"
              :input-class="'col-7'"
              :label="'Требует смены пароля'"
            >
              {{ dataUsers.profile.change_pswd ? "Да" : "Нет" }}
            </LabelSlot>
            <LabelSlot
              :label-class="'col-5'"
              :input-class="'col-7'"
              :label="'Попытки входа'"
            >
              {{ dataUsers.profile.attempt }}
            </LabelSlot>
            <LabelSlot
              :label-class="'col-5'"
              :input-class="'col-7'"
              :label="'Заблокирован'"
            >
              {{ dataUsers.profile.blocked ? "Заблокирован" : "Разблокирован" }}
            </LabelSlot>
            <LabelSlot
              :label-class="'col-5'"
              :input-class="'col-7'"
              :label="'Активность'"
            >
              {{ dataUsers.profile.deleted ? "Удален" : "Активен" }}
            </LabelSlot>
            <LabelSlot
              :label-class="'col-5'"
              :input-class="'col-7'"
              :label="'Администратор'"
            >
              {{ dataUsers.profile.has_admin ? "Да" : "Нет" }}
            </LabelSlot>
            <LabelSlot
              :label-class="'col-5'"
              :input-class="'col-7'"
              :label="'Дата создания профиля'"
            >
              {{
                new Date(dataUsers.profile.created + " UTC").toLocaleString(
                  "ru-RU"
                )
              }}
            </LabelSlot>
          </div>
          <div class="btn-group p-3" role="group">
            <button
              class="btn btn-outline-primary"
              type="button"
              @click="userAction('admin')"
            >
              {{
                dataUsers.profile.has_admin
                  ? "Отобрать админа"
                  : "Сделать админом"
              }}
            </button>
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
              {{ dataUsers.profile.deleted ? "Восстановить" : "Удалить" }}
            </button>
          </div>
        </div>
      </div>
    </div>
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
