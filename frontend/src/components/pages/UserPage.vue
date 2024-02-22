<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { useRoute } from "vue-router";
import { authStore } from "@/store/token";
import { alertStore } from "@store/alert";
import { classifyStore } from "@/store/classify";
import { server } from "@utilities/utils";
import { router } from "@/router/router";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/layouts/HeaderDiv.vue")
);
const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
);
const UserForm = defineAsyncComponent(
  () => import("@components/forms/UserForm.vue")
);

const storeClassify = classifyStore();
const storeAlert = alertStore();
const storeAuth = authStore();

const route = useRoute();

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

onBeforeMount(async () => {
  userData.value.id = route.params.id.toString();
  userData.value.userAction("view");
});

const userData = ref({
  id: "",
  action: "",
  role: "",
  group: "",
  search: "",
  profile: <User>{},

  userAction: async function (action: String): Promise<void> {
    try {
      const response = await storeAuth.axiosInstance.get(
        `${server}/user/${this.id}`, {
          params: {
            action: action,
          }
        }
      );
      this.profile = response.data;
      if (action === "drop") {
        storeAlert.alertMessage.setAlert("alert-success", "Пароль сброшен");
      } else if (action === "block") {
        storeAlert.alertMessage.setAlert(
          "alert-success",
          `Пользователь ${
            this.profile.blocked ? "заблокирован" : "разблокирован"
          }`
        );
      } else if (action === "restore") {
        storeAlert.alertMessage.setAlert(
          "alert-success",
          "Пользователь восстановлен"
        )
      };
    } catch (error) {
      storeAlert.alertMessage.setAlert("alert-danger", error as string);
    }
  },

  userDelete: async function (): Promise<void> {
    if (confirm("Вы действительно хотите удалить пользователя?")) {
      try {
        const response = await storeAuth.axiosInstance.delete(
          `${server}/user/${this.id}`
        );
        this.profile = response.data;
        storeAlert.alertMessage.setAlert(
          "alert-success",
          "Пользователь удалён"
        );
        router.push({ name: "users" });
      } catch (error) {
        storeAlert.alertMessage.setAlert("alert-danger", error as string);
      }
    }
  },

  updateGroupRole: async function (
    action: string,
    item: string,
    value: string
  ): Promise<void> {
    if (value !== "") {
      try {
        const response =
          action === "add"
            ? await storeAuth.axiosInstance.get(
                `${server}/${item}/${value}/${this.id}`
              )
            : await storeAuth.axiosInstance.delete(
                `${server}/${item}/${value}/${this.id}`
              );
        this.profile = response.data;
        this.userAction("view");

        storeAlert.alertMessage.setAlert(
          "alert-success",
          `${item === "role" ? "Роль" : "Группа"} ${
            action === "add" ? "добавлена" : "удалена"
          }`
        );
      } catch (error) {
        storeAlert.alertMessage.setAlert("alert-danger", error as string);
      }
    }
  },

  deactivateAction: function (){
    this.action = ""
  }
});
</script>

