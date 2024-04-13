<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { useRoute } from "vue-router";
import { authStore } from "@/store/auth";
import { alertStore } from "@store/alert";
import { classifyStore } from "@/store/classify";
import { server } from "@utilities/utils";
import { User } from "@/interfaces/interface";

const AlertMessage = defineAsyncComponent(
  () => import("@components/content/elements/AlertMessage.vue")
);
const HeaderDiv = defineAsyncComponent(
  () => import("@components/content/elements/HeaderDiv.vue")
);
const SelectObject = defineAsyncComponent(
  () => import("@components/content/elements/SelectObject.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);
const UserForm = defineAsyncComponent(
  () => import("@components/content/forms/UserForm.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);

const storeClassify = classifyStore();
const storeAlert = alertStore();
const storeAuth = authStore();

const route = useRoute();

onBeforeMount(async () => {
  userData.value.id = route.params.id.toString();
  await userAction("view");
});

const userData = ref({
  id: "",
  action: "",
  role: "",
  search: "",
  profile: <User>{},
});

async function userAction(action: String): Promise<void> {
  try {
    const response = await storeAuth.axiosInstance.get(
      `${server}/user/${userData.value.id}`,
      {
        params: {
          action: action,
        },
      }
    );
    userData.value.profile = response.data;
    if (action === "drop") {
      storeAlert.alertMessage.setAlert("alert-success", "Пароль сброшен");
    } else if (action === "block") {
      storeAlert.alertMessage.setAlert(
        "alert-success",
        `Пользователь ${
          userData.value.profile.blocked ? "заблокирован" : "разблокирован"
        }`
      );
    }
  } catch (error) {
    storeAlert.alertMessage.setAlert("alert-danger", error as string);
  }
}

async function userDelete(): Promise<void> {
  if (confirm("Вы действительно хотите удалить пользователя?")) {
    try {
      const response = await storeAuth.axiosInstance.delete(
        `${server}/user/${userData.value.id}`
      );
      console.log(response.status);
      storeAlert.alertMessage.setAlert(
        "alert-success",
        "Пользователь отмечен к удалению"
      );
      userAction("view");
    } catch (error) {
      storeAlert.alertMessage.setAlert("alert-danger", error as string);
    }
  }
}

async function updateRole(action: string, value: string): Promise<void> {
  if (value) {
    try {
      const response =
        action === "add"
          ? await storeAuth.axiosInstance.get(
              `${server}/role/${value}/${userData.value.id}`
            )
          : await storeAuth.axiosInstance.delete(
              `${server}/role/${value}/${userData.value.id}`
            );
      console.log(response.status);
      userAction("view");

      storeAlert.alertMessage.setAlert(
        "alert-success",
        `Роль ${action === "add" ? "добавлена" : "удалена"}`
      );
    } catch (error) {
      storeAlert.alertMessage.setAlert("alert-danger", error as string);
    }
    userData.value.role = "";
  }
}
</script>

<template>
  <!-- <div class="container py-3"> -->
    <AlertMessage/>
    <HeaderDiv
      :page-header="userData.profile.fullname"
      :cls="'text-secondary'"
    />
    <div class="py-3">
      <LabelSlot :label="'ID'">{{ userData.profile.id }}</LabelSlot>
      <LabelSlot :label="'Имя пользователя'">{{
        userData.profile.fullname
      }}</LabelSlot>
      <LabelSlot :label="'Логин'">{{ userData.profile.username }}</LabelSlot>
      <LabelSlot :label="'E-mail'">{{ userData.profile.email }}</LabelSlot>
      <LabelSlot :label="'Дата создания'">{{
        new Date(userData.profile.pswd_create).toLocaleString("ru-RU")
      }}</LabelSlot>
      <LabelSlot :label="'Дата изменения'">{{
        new Date(userData.profile.pswd_change).toLocaleString("ru-RU")
      }}</LabelSlot>
      <LabelSlot :label="'Дата последнего входа'">{{
        new Date(userData.profile.last_login).toLocaleString("ru-RU")
      }}</LabelSlot>
      <LabelSlot :label="'Попытки входа'">{{
        userData.profile.attempt
      }}</LabelSlot>
      <LabelSlot :label="'Заблокирован'">{{
        userData.profile.blocked ? "Заблокирован" : "Разблокирован"
      }}</LabelSlot>
      <LabelSlot :label="'Активность'">{{
        userData.profile.deleted ? "Удален" : "Активен"
      }}</LabelSlot>

      <div class="row mb-3">
        <div class="col-md-3">Роли</div>
        <div class="col-md-9">
          <ul v-for="(role, index) in userData.profile.roles" :key="index">
            <li>
              {{ role["role"] }}
              <a href="#" @click="updateRole('delete', role['id'])">
                <i class="bi bi-dash-circle"></i>
              </a>
            </li>
          </ul>
          <SelectObject
            :name="'role'"
            :select="storeClassify.classData.roles"
            v-model="userData.role"
            @submit-data="updateRole('add', userData.role)"
          />
        </div>
      </div>
      <UserForm
        v-if="userData.action"
        :action="userData.action"
        :item="userData.profile"
        @update="
          userData.action = '';
          userAction('view');
        "
      />
      <div class="py-3">
        <BtnGroup :offset="false">
          <button
            class="btn btn-outline-secondary"
            type="button"
            @click="
              userData.action === ''
                ? (userData.action = 'edit')
                : (userData.action = '')
            "
          >
            {{ userData.action === "" ? "Редактировать" : "Отменить" }}
          </button>
          <button
            @click="userAction('block')"
            class="btn btn-outline-secondary"
          >
            {{ userData.profile.blocked ? "Разблокировать" : "Заблокировать" }}
          </button>
          <button
            @click="userAction('drop')"
            type="button"
            class="btn btn-outline-secondary"
          >
            Сбросить пароль
          </button>
          <button
            @click="userDelete"
            type="button"
            class="btn btn-outline-secondary"
            :disabled="userData.profile.deleted"
          >
            Удалить
          </button>
        </BtnGroup>
      </div>
    </div>
  <!-- </div> -->
</template>

<style scoped>
#role {
  padding-left: 0;
}
</style>
