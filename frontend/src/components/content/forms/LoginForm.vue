<script setup lang="ts">
import axios from "axios";
import { defineAsyncComponent, ref } from "vue";
import { alertStore } from "@store/alert";
import { authStore } from "@/store/auth";
import { server } from "@utilities/utils";
import { router } from "@/router/router";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/content/elements/HeaderDiv.vue")
)
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
)
const GroupInput = defineAsyncComponent(
  () => import("@components/content/elements/GroupInput.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);
const GroupContent = defineAsyncComponent(
  () => import("@components/content/elements/GroupContent.vue")
);

const storeAlert = alertStore();
const storeAuth = authStore();

const loginData = ref({
  action: "login",
  hidden: true,
  form: <Record<string, any>>{},
});

 async function submitLogin(): Promise<void> {
  loginData.value.hidden = true;
  if (loginData.value.action === "password") {
    if (loginData.value.form["password"] === loginData.value.form["new_pswd"]) {
      storeAlert.alertMessage.setAlert(
        "alert-warning",
        "Старый и новый пароли совпадают"
      );
      return;
    }
    if (loginData.value.form["conf_pswd"] !== loginData.value.form["new_pswd"]) {
      storeAlert.alertMessage.setAlert(
        "alert-warning",
        "Новый пароль и подтверждение не совпадают"
      );
      return;
    }
    delete loginData.value.form["conf_pswd"];
  }
  try {
    const response =
      loginData.value.action === "password"
        ? await axios.patch(`${server}/login`, loginData.value.form)
        : await axios.post(`${server}/login`, loginData.value.form);
    const { message, access_token, refresh_token } = response.data;

    switch (message) {
      case "Changed":
        loginData.value.action = "login";
        storeAlert.alertMessage.attr = "alert-success";
        storeAlert.alertMessage.text = "Войдите с новым паролем";
        break
        
      case "Authenticated":
        storeAuth.accessToken = access_token;
        localStorage.setItem("refresh_token", refresh_token);
        router.push({name: "auth"});
        break;

      case "Overdue":
        loginData.value.action = "password";
        storeAlert.alertMessage.setAlert(
          "alert-warning",
          "Пароль просрочен. Измените пароль"
        );
        break;

      case "Denied":
        loginData.value.action = "login";
        storeAlert.alertMessage.setAlert(
          "alert-danger",
          "Неверный логин или пароль"
        );
        break;
    }
  } catch (error) {
    storeAlert.alertMessage.setAlert("alert-warning", error as string);
  }
}
</script>

<template>
  <div class="border border-primary rounded p-5">
    <HeaderDiv 
      :cls="'text-primary mb-3 text-center'"
      :page-header="loginData.action === 'login'
      ? 'Вход в систему'
      : 'Изменить пароль'
      "
    />
    <div class="mb-3">
      <form
        class="form form-check"
        role="form"
        @submit.prevent="submitLogin"
      > 
        <LabelSlot :label="'Пользователь'">
          <GroupInput
            :name="'username'"
            :place="'Логин'"
            :min="3"
            :max="16"
            :pattern="'[a-zA-Z]+'"
            v-model="loginData.form['username']"
          />        
        </LabelSlot>
        <LabelSlot :label="'Пароль'">
          <GroupInput
            :name="'password'"
            :place="'Пароль'"
            :min="8"
            :max="16"
            :pattern="'[0-9a-zA-Z]+'"
            :type="loginData.hidden ? 'password' : 'text'"
            v-model="loginData.form['password']"
          >         
            <span class="input-group-text">
                <a
                  role="button"
                  @click="loginData.hidden = !loginData.hidden"
                >
                  <i :class="loginData.hidden ? 'bi bi-eye' : 'bi bi-eye-slash'"></i>
                </a>
            </span>
          </GroupInput>
        </LabelSlot>
        <div class="row mb-3 col-lg-9 offset-lg-3"
          v-show="loginData.action === 'login'">
          <a
            class="link-primary"
            href="#"
            @click="loginData.action = 'password'"
          >
            Изменить пароль
          </a>
        </div>
        <div v-if="loginData.action === 'password'">
          <LabelSlot :label="'Новый пароль'">
            <GroupInput 
              :name="'new_pswd'"
              :place="'Новый'"
              :min="8"
              :max="16"
              :pattern="'[0-9a-zA-Z]+'"
              :type="loginData.hidden ? 'password' : 'text'"
              v-model="loginData.form['new_pswd']"
            />
          </LabelSlot>
          <LabelSlot :label="'Повтор пароля'">
            <GroupInput
              :name="'conf_pswd'"
              :place="'Повтор'"
              :min="8"
              :max="16"
              :pattern="'[0-9a-zA-Z]+'"
              :type="loginData.hidden ? 'password' : 'text'"
              v-model="loginData.form['conf_pswd']"
            />
          </LabelSlot>
        </div>
        <BtnGroup>
          <GroupContent
            :submit-btn="loginData.action === 'login' ? 'Войти' : 'Изменить'"
            @cancel="loginData.action = 'login'"
          />
        </BtnGroup>
      </form>
    </div>
  </div>
</template>
