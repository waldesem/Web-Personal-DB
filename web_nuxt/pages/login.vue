<script setup lang="ts">
import type { AlertProps, AuthFormField } from "@nuxt/ui";
import type { Login } from "@/types";

definePageMeta({ layout: false });

const alerts = {
  login: {
    color: "success",
    title: "Информация",
    description: "Введите логин и пароль",
    icon: "i-lucide-circle-alert",
  },
  refresh: {
    color: "info",
    title: "Информация",
    description: "Введите новый пароль и подтверждение",
    icon: "i-lucide-circle-alert",
  },
  denied: {
    color: "warning",
    title: "Предупреждение",
    description: "Пароль просрочен.",
    icon: "i-lucide-circle-alert",
  },
  updated: {
    color: "success",
    title: "Информация",
    description: "Войдите с новым паролем.",
    icon: "i-lucide-circle-alert",
  },
  error: {
    color: "error",
    title: "Внимание",
    description: "Неправильный логин или пароль.",
    icon: "i-lucide-triangle-alert",
  },
};

// Объявляем переменные для формы и состояния
const action = ref("login");
const loginForm = ref({} as Login);

// Объявляем переменную для показа алерта
const alert = ref(alerts.login);

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
    icon: "i-lucide-lock-keyhole",
    type: "password",
    required: true,
  },
  {
    name: "conf_pswd",
    label: "Подтверждение пароля",
    placeholder: "Подтверждение пароля",
    icon: "i-lucide-lock-keyhole",
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
  }
  return errors;
};

// Объявляем функцию для отправки формы
async function submitLogin() {
  const { message, access_token, refresh_token } = (await $fetch(
    "/routes/auth/" + action.value,
    {
      method: "POST",
      body: loginForm.value,
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
    token.value = access_token.split(" ")[1];
    refresh.value = refresh_token.split(" ")[1];
    return navigateTo("/persons");
  } else if (message === "updated") {
    action.value = "login";
    Object.assign(alert.value, alerts.updated);
  } else if (message === "denied") {
    action.value = "update";
    Object.assign(alert.value, alerts.denied);
  } else {
    Object.assign(alert.value, alerts.error);
  }
}
</script>

<template>
  <UPage>
    <div class="flex flex-col items-center justify-center gap-4 p-4">
      <UPageCard class="w-full max-w-md">
        <UAuthForm
          title="Вход в систему"
          description="Доступ в систему кадровой безопасности."
          icon="i-lucide-user"
          :validate="validate"
          :fields="action == 'login' ? login : update"
          :submit="{
            label: action === 'login' ? 'Войти' : 'Изменить',
            color: 'success',
            variant: 'outline',
          }"
          @submit="submitLogin()"
        >
          <template #title>
            <ElementsLogoDiv />
          </template>
          <template #validation>
            <UAlert
              variant="subtle"
              :color="(alert.color as AlertProps['color'])"
              :title="alert.title"
              :description="alert.description"
              :icon="alert.icon"
            />
          </template>
          <template #footer>
            <UButton
              :label="action == 'login' ? 'Изменить' : 'Отмена'"
              color="secondary"
              variant="outline"
              block
              @click="
                action == 'login' ? (action = 'update') : (action = 'login')
              "
            />
          </template>
        </UAuthForm>
      </UPageCard>
    </div>
  </UPage>
</template>
