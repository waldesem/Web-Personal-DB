<script setup lang="ts">
import { reactive, ref } from "vue";
import { server, stateAlert, stateUser } from "@/state/state";

const alertState = stateAlert();
const userState = stateUser();

const showPswd = ref(false);
const loginAction = ref("create");
const loginForm = reactive(<Record<string, unknown>>{});

async function submitLogin(): Promise<void> {
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
      case "Success": {
        const { user_token } = data as { user_token: string };
        localStorage.setItem("user_token", user_token);
        await userState.getCurrentUser();
        break;
      }

      case "Updated":
        loginAction.value = "create";
        alertState.setAlert("green", "Войдите с новым паролем");
        break;

      case "Denied":
        loginAction.value = "update";
        alertState.setAlert("purple", "Пароль просрочен");
        break;

      default:
        alertState.setAlert("red", "Неправильный логин или пароль");
        break;
    }
  } catch (error: unknown) {
    console.error(error);
    alertState.setAlert("red", "Неправильный логин или пароль");
  }
  showPswd.value = false;
}
</script>

<template>
  <UContainer class="flex justify-center py-5">
    <div>
      <DivsAlertMessage />
      <div class="py-5">
        <h3 class="text-2xl text-opacity-75 text-red-600 font-bold">
          StaffSec - кадровая безопасность
        </h3>
      </div>
      <div class="border border-red-600 rounded-md p-5">
        <h3 class="text-xl text-opacity-75 text-red-600 font-bold">
          {{ loginAction === "create" ? "Вход в систему" : "Изменить пароль" }}
        </h3>
        <UForm class="mt-4" @submit.prevent="submitLogin">
          <UFormGroup class="mb-3" size="md" label="Логин" required>
            <UInput
              placeholder="username"
              icon="i-bi-person"
              v-model="loginForm['username']"
            />
          </UFormGroup>
          <UFormGroup class="mb-3" size="md" label="Пароль" required>
            <UButtonGroup size="md" orientation="horizontal">
              <UInput
                :type="!showPswd ? 'password' : 'text'"
                placeholder="password"
                icon="i-bi-lock"
                v-model="loginForm['password']"
              />
              <UButton
                :title="!showPswd ? 'Показать' : 'Скрыть'"
                :icon="showPswd ? 'i-bi-eye-slash' : 'i-bi-eye'"
                color="gray"
                @click="showPswd = !showPswd"
              />
            </UButtonGroup>
          </UFormGroup>
          <div v-if="loginAction === 'update'">
            <UFormGroup class="mb-3" size="md" label="Новый пароль" required>
              <UInput
                :type="!showPswd ? 'password' : 'text'"
                placeholder="password"
                v-model="loginForm['new_pswd']"
              />
            </UFormGroup>
            <UFormGroup class="mb-3" size="md" label="Повтор пароля" required>
              <UInput
                :type="!showPswd ? 'password' : 'text'"
                placeholder="password"
                v-model="loginForm['conf_pswd']"
              />
            </UFormGroup>
          </div>
          <UButtonGroup class="mt-3" size="md" orientation="horizontal">
            <UButton
              label="Принять"
              color="green"
              variant="outline"
              type="submit"
            />
            <UButton
              v-show="loginAction === 'create'"
              label="Изменить"
              color="blue"
              variant="outline"
              @click="loginAction = 'update'"
            />
            <UButton
              label="Отмена"
              color="red"
              variant="outline"
              @click="loginAction = 'create'"
            />
          </UButtonGroup>
        </UForm>
      </div>
    </div>
  </UContainer>
</template>

<style scoped>
.container {
  justify-content: center;
  align-items: center;
  width: fit-content;
}
</style>
