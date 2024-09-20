<script setup lang="ts">
import { userToken } from "@/utils/auth";

interface Login {
  username: string;
  password: string;
  new_pswd: string;
  conf_pswd: string;
}

const loginAction = ref("create");
const loginForm = ref({} as Login);

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

const validate = (state: Login) => {
  const errors = [];
  const pattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*d).{8,16}$/;
  if (loginAction.value === "update") {
    if (state.password === state.new_pswd) {
      errors.push({
        path: "new_pswd",
        message: "Старый и новый пароли совпадают",
      });
    }
    if (!state.new_pswd.match(pattern)) {
      errors.push({
        path: "new_pswd",
        message:
          "Пароль должен быть от 8 до 16 цифр и букв в нижнем регистре латинской раскладки",
      });
    }
    if (state.conf_pswd !== state.new_pswd) {
      errors.push({
        path: "conf_pswd",
        message: "Новый пароль и подтверждение не совпадают",
      });
    }
  }
  return errors;
};

/**
 * Submit login form to server and get a new token.
 * @returns {Promise<void>}
 */
async function submitLogin(): Promise<void> {
  const { message, user_token } = (await $fetch(
    "/api/login/" + loginAction.value,
    {
      method: "POST",
      body: loginForm.value,
    }
  )) as { message: string; user_token: string };
  if (message === "Success") {
    userToken.value = user_token;
    navigateTo("/persons");
  } else if (message === "Updated") {
    loginAction.value = "create";
    alertMessage.setAlert("blue", "Информация", "Войдите с новым паролем.");
  } else if (message === "Denied") {
    loginAction.value = "update";
    alertMessage.setAlert("red", "Предупреждение", "Пароль просрочен.");
  } else {
    alertMessage.setAlert("red", "Внимание", "Неправильный логин или пароль.");
  }
}
</script>

<template>
  <div class="flex justify-center">
    <div class="py-8">
      <UAlert
        variant="subtle"
        :color="(alertMessage.alert.value.color as any)"
        :title="alertMessage.alert.value.title"
        :description="alertMessage.alert.value.description"
      />
      <ElementsHeaderDiv
        :div="'py-5'"
        :cls="'text-2xl text-blue-800'"
        :header="'Кадровая безопасность'"
      />
      <div class="border border-red-600 rounded-md p-5">
        <ElementsHeaderDiv
          :div="'mb-1'"
          :cls="'text-xl text-red-800'"
          :header="
            loginAction === 'create' ? 'Вход в систему' : 'Обновление пароля'
          "
        />
        <UForm
          :state="loginForm"
          :validate="validate"
          class="mt-4"
          @submit.prevent="submitLogin"
        >
          <UFormGroup class="mb-3" size="md" label="Логин">
            <UInput
              v-model="loginForm['username']"
              placeholder="username"
              icon="i-heroicons-user"
              required
            />
          </UFormGroup>
          <UFormGroup class="mb-3" size="md" label="Пароль">
            <UInput
              v-model="loginForm['password']"
              type="password"
              placeholder="password"
              icon="i-heroicons-lock-closed"
              required
            />
          </UFormGroup>
          <div v-if="loginAction === 'update'">
            <UFormGroup class="mb-3" size="md" label="Новый пароль">
              <UInput
                v-model="loginForm['new_pswd']"
                type="password"
                placeholder="password"
                icon="i-heroicons-lock-closed"
                required
              />
            </UFormGroup>
            <UFormGroup class="mb-3" size="md" label="Повтор пароля">
              <UInput
                v-model="loginForm['conf_pswd']"
                type="password"
                placeholder="password"
                icon="i-heroicons-lock-closed"
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
