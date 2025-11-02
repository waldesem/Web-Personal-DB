<script setup lang="ts">
import type { AlertProps, AuthFormField, FormSubmitEvent } from "@nuxt/ui";
import { refManualReset } from '@vueuse/core'
import type { Login } from "@/types";

definePageMeta({ layout: false });

// Объявляем переменные для формы и состояния
const action = refManualReset("login");

// Объявляем переменную для показа алерта
const alert = ref({
  color: "success",
  title: "Информация",
  description: "Введите логин и пароль",
}) as Ref<AlertProps>;

const login: AuthFormField[] = [
  {
    name: "username",
    label: "Имя пользователя",
    placeholder: "Имя пользователя",
    icon: "i-lucide-user",
    type: "text",
    required: true,
  },
  {
    name: "password",
    label: "Пароль",
    placeholder: "Пароль",
    icon: "i-lucide-lock-keyhole",
    type: "password",
    required: true,
  },
];

const update = login.concat([
  {
    name: "new_pswd",
    label: "Новый пароль",
    placeholder: "Новый пароль",
    icon: "i-lucide-lock",
    type: "password",
    required: true,
  },
  {
    name: "conf_pswd",
    label: "Подтверждение пароля",
    placeholder: "Подтверждение пароля",
    icon: "i-lucide-lock",
    type: "password",
    required: true,
  },
]);

// Объявляем функцию для валидации формы
const validate = (state: Partial<Login>) => {
  const errors = [];
  if (action.value === "update") {
    if (
      state.new_pswd &&
      !state.new_pswd.match(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,16}$/)
    ) {
      errors.push({
        name: "new_pswd",
        message: "От 8 до 16 цифр и латинских букв в нижнем и верхнем регистре",
      });
    }
    if (state.password === state.new_pswd) {
      errors.push({
        name: "new_pswd",
        message: "Старый и новый пароли совпадают",
      });
    }
    if (state.conf_pswd !== state.new_pswd) {
      errors.push({
        name: "conf_pswd",
        message: "Новый пароль и подтверждение не совпадают",
      });
    }
  } else {
    if (!state.username) {
      errors.push({
        name: "username",
        message: "Введите имя пользователя",
      });
    } else if (state.username.length > 255) {
      errors.push({
        name: "username",
        message: "Слишком длинное имя",
      });
    }
    if (!state.password) {
      errors.push({
        name: "password",
        message: "Введите пароль",
      });
    } else if (state.password.length > 255) {
      errors.push({
        name: "password",
        message: "Слишком длинный пароль",
      });
    }
  }
  return errors;
};

// Объявляем функцию для отправки формы
async function onSubmit(payload: FormSubmitEvent<Partial<Login>>) {
  try {
    const { message, access_token, refresh_token } = (await $fetch(
      "/routes/auth/" + action.value,
      {
        method: "POST",
        body: payload.data,
      }
    )) as { message: string; access_token: string; refresh_token: string };
    if (message === "success") {
      const token = useCookie("token", {
        maxAge: 60 * 59,
        sameSite: "strict",
        watch: "shallow",
      });
      const refresh = useCookie("refresh", {
        maxAge: 60 * 60 * 24 * 30,
        sameSite: "strict",
        watch: "shallow",
      });
      token.value = access_token;
      refresh.value = refresh_token;
      return navigateTo("/persons");
    } else if (message === "updated") {
      action.reset();
      alert.value.color = "success";
      alert.value.title = "Информация";
      alert.value.description = "Войдите с новым паролем.";
    } else if (message === "denied") {
      alert.value.color = "warning";
      alert.value.title = "Предупреждение";
      alert.value.description = "Пароль просрочен.";
      action.value = "update";
    } else {
      alert.value.color = "error";
      alert.value.title = "Внимание";
      alert.value.description = "Неправильный логин или пароль.";
    }
  } catch (error) {
    console.error(error);
    alert.value.color = "error";
    alert.value.title = "Внимание";
    alert.value.description = "Ошибка соединения с сервером.";
  }
}
</script>

<template>
  <UMain class="my-[20vh]">
    <UPageCard class="w-full max-w-md m-auto">
      <UAuthForm
        title="Вход в систему"
        description="Доступ в систему кадровой безопасности."
        icon="i-lucide-user-lock"
        :validate="validate"
        :fields="action == 'login' ? login : update"
        :submit="{
          label: action === 'login' ? 'Войти' : 'Изменить',
          color: 'success',
          variant: 'outline',
        }"
        @submit.prevent="onSubmit($event)"
      >
        <template #title>
          <ElementsLogoDiv class="my-2" />
        </template>
        <template #validation>
          <UAlert
            variant="subtle"
            :color="alert.color"
            :title="alert.title"
            :description="alert.description"
            icon="i-lucide-circle-alert"
          />
        </template>
        <template #footer>
          <UButton
            :label="action == 'login' ? 'Изменить' : 'Отмена'"
            color="secondary"
            variant="outline"
            block
            @click="
              () => {
                if (action == 'login') {
                  action = 'update';
                  alert.color = 'info';
                  alert.title = 'Информация';
                  alert.description = 'Введите новый пароль и подтверждение.';
                } else {
                  action = 'login';
                  alert.color = 'success';
                  alert.title = 'Информация';
                  alert.description = 'Введите логин и пароль';
                }
              }
            "
          />
        </template>
      </UAuthForm>
    </UPageCard>
  </UMain>
</template>
