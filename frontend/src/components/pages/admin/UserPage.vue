<script setup lang="ts">
import { computed, defineAsyncComponent, onBeforeMount, ref } from "vue";
import { useRoute } from "vue-router";
import { authStore } from "@/store/auth";
import { alertStore } from "@store/alert";
import { classifyStore } from "@/store/classify";
import { server } from "@utilities/utils";
import { User } from "@/interfaces/interface";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/layouts/HeaderDiv.vue")
);
const ModalWin = defineAsyncComponent(
  () => import("@components/layouts/ModalWin.vue")
);
const UserForm = defineAsyncComponent(
  () => import("@components/content/admin/forms/UserForm.vue")
);

const storeClassify = classifyStore();
const storeAlert = alertStore();
const storeAuth = authStore();

const route = useRoute();

onBeforeMount( async () => {
  userData.value.id = route.params.id.toString();
  await userData.value.userAction("view");
});

const userData = ref({
  id: "",
  action: "",
  role: "",
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
        console.log(response.status);
        storeAlert.alertMessage.setAlert(
          "alert-success",
          "Пользователь отмечен к удалению"
        );
        this.userAction("view");
      } catch (error) {
        storeAlert.alertMessage.setAlert("alert-danger", error as string);
      }
    }
  },

  updateRole: async function (
    action: string,
    value: string
  ): Promise<void> {
    if (value) {
      try {
        const response =
          action === "add"
            ? await storeAuth.axiosInstance.get(
                `${server}/role/${value}/${this.id}`
              )
            : await storeAuth.axiosInstance.delete(
                `${server}/role/${value}/${this.id}`
              );
        this.profile = response.data;
        this.userAction("view");

        storeAlert.alertMessage.setAlert(
          "alert-success", `Роль ${action === "add" ? "добавлена" : "удалена"}`
        );
      } catch (error) {
        storeAlert.alertMessage.setAlert("alert-danger", error as string);
      }
      this.role = '';
    }
  },
});

const profileObjec = computed(() => {
  return {
    id: ["ID", userData.value.profile.id],
    username: ["Имя пользователя", userData.value.profile.fullname],
    login: ["Логин", userData.value.profile.username],
    email: ["E-mail", userData.value.profile.email],
    created: ["Дата создания", new Date(userData.value.profile.pswd_create).toLocaleString('ru-RU')],
    updated: ["Дата изменения", new Date(userData.value.profile.pswd_change).toLocaleString('ru-RU')],
    lastLogin: ["Дата последнего входа", new Date(userData.value.profile.last_login).toLocaleString('ru-RU')],
    attempt: ["Попытки входа", userData.value.profile.attempt],
    blocked: ["Заблокирован", userData.value.profile.blocked ? 'Заблокирован' : 'Разблокирован'],
    activity: ["Активность", userData.value.profile.deleted ? 'Удален' : 'Активен'],
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
      <div v-for="value, key in profileObjec" :key="key" class="row mb-3">
        <div class="col-md-3">{{ value[0] }}</div>
        <div class="col-md-9">{{ value[1] }}</div>
      </div>
      <div class="row mb-3">
        <div class="col-md-3">Роли</div>
        <div class="col-md-9">
          <ul
            v-for="(role, index) in userData.profile.roles"
            :key="index"
          >
            <li>
              {{ role["role"] }}
              <a
                href="#"
                @click="
                  userData.updateRole(
                    'delete',
                    role['id']
                  )
                "
              >
                <i class="bi bi-dash-circle"></i>
              </a>
            </li>
          </ul>
          <form class="form form-check" role="form" id="role-form">
            <select
              class="form-select"
              name="role"
              style="width: 30%"
              v-model="userData.role"
              @change="
                userData.updateRole(
                  'add',
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
        </div>
      </div>
      <div class="py-3">
        <div class="btn-group" role="group">
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
            :disabled="userData.profile.deleted"
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
    </div>
    <ModalWin
      :title="'Изменить пользователя'"
      :id="'modalUser'"
      @cancel="userData.action = ''"
    >
      <UserForm 
        :action="userData.action"
        :item="userData.profile"
        @update="userData.action = ''; userData.userAction('view');"
      />
    </ModalWin>
  </div>
</template>

<style scoped>
#role-form {
  padding-left: 0;
}
</style>
