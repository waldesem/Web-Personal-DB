<script setup lang="ts">
import axios from "axios";
import { defineAsyncComponent, ref } from "vue";
import { stateAlert } from "@/state";
import { server } from "@/utilities";
import { router } from "@/router";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/content/elements/HeaderDiv.vue")
);
const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);
const GroupContent = defineAsyncComponent(
  () => import("@components/content/elements/GroupContent.vue")
);

const loginData = ref({
  action: "create",
  hidden: true,
  form: <Record<string, any>>{},
});

async function submitLogin(): Promise<void> {
  loginData.value.hidden = true;
  if (loginData.value.action === "update") {
    if (loginData.value.form["password"] === loginData.value.form["new_pswd"]) {
      stateAlert.setAlert("alert-warning", "Старый и новый пароли совпадают");
      return;
    }
    if (
      loginData.value.form["conf_pswd"] !== loginData.value.form["new_pswd"]
    ) {
      stateAlert.setAlert(
        "alert-warning",
        "Новый пароль и подтверждение не совпадают"
      );
      return;
    }
  }

  try {
    const response = await axios.post(
      `${server}/login/${loginData.value.action}`,
      loginData.value.form
    );
    switch (response.status) {
      case 201:
        loginData.value.action = "create";
        stateAlert.setAlert("alert-success", "Войдите с новым паролем");
        break;

      case 200:
        const { user_token } = response.data;
        localStorage.setItem("user_token", user_token);
        router.push({ name: "persons" });
        break;

      case 205:
        loginData.value.action = "update";
        stateAlert.setAlert(
          "alert-warning",
          "Пароль просрочен. Измените пароль"
        );
        break;

      case 204:
        loginData.value.action = "create";
        stateAlert.setAlert("alert-danger", "Неверный логин или пароль");
        break;
    }
  } catch (error) {
    stateAlert.setAlert("alert-warning", error as string);
  }
}
</script>

<template>
  <div class="border border-primary rounded p-5">
    <HeaderDiv
      :cls="'text-primary mb-3 text-center'"
      :page-header="
        loginData.action === 'create' ? 'Вход в систему' : 'Изменить пароль'
      "
    />
      <form class="form form-check" role="form" @submit.prevent="submitLogin">
        <div class="mb-3">
          <InputElement
            :need="true"
            :name="'username'"
            :place="'Логин'"
            v-model="loginData.form['username']"
          />
        </div>
        <div class="mb-3">
          <InputElement
            :need="true"
            :name="'password'"
            :place="'Пароль'"
            :typeof="loginData.hidden ? 'password' : 'text'"
            v-model="loginData.form['password']"
          />
        </div>
        <div v-if="loginData.action === 'update'">
          <div class="mb-3">
            <InputElement
              :need="true"
              :name="'new_pswd'"
              :place="'Новый'"
              :min="8"
              :max="16"
              :typeof="loginData.hidden ? 'password' : 'text'"
              v-model="loginData.form['new_pswd']"
            />
          </div>
          <div class="mb-3">
            <InputElement
              :need="true"
              :name="'conf_pswd'"
              :place="'Повтор'"
              :typeof="loginData.hidden ? 'password' : 'text'"
              v-model="loginData.form['conf_pswd']"
            />
          </div>
        </div>
        <div class="row mb-3 col-lg-9">
          <a 
            v-show="loginData.action === 'create'" 
            class="link-primary mb-2" 
            href="#" 
            @click="loginData.action = 'update'"
            >
            Изменить пароль
          </a>
          <a 
            class="link-primary" 
            href="#" 
            @click="loginData.hidden = !loginData.hidden"
          >
            {{ loginData.hidden ? "Показать" : "Скрыть" }} пароль
          </a>
        </div>
        <BtnGroup :offset="false">
          <GroupContent
            :submit-btn="loginData.action === 'create' ? 'Войти' : 'Изменить'"
            @cancel="loginData.action = 'create'"
          />
        </BtnGroup>
      </form>
  </div>
</template>
