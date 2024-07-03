<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { stateAlert, stateUser, server } from "@/state";
import { axiosAuth } from "@/auth";
import { useRoute } from "vue-router";
import { User } from "@/interfaces";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/content/elements/HeaderDiv.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);
const UserForm = defineAsyncComponent(
  () => import("@components/content/forms/UserForm.vue")
);

onBeforeMount(async () => {
  const route = useRoute();
  userData.value.id = route.params.id as string;
  await userAction("view");
});

const userData = ref({
  id: "",
  action: "",
  profile: <User>{},
});

async function userAction(action: String): Promise<void> {
  try {
    const response = await axiosAuth.get(
      `${server}/users/${userData.value.id}`,
      {
        params: {
          action: action,
        },
      }
    );
    userData.value.profile = response.data;
    if (action === "drop") {
      stateAlert.setAlert("alert-success", "Пароль сброшен");
    }
  } catch (error: any) {
    console.error(error);
  }
}

async function userDelete(): Promise<void> {
  if (confirm("Вы действительно хотите удалить пользователя?")) {
    try {
      const response = await axiosAuth.delete(
        `${server}/users/${userData.value.id}`
      );
      const status =response.status;
      if(status === 204) {
        stateAlert.setAlert(
          "alert-success",
          "Пользователь отмечен к удалению"
        );
        userAction("view");
      } else {
        stateAlert.setAlert("alert-danger", "Произошла ошибка");
      }
    } catch (error: any) {
      console.error(error);
    }
  }
}
</script>

<template>
  <HeaderDiv
    :page-header="userData.profile.fullname"
    :cls="'text-secondary py-5'"
  />
  <UserForm
    v-if="userData.action"
    :action="userData.action"
    :item="userData.profile"
    @update="
      userData.action = '';
      userAction('view');
    "
    @cancel="userData.action = '';"
  />
  <div v-else>
    <div class="mb-5">
      <LabelSlot :label="'ID'">
        {{ userData.profile.id }}
      </LabelSlot>
      <LabelSlot :label="'Регион'">
        {{ userData.profile.region }}
      </LabelSlot>
      <LabelSlot :label="'Имя пользователя'">
        {{ userData.profile.fullname }}
      </LabelSlot>
      <LabelSlot :label="'Логин'">
        {{ userData.profile.username }}
      </LabelSlot>
      <LabelSlot :label="'Дата создания пароля'">
        {{ new Date(userData.profile.pswd_create + ' UTC').toLocaleString("ru-RU") }}
      </LabelSlot>
      <LabelSlot :label="'Требует смены пароля'">
        {{ userData.profile.change_pswd ? "Да" : "Нет" }}
      </LabelSlot>
      <LabelSlot :label="'Дата последнего входа'">
        {{ new Date(userData.profile.last_login).toLocaleString("ru-RU") }}
      </LabelSlot>
      <LabelSlot :label="'Попытки входа'">
        {{ userData.profile.attempt }}
      </LabelSlot>
      <LabelSlot :label="'Заблокирован'">
        {{ userData.profile.blocked ? "Заблокирован" : "Разблокирован" }}
      </LabelSlot>
      <LabelSlot :label="'Активность'">
        {{ userData.profile.deleted ? "Удален" : "Активен" }}
      </LabelSlot>
      <LabelSlot :label="'Администратор'">
        {{ userData.profile.has_admin ? "Да" : "Нет" }}
      </LabelSlot>
      <LabelSlot :label="'Дата создания профиля'">
        {{ new Date(userData.profile.created + ' UTC').toLocaleString("ru-RU")}}
      </LabelSlot>
    </div>
    <div class="btn-group" role="group">
      <button
        class="btn btn-outline-primary"
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
        @click="userAction('drop')"
        type="button"
        class="btn btn-outline-secondary"
      >
        Сбросить пароль
      </button>
      <button
        @click="userDelete"
        type="button"
        class="btn btn-outline-danger"
        :disabled="userData.profile.deleted || userData.id == stateUser.userId"
      >
        Удалить
      </button>
    </div>
  </div>
</template>

<style scoped>
#role {
  padding-left: 0;
}
</style>