<template>
  <div class="container py-3">
    <HeaderDiv
      :page-header="userData.profile.fullname"
      :cls="'text-secondary'"
    />
    <div class="py-3">
      <div>
        <RowDivSlot :label="'ID'" :value="userData.profile.id" />
        <RowDivSlot
          :label="'Имя пользователя'"
          :value="userData.profile.fullname"
        />
        <RowDivSlot
          :label="'Логин'"
          :value="userData.profile.username"
        />
        <RowDivSlot
          :label="'E-mail'"
          :value="userData.profile.email"
        />
        <RowDivSlot
          :label="'Создан'"
          :value="
            new Date(userData.profile.pswd_create).toLocaleString(
              'ru-RU'
            )
          "
        />
        <RowDivSlot
          :label="'Изменен'"
          :value="
            new Date(userData.profile.pswd_change).toLocaleString(
              'ru-RU'
            )
          "
        />
        <RowDivSlot
          :label="'Вход'"
          :value="
            new Date(userData.profile.last_login).toLocaleString(
              'ru-RU'
            )
          "
        />
        <RowDivSlot
          :label="'Попыток входа'"
          :value="userData.profile.attempt"
        />
        <RowDivSlot
          :label="'Блокировка'"
          :value="
            userData.profile.blocked
              ? 'Заблокирован'
              : 'Разблокирован'
          "
        />
        <RowDivSlot
          :label="'Активность'"
          :value="
            userData.profile.deleted
              ? 'Удален'
              : 'Активен'
          "
        />
        <RowDivSlot :label="'Группы'" :slotTwo="true">
          <template v-slot:divTwo>
            <ul
              v-for="(group, index) in userData.profile.groups"
              :key="index"
            >
              <li>
                {{ group["group"] }}
                <a
                  href="#"
                  @click="
                    userData.updateGroupRole(
                      'delete',
                      'group',
                      group['id']
                    )
                  "
                >
                  <i class="bi bi-dash-circle"></i>
                </a>
              </li>
            </ul>
            <form class="form form-check" role="form">
              <select
                class="form-select"
                id="group"
                name="group"
                style="width: 30%"
                v-model="userData.group"
                @change="
                  userData.updateGroupRole(
                    'add',
                    'group',
                    userData.group
                  )
                "
              >
                <option value="" selected>Добавить группу</option>
                <option
                  v-for="(group, index) in storeClassify.classData.groups"
                  :key="index"
                  :value="group['id']"
                >
                  {{ group["group"] }}
                </option>
              </select>
            </form>
          </template>
        </RowDivSlot>
        <RowDivSlot :label="'Роли'" :slotTwo="true">
          <template v-slot:divTwo>
            <ul
              v-for="(role, index) in userData.profile.roles"
              :key="index"
            >
              <li>
                {{ role["role"] }}
                <a
                  href="#"
                  @click="
                    userData.updateGroupRole(
                      'delete',
                      'role',
                      role['id']
                    )
                  "
                >
                  <i class="bi bi-dash-circle"></i>
                </a>
              </li>
            </ul>
            <form class="form form-check" role="form">
              <select
                class="form-select"
                id="role"
                name="role"
                style="width: 30%"
                v-model="userData.role"
                @change="
                  userData.updateGroupRole(
                    'add',
                    'role',
                    userData.role
                  )
                "
              >
                <option value="" selected>Добавить роль</option>
                <option
                  v-for="(role, index) in storeClassify.classData.roles"
                  :key="index"
                  :value="role['id']"
                >
                  {{ role["role"] }}
                </option>
              </select>
            </form>
          </template>
        </RowDivSlot>
      </div>
      <div class="btn-group py-3" role="group">
        <button
          class="btn btn-outline-secondary"
          type="button"
          data-bs-toggle="modal"
          data-bs-target="#modalUser"
          @click="userData.action = 'edit'"
        >
          Изменить пользователя
        </button>
        <button
          @click="userData.userAction('block')"
          class="btn btn-outline-secondary"
        >
          {{
            userData.profile.blocked
              ? "Разблокировать"
              : "Заблокировать"
          }}
        </button>
        <button
          @click="userData.userAction('drop')"
          type="button"
          class="btn btn-outline-secondary"
        >
          Сбросить пароль
        </button>
        <button
          @click="userData.userDelete"
          type="button"
          class="btn btn-outline-secondary"
        >
          Удалить
        </button>
        <button
          @click="userData.userAction('restore')"
          type="button"
          class="btn btn-outline-secondary"
          :disabled="!userData.profile.deleted"
        >
          Восстановить
        </button>
      </div>
    </div>
    <UserForm 
      :action="userData.action"
      :item="userData.profile"
      :userAction="userData.userAction"
      @deactivate="userData.deactivateAction"
    />
  </div>
</template>

<style scoped>
ul,
li {
  padding-left: 0;
}
</style>
@/utilities/token