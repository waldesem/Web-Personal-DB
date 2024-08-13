<script setup lang="ts">
import { reactive, ref } from "vue";
import { server, stateAlert, stateUser, userToken } from "@/state/state";

const alertState = stateAlert();
const userState = stateUser();

const showPswd = ref(false);
const loginAction = ref("create");
const loginForm = reactive({} as Record<string, unknown>);

async function submitLogin(): Promise<void> {
  if (loginAction.value === "update") {
    if (loginForm["passhash"] === loginForm["new_pswd"]) {
      alertState.setAlert("purple", "Предупреждение", "Старый и новый пароли совпадают");
      return;
    }
    if (loginForm["conf_pswd"] !== loginForm["new_pswd"]) {
      alertState.setAlert(
        "purple",
        "Предупреждение",
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
        userToken.value = user_token;
        userState.getCurrentUser();
        break;
      }

      case "Updated":
        loginAction.value = "create";
        alertState.setAlert("green", "Продолжение", "Войдите с новым паролем");
        break;

      case "Denied":
        loginAction.value = "update";
        alertState.setAlert("purple", "Предупреждение", "Пароль просрочен");
        break;

      default:
        alertState.setAlert("rose", "Внимание", "Неправильный логин или пароль");
        break;
    }
  } catch (error: unknown) {
    console.error(error);
    alertState.setAlert("rose", "Внимание", "Неправильный логин или пароль");
  }
  showPswd.value = false;
}
</script>

<template>
  <UContainer class="flex justify-center py-5">
    <div>
      <ElementsAlertMessage />
      <div class="py-5">
        <h3 class="text-2xl text-primary font-bold">
          Кадровая безопасность
        </h3>
      </div>
      <div class="border border-red-600 rounded-md p-5">
        <h3 class="text-xl text-opacity-75 text-red-800 font-bold">
          {{ loginAction === "create" ? "Вход в систему" : "Изменить пароль" }}
        </h3>
        <UForm :state="loginForm" class="mt-4" @submit.prevent="submitLogin">
          <UFormGroup class="mb-3" size="md" label="Логин" required>
            <UInput
              v-model="loginForm['username']"
              placeholder="username"
              icon="i-heroicons-user"
            />
          </UFormGroup>
          <UFormGroup class="mb-3" size="md" label="Пароль" required>
            <UButtonGroup size="md" orientation="horizontal">
              <UInput
                v-model="loginForm['password']"
                :type="!showPswd ? 'password' : 'text'"
                placeholder="password"
                icon="i-heroicons-lock-closed"
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
                v-model="loginForm['new_pswd']"
                :type="!showPswd ? 'password' : 'text'"
                placeholder="password"
              />
            </UFormGroup>
            <UFormGroup class="mb-3" size="md" label="Повтор пароля" required>
              <UInput
                v-model="loginForm['conf_pswd']"
                :type="!showPswd ? 'password' : 'text'"
                placeholder="password"
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
