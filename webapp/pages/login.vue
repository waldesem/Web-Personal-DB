<script setup lang="ts">
import { reactive, ref } from "vue";
import { server, stateAlert, stateUser } from "@/state/state";

const alertState = stateAlert();
const userState = stateUser();

const showPswd = ref(false);
const loginAction = ref("create");
const loginForm = reactive(<Record<string, any>>{});

async function submitLogin(): Promise<void> {
  showPswd.value = false;
  if (loginAction.value === "update") {
    if (loginForm["passhash"] === loginForm["new_pswd"]) {
      alertState.setAlert("alert-warning", "Старый и новый пароли совпадают");
      return;
    }
    if (loginForm["conf_pswd"] !== loginForm["new_pswd"]) {
      alertState.setAlert(
        "alert-warning",
        "Новый пароль и подтверждение не совпадают"
      );
      return;
    }
  }
  try {
    const data = await $fetch(`${server}/login/${loginAction.value}`, {
      method: "POST",
      body: loginForm,
    });
    const { message } = data as { message: string };
    switch (message) {
      case "Success":
        const { user_token } = data as { user_token: string };
        localStorage.setItem("user_token", user_token);
        await userState.getCurrentUser();
        break;

      case "Updated":
        loginAction.value = "create";
        alertState.setAlert("alert-success", "Войдите с новым паролем");
        break;

      case "Denied":
        loginAction.value = "update";
        alertState.setAlert("alert-warning", "Пароль просрочен");
        break;

      default:
        alertState.setAlert("alert-warning", "Неправильный логин или пароль");
        break;
    }
  } catch (error) {
    alertState.setAlert("alert-warning", "Неправильный логин или пароль");
  }
}
</script>

<template>
  <div class="container pt-5">
    <DivsAlertMessage />
    <ElementsHeaderDiv
      :cls="'text-danger py-3'"
      :page-header="'StaffSec - кадровая безопасность'"
    />
    <div class="border border-primary rounded p-5">
      <ElementsHeaderDiv
        :cls="'text-primary mb-3 text-center'"
        :page-header="
          loginAction === 'create' ? 'Вход в систему' : 'Изменить пароль'
        "
      />
      <form class="form form-check" role="form" @submit.prevent="submitLogin">
        <div class="mb-3">
          <ElementsInputElement
            :need="true"
            :name="'username'"
            :place="'Логин'"
            v-model="loginForm['username']"
          />
        </div>
        <div class="input-group mb-3">
          <input
            :name="'password'"
            id="password"
            :type="!showPswd ? 'password' : 'text'"
            class="form-control"
            placeholder="Пароль"
            required
            v-model="loginForm['password']"
          />
          <button
            class="btn btn-outline-primary"
            type="button"
            :title="!showPswd ? 'Показать' : 'Скрыть'"
            @click="showPswd = !showPswd"
          >
            <i v-if="!showPswd" class="bi bi-eye"></i>
            <i v-else class="bi bi-eye-slash"></i>
          </button>
        </div>
        <div v-if="loginAction === 'update'">
          <div class="mb-3">
            <ElementsInputElement
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
            <ElementsInputElement
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
        </div>
        <ElementsBtnGroup
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
