<script setup lang="ts">
import type { AlertProps, AuthFormField, FormSubmitEvent } from "@nuxt/ui";
import type { Login } from "@/types";

definePageMeta({ layout: false });

onBeforeMount(() => clearNuxtData());

// Объявляем переменные для формы и состояния
const method = ref<"POST" | "PATCH">("POST");

// Объявляем переменную для показа алерта
const alert = ref({
  color: "success",
  title: "Информация",
  description: "Введите логин и пароль",
}) as Ref<AlertProps>;

function defineAlert(color: string, title: string, description: string) {
  alert.value = {
    color,
    title,
    description,
  };
}

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
    icon: "i-lucide-lock",
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
  if (method.value === "PATCH") {
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
    }
    if (!state.password) {
      errors.push({
        name: "password",
        message: "Введите пароль",
      });
    }
  }
  return errors;
};

// Объявляем функцию для отправки формы
async function onSubmit(payload: FormSubmitEvent<Partial<Login>>) {
  try {
    const resp = await $fetch.raw("/routes/auth/login", {
      method: method.value,
      body: payload.data,
    });
    if (resp.status === 200) {
      method.value = "POST";
      defineAlert(
        "success",
        "Информация",
        "Пароль успешно изменен. Войдите с новым паролем.",
      );
    } else if (resp.status === 201) {
      const { message, access_token, refresh_token } = await resp.json();
      if (message === "success") {
        const token = useCookie("access", {
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
      } else {
        defineAlert(
          "warning",
          "Предупреждение",
          "Пароль просрочен. Измените пароль.",
        );
        method.value = "PATCH";
      }
    } else {
      defineAlert(
        "error",
        "Ошибка",
        "Неправильный логин или пароль. Попробуйте еще раз.",
      );
    }
  } catch (error) {
    console.error(error);
    defineAlert("error", "Внимание", "Ошибка соединения с сервером.");
  }
}
</script>

<template>
  <UPageCard class="w-full max-w-md m-auto my-[20vh]">
    <UAuthForm
      description="Доступ в систему кадровой безопасности."
      icon="i-lucide-user-lock"
      :validate="validate"
      :fields="method == 'POST' ? login : update"
      :submit="{
        label: method === 'POST' ? 'Войти' : 'Изменить',
        color: 'success',
        variant: 'outline',
      }"
      :ui="{ leadingIcon: 'text-blue-800' }"
      @submit.prevent="onSubmit($event)"
    >
      <template #title>
        <ElementLogoDiv />
      </template>
      <template #validation>
        <UAlert
          variant="subtle"
          :color="alert.color"
          :title="alert.title"
          :description="alert.description"
        />
      </template>
      <template #footer>
        <UButton
          :label="method == 'POST' ? 'Изменить' : 'Отмена'"
          color="secondary"
          variant="outline"
          block
          @click="
            () => {
              if (method == 'POST') {
                method = 'PATCH';
                defineAlert(
                  'info',
                  'Информация',
                  'Введите новый пароль и подтверждение.',
                );
              } else {
                method = 'POST';
                defineAlert('success', 'Информация', 'Введите логин и пароль');
              }
            }
          "
        />
      </template>
    </UAuthForm>
  </UPageCard>
</template>
