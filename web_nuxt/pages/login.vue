<script setup lang="ts">
import type { Login } from "@/types";

definePageMeta({ layout: false });

const loginAction = ref("login");
const loginForm = ref({} as Login);

const alert = ref({
  color: "success",
  title: "Информация",
  description: "Введите логин и пароль",
  icon: "i-heroicons-information-circle",
});

const validate = (state: Partial<Login>) => {
  const errors = [];
  if (loginAction.value === "update") {
    if (state.password === state.new_pswd) {
      errors.push({
        path: "new_pswd",
        message: "Старый и новый пароли совпадают",
      });
    }
    if (state.conf_pswd !== state.new_pswd) {
      errors.push({
        path: "conf_pswd",
        message: "Новый пароль и подтверждение не совпадают",
      });
    }
  }
  if (
    state.new_pswd &&
    !state.new_pswd.match(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,16}$/)
  ) {
    errors.push({
      path: "new_pswd",
      message: "От 8 до 16 цифр и латинских букв в нижнем и верхнем регистре",
    });
  }
  return errors;
};

/**
 * Submit login form to server and get a new token.
 * @returns {Promise<void>}
 */
async function submitLogin(): Promise<void> {
  const { message, access_token } = (await $fetch(
    "/route/auth/" + loginAction.value,
    {
      method: "POST",
      body: loginForm.value,
    }
  )) as { message: string; access_token: string };
  if (message === "Success") {
    accessToken.value = access_token;
    await navigateTo("/persons");
  } else if (message === "Updated") {
    loginAction.value = "login";
    Object.assign(alert.value, {
      color: "success",
      title: "Информация",
      description: "Войдите с новым паролем.",
      icon: "i-heroicons-information-circle",
    });
  } else if (message === "Denied") {
    loginAction.value = "update";
    Object.assign(alert.value, {
      color: "warning",
      title: "Предупреждение",
      description: "Пароль просрочен.",
      icon: "i-heroicons-exclamation-circle",
    });
  } else {
    Object.assign(alert.value, {
      color: "error",
      title: "Внимание",
      description: "Неправильный логин или пароль.",
      icon: "i-heroicons-exclamation-triangle",
    });
  }
}
</script>

<template>
  <div class="flex flex-row justify-center">
    <div class="align-middle py-12">
      <UAlert
        variant="subtle"
        :color="(alert.color as any)"
        :title="alert.title"
        :description="alert.description"
        :icon="alert.icon"
      />
      <h3 class="text-2xl text-blue-800 font-bold my-6">
        Кадровая безопасность
      </h3>
      <UCard>
        <h3 class="text-xl text-red-800 font-bold mb-2">
          {{ loginAction === "login" ? "Вход в систему" : "Обновление пароля" }}
        </h3>
        <UForm
          :state="loginForm"
          :validate="validate"
          @submit.prevent="submitLogin"
        >
          <UFormField
            label="Логин"
            name="username"
            required
          >
            <UInput
              v-model="loginForm['username']"
              placeholder="username"
              icon="i-heroicons-user"
              required
            />
          </UFormField>
          <UFormField
            label="Пароль"
            name="password"
            required
          >
            <UInput
              v-model="loginForm['password']"
              type="password"
              placeholder="password"
              icon="i-heroicons-lock-closed"
              required
            />
          </UFormField>
          <div v-if="loginAction === 'update'">
            <UFormField
              label="Новый пароль"
              name="new_pswd"
              required
            >
              <UInput
                v-model="loginForm['new_pswd']"
                type="password"
                placeholder="password"
                icon="i-heroicons-lock-closed"
                required
              />
            </UFormField>
            <UFormField
              label="Повтор пароля"
              name="conf_pswd"
              required
            >
              <UInput
                v-model="loginForm['conf_pswd']"
                type="password"
                placeholder="password"
                icon="i-heroicons-lock-closed"
                required
              />
            </UFormField>
          </div>
          <UButtonGroup class="mt-2">
            <UButton
              :label="loginAction === 'login' ? 'Войти' : 'Изменить'"
              color="success"
              variant="outline"
              type="submit"
            />
            <UButton
              v-if="loginAction === 'login'"
              label="Изменить"
              color="secondary"
              variant="outline"
              @click="loginAction = 'update'"
            />
            <UButton
              v-if="loginAction === 'update'"
              label="Отмена"
              color="error"
              variant="outline"
              @click="
                loginAction = 'login';
                loginForm = {} as Login;
              "
            />
          </UButtonGroup>
        </UForm>
      </UCard>
    </div>
  </div>
</template>
