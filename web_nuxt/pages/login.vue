<script setup lang="ts">
import { z } from "zod";

definePageMeta({ layout: false });

const schema = z.object({
  username: z.string(),
  password: z.string(),
  new_pswd: z
    .string()
    .regex(
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,16}$/,
      "Пароль от 8 до 16 цифр и латинских букв в нижнем и верхнем регистре"
    )
    .optional(),
  conf_pswd: z.string().optional(),
});

type Login = z.infer<typeof schema>;

const loginAction = ref("create");
const loginForm = ref({} as Login);

const alert = ref({
  color: "green",
  title: "Информация",
  description: "Введите логин и пароль",
});

const validate = (state: Login) => {
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
  return errors;
};

/**
 * Submit login form to server and get a new token.
 * @returns {Promise<void>}
 */
async function submitLogin(): Promise<void> {
  const { message, access_token } = (await $fetch(
    "/route/auth/login/" + loginAction.value,
    {
      method: "POST",
      body: loginForm.value,
    }
  )) as { message: string; access_token: string };
  if (message === "Success") {
    accessToken.value = access_token;
    await navigateTo("/persons");
  } else if (message === "Updated") {
    loginAction.value = "create";
    Object.assign(alert.value, {
      color: "blue",
      title: "Информация",
      description: "Войдите с новым паролем.",
    });
  } else if (message === "Denied") {
    loginAction.value = "update";
    Object.assign(alert.value, {
      color: "red",
      title: "Предупреждение",
      description: "Пароль просрочен.",
    });
  } else {
    Object.assign(alert.value, {
      color: "red",
      title: "Внимание",
      description: "Неправильный логин или пароль.",
    });
  }
}
</script>

<template>
  <div class="flex justify-center">
    <div class="py-8">
      <UAlert
        variant="subtle"
        :color="(alert.color as any)"
        :title="alert.title"
        :description="alert.description"
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
          :schema="schema"
          :state="loginForm"
          :validate="validate"
          class="mt-4"
          @submit.prevent="submitLogin"
        >
          <UFormGroup
            class="mb-3"
            size="md"
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
          </UFormGroup>
          <UFormGroup
            class="mb-3"
            size="md"
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
          </UFormGroup>
          <div v-if="loginAction === 'update'">
            <UFormGroup
              class="mb-3"
              size="md"
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
            </UFormGroup>
            <UFormGroup
              class="mb-3"
              size="md"
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
