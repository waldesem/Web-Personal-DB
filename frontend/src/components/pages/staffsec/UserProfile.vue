<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { stateAlert, stateClassify } from "@/state";
import { axiosAuth } from "@/auth";
import { server } from "@/utilities";
import { router } from "@/router";
import { User } from "@/interfaces";

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

onBeforeMount(async () => {
  userData.value.id = router.currentRoute.value.params.id.toString();
  await userAction("view");
});

const userData = ref({
  id: "",
  action: "",
  role: "",
  profile: <User>{},
});

async function userAction(action: String): Promise<void> {
  try {
    const response = await axiosAuth.get(
      `${server}/user/${userData.value.id}`,
      {
        params: {
          action: action,
        },
      }
    );
    userData.value.profile = response.data;
    if (action === "drop") {
      stateAlert.setAlert("alert-success", "Пароль сброшен");
    } else if (action === "block") {
      stateAlert.setAlert(
        "alert-success",
        `Пользователь ${
          userData.value.profile.blocked ? "заблокирован" : "разблокирован"
        }`
      );
    }
  } catch (error) {
    stateAlert.setAlert("alert-danger", error as string);
  }
}

async function userDelete(): Promise<void> {
  if (confirm("Вы действительно хотите удалить пользователя?")) {
    try {
      const response = await axiosAuth.delete(
        `${server}/user/${userData.value.id}`
      );
      console.log(response.status);
      stateAlert.setAlert(
        "alert-success",
        "Пользователь отмечен к удалению"
      );
      userAction("view");
    } catch (error) {
      stateAlert.setAlert("alert-danger", error as string);
    }
  }
}

async function updateRole(action: string, value: string): Promise<void> {
  if (value) {
    try {
      const response =
        action === "add"
          ? await axiosAuth.get(
              `${server}/role/${value}/${userData.value.id}`
            )
          : await axiosAuth.delete(
              `${server}/role/${value}/${userData.value.id}`
            );
      console.log(response.status);
      userAction("view");

      stateAlert.setAlert(
        "alert-success",
        `Роль ${action === "add" ? "добавлена" : "удалена"}`
      );
    } catch (error) {
      stateAlert.setAlert("alert-danger", error as string);
    }
    userData.value.role = "";
  }
}
</script>

<template>
  <HeaderDiv
    :page-header="userData.profile.fullname"
    :cls="'text-secondary py-3'"
  />
  <div class="mb-3">
    <LabelSlot :label="'ID'">
      {{ userData.profile.id }}
    </LabelSlot>
    <LabelSlot :label="'Имя пользователя'">
      {{ userData.profile.fullname }}
    </LabelSlot>
    <LabelSlot :label="'Логин'">
      {{ userData.profile.username }}
    </LabelSlot>
    <LabelSlot :label="'E-mail'">
      {{ userData.profile.email }}
    </LabelSlot>
    <LabelSlot :label="'Дата создания'">
      {{ new Date(userData.profile.pswd_create).toLocaleString("ru-RU") }}
    </LabelSlot>
    <LabelSlot :label="'Дата изменения'">
      {{ new Date(userData.profile.pswd_change).toLocaleString("ru-RU") }}
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
    <LabelSlot :label="'Роли'">
      <ul v-for="(role, index) in userData.profile.roles" :key="index">
        <li>
          {{ role["role"] }}
          <button 
            type="button" 
            class="btn btn-link" 
            @click="updateRole('delete', role['id'])"
          >
            <i class="bi bi-dash-circle"></i>
          </button>
        </li>
      </ul>
      <SelectObject
        :name="'role'"
        :select="stateClassify.roles"
        v-model="userData.role"
        @submit-data="updateRole('add', userData.role)"
      />
    </LabelSlot>
    <UserForm
      v-if="userData.action"
      :action="userData.action"
      :item="userData.profile"
      @update="
        userData.action = '';
        userAction('view');
      "
    />
    <BtnGroup :offset="false">
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
        @click="userAction('block')"
        class="btn btn-outline-info"
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
        class="btn btn-outline-danger"
        :disabled="userData.profile.deleted"
      >
        Удалить
      </button>
    </BtnGroup>
  </div>
</template>

<style scoped>
#role {
  padding-left: 0;
}
</style>
