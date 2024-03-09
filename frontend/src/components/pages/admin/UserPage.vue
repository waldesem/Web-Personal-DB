<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { useRoute } from "vue-router";
import { authStore } from "@/store/auth";
import { alertStore } from "@store/alert";
import { classifyStore } from "@/store/classify";
import { server } from "@utilities/utils";
import { User } from "@/interfaces/interface";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/layouts/HeaderDiv.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/elements/LabelSlot.vue")
);
const LabelValue = defineAsyncComponent(
  () => import("@components/elements/LabelValue.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/elements/BtnGroup.vue")
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

async function updateData() {
  userData.value.action = "";
  await userData.value.userAction("view");
};
</script>

<template>
  <div class="container py-3">
    <HeaderDiv
      :page-header="userData.profile.fullname"
      :cls="'text-secondary'"
    />
    <div class="py-3">
      <div>
        <LabelValue :label="'ID'" :value="userData.profile.id" />
        <LabelValue
          :label="'Имя пользователя'"
          :value="userData.profile.fullname"
        />
        <LabelValue
          :label="'Логин'"
          :value="userData.profile.username"
        />
        <LabelValue
          :label="'E-mail'"
          :value="userData.profile.email"
        />
        <LabelValue
          :label="'Создан'"
          :value="
            new Date(userData.profile.pswd_create).toLocaleString(
              'ru-RU'
            )
          "
        />
        <LabelValue
          :label="'Изменен'"
          :value="
            new Date(userData.profile.pswd_change).toLocaleString(
              'ru-RU'
            )
          "
        />
        <LabelValue
          :label="'Вход'"
          :value="
            new Date(userData.profile.last_login).toLocaleString(
              'ru-RU'
            )
          "
        />
        <LabelValue
          :label="'Попыток входа'"
          :value="userData.profile.attempt"
        />
        <LabelValue
          :label="'Блокировка'"
          :value="
            userData.profile.blocked
              ? 'Заблокирован'
              : 'Разблокирован'
          "
        />
        <LabelValue
          :label="'Активность'"
          :value="
            userData.profile.deleted
              ? 'Удален'
              : 'Активен'
          "
        />
        <LabelSlot :label="'Роли'">
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
          <form class="form form-check" role="form">
            <select
              class="form-select"
              id="role"
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
        </LabelSlot>
      </div>
      <div class="py-3">
        <BtnGroup :cls="false">
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
        </BtnGroup>
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
        @update="updateData"
      />
    </ModalWin>
  </div>
</template>

<style scoped>
ul,
li {
  padding-left: 0;
}
</style>
