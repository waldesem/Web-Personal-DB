<script setup lang="ts">
import axios from "axios";
import { defineAsyncComponent, reactive, ref } from "vue";
import { stateAlert, server } from "@/state";
import { router } from "@/router";

const HeaderDiv = defineAsyncComponent(
  () => import("@components/content/elements/HeaderDiv.vue")
);
const AlertMessage = defineAsyncComponent(
  () => import("@components/content/elements/AlertMessage.vue")
);
const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);

const showPswd = ref(false);
const loginAction = ref("create");
const loginForm = reactive(<Record<string, any>>{});

async function submitLogin(): Promise<void> {
  showPswd.value = false;
  if (loginAction.value === "update") {
    if (loginForm["passhash"] === loginForm["new_pswd"]) {
      stateAlert.setAlert("alert-warning", "Старый и новый пароли совпадают");
      return;
    }
    if (
      loginForm["conf_pswd"] !== loginForm["new_pswd"]
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
      `${server}/login/${loginAction.value}`, loginForm
    );
    switch (response.status) {
      case 201:
        loginAction.value = "create";
        stateAlert.setAlert("alert-success", "Войдите с новым паролем");
        break;

      case 200:
        const { user_token } = response.data;
        localStorage.setItem("user_token", user_token);
        router.push({ name: "persons" });
        break;

      case 205:
        loginAction.value = "update";
        stateAlert.setAlert(
          "alert-warning",
          "Пароль просрочен. Измените пароль"
        );
        break;
    }
  } catch (error) {
    stateAlert.setAlert("alert-warning", "Неправильный логин или пароль");
  }
}
</script>

<template>
  <div class="container pt-5">
    <AlertMessage/>
    <HeaderDiv 
      :cls="'text-danger py-3'"
      :page-header="'StaffSec - кадровая безопасность'"
    />
    <div class="border border-primary rounded p-5">
      <HeaderDiv
        :cls="'text-primary mb-3 text-center'"
        :page-header="
          loginAction === 'create' ? 'Вход в систему' : 'Изменить пароль'
        "
      />
        <form class="form form-check" role="form" @submit.prevent="submitLogin">
          <div class="mb-3">
            <InputElement
              :need="true"
              :name="'username'"
              :place="'Логин'"
              v-model="loginForm['username']"
            />
          </div>
          <div class="mb-3">
            <InputElement
              :need="true"
              :name="'password'"
              :place="'Пароль'"
              :typeof="!showPswd ? 'password' : 'text'"
              v-model="loginForm['password']"
            />
          </div>
          <div v-if="loginAction === 'update'">
            <div class="mb-3">
              <InputElement
                :need="true"
                :name="'new_pswd'"
                :place="'Новый пароль'"
                :min="8"
                :max="16"
                :typeof="!showPswd ? 'password' : 'text'"
                v-model="loginForm['new_pswd']"
              />
            </div>
            <div class="mb-3">
              <InputElement
                :need="true"
                :name="'conf_pswd'"
                :place="'Повтор пароля'"
                :typeof="!showPswd ? 'password' : 'text'"
                v-model="loginForm['conf_pswd']"
              />
            </div>
          </div>
          <div class="row mb-3 col-lg-9">
            <a 
              v-show="loginAction === 'create'" 
              class="link-primary mb-2" 
              href="#" 
              @click="loginAction = 'update'"
              >
              Изменить пароль
            </a>
            <a 
              class="link-primary" 
              href="#" 
              @click="showPswd = !showPswd"
            >
              {{ !showPswd ? "Показать" : "Скрыть" }} пароль
            </a>
          </div>
          <BtnGroup 
            :offset="false" 
            :submit-btn="loginAction === 'create' ? 'Войти' : 'Изменить'"
            @cancel="loginAction = 'create'"
            />
        </form>
    </div>
  </div>
</template>

<style scoped>
.container {
  justify-content: center;
  align-items: center;
  width: fit-content;
}
</style>
