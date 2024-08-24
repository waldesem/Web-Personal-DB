<script setup lang="ts">
import { ref } from "vue";
import { server, stateUser, userToken } from "@/state/state";

const userState = stateUser();

const showPswd = ref(false);

const loginAction = ref("create");

const loginForm = ref({} as Record<string, unknown>);

const alertMessage = {
  alert: ref({
    color: "green",
    variant: "subtle",
    title: "Информация",
    description: "Введите логин и пароль",
  }),
  setAlert(color: string, title: string, description: string) {
    this.alert.value.color = color;
    this.alert.value.title = title;
    this.alert.value.description = description;
  },
};

/**
 * Submit login form to server and get a new token.
 * @returns {Promise<void>}
 */
async function submitLogin(): Promise<void> {
  if (loginAction.value === "update") {
    if (loginForm.value["passhash"] === loginForm.value["new_pswd"]) {
      alertMessage.setAlert(
        "purple",
        "Предупреждение",
        "Старый и новый пароли совпадают"
      );
      return;
    }
    if (loginForm.value["conf_pswd"] !== loginForm.value["new_pswd"]) {
      alertMessage.setAlert(
        "red",
        "Предупреждение",
        "Новый пароль и подтверждение не совпадают"
      );
      return;
    }
  }
  const { message, user_token } = (await $fetch(
    `${server}/login/${loginAction.value}`,
    {
      method: "POST",
      body: loginForm.value,
    }
  )) as { message: string; user_token: string };
  console.log(message);
  if (message === "Success") {
    userToken.value = user_token;
    userState.getCurrentUser();
  } else if (message === "Updated") {
    loginAction.value = "create";
    alertMessage.setAlert("blue", "Информация", "Войдите с новым паролем.");
  } else if (message === "Denied") {
    loginAction.value = "update";
    alertMessage.setAlert("red", "Предупреждение", "Пароль просрочен.");
  } else {
    alertMessage.setAlert(
      "red",
      "Внимание",
      "Неправильный логин или пароль."
    );
    }
  showPswd.value = false;
}
</script>

<template>
  <div class="flex justify-center">
    <div class="py-8">
      <UAlert
        variant="subtle"
        :color="alertMessage.alert.value.color"
        :title="alertMessage.alert.value.title"
        :description="alertMessage.alert.value.description"
      />
      <div class="py-5">
        <h3 class="text-2xl text-primary font-bold">Кадровая безопасность</h3>
      </div>
      <div class="border border-red-600 rounded-md p-5">
        <h3 class="text-xl text-opacity-75 text-red-800 font-bold">
          {{ loginAction === "create" ? "Вход в систему" : "Изменить пароль" }}
        </h3>
        <UForm :state="loginForm" class="mt-4" @submit.prevent="submitLogin">
          <UFormGroup class="mb-3" size="md" label="Логин">
            <UInput
              v-model="loginForm['username']"
              placeholder="username"
              icon="i-heroicons-user"
              required
            />
          </UFormGroup>
          <UFormGroup class="mb-3" size="md" label="Пароль">
            <UButtonGroup size="md" orientation="horizontal">
              <UInput
                v-model="loginForm['password']"
                :type="!showPswd ? 'password' : 'text'"
                placeholder="password"
                icon="i-heroicons-lock-closed"
                required
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
            <UFormGroup class="mb-3" size="md" label="Новый пароль">
              <UInput
                v-model="loginForm['new_pswd']"
                :type="!showPswd ? 'password' : 'text'"
                placeholder="password"
                required
              />
            </UFormGroup>
            <UFormGroup class="mb-3" size="md" label="Повтор пароля">
              <UInput
                v-model="loginForm['conf_pswd']"
                :type="!showPswd ? 'password' : 'text'"
                placeholder="password"
                required
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
  </div>
</template>
