<script setup lang="ts">
import type { AlertProps } from "@nuxt/ui";

definePageMeta({ layout: false });

interface Login {
  username: string;
  password: string;
  new_pswd: string;
  conf_pswd: string;
}

const action = ref("login");
const loginForm = ref({} as Login);

const alert = ref({
  color: "success",
  title: "Информация",
  description: "Введите логин и пароль",
  icon: "i-lucide-circle-alert",
});

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

async function submitLogin() {
  const { message, access_token } = (await $fetch(
    "/route/auth/" + action.value,
    {
      method: "POST",
      body: loginForm.value,
    }
  )) as { message: string; access_token: string };
  if (message === "Success") {
    accessToken.value = access_token;
    return navigateTo("/persons");
  } else if (message === "Updated") {
    action.value = "login";
    Object.assign(alert.value, {
      color: "success",
      title: "Информация",
      description: "Войдите с новым паролем.",
      icon: "i-lucide-circle-alert",
    });
  } else if (message === "Denied") {
    action.value = "update";
    Object.assign(alert.value, {
      color: "warning",
      title: "Предупреждение",
      description: "Пароль просрочен.",
      icon: "i-lucide-circle-alert",
    });
  } else {
    Object.assign(alert.value, {
      color: "error",
      title: "Внимание",
      description: "Неправильный логин или пароль.",
      icon: "i-lucide-triangle-alert",
    });
  }
}
</script>

<template>
  <UContainer>
    <div class="flex flex-row justify-center">
      <div class="py-12">
        <UAlert
          variant="subtle"
          :color="(alert.color as AlertProps['color'])"
          :title="alert.title"
          :description="alert.description"
          :icon="alert.icon"
        />
        <h3 class="text-2xl text-blue-800 font-bold my-6">
          Кадровая безопасность
        </h3>
        <UCard>
          <h3 class="text-xl text-red-800 font-bold mb-2">Вход в систему</h3>
          <UForm
            :validate="validate"
            :state="loginForm"
            @submit.prevent="submitLogin()"
          >
            <UFormField label="Логин" name="username" required>
              <UInput
                v-model="loginForm['username']"
                placeholder="Имя пользователя"
                icon="i-lucide-user"
                autofocus
                required
              />
            </UFormField>
            <UFormField label="Пароль" name="password" required>
              <UInput
                v-model="loginForm.password"
                type="password"
                placeholder="Пароль"
                icon="i-lucide-lock-keyhole"
                required
              />
            </UFormField>
            <div v-if="action === 'update'">
              <UFormField label="Новый пароль" name="new_pswd" required>
                <UInput
                  v-model="loginForm.new_pswd"
                  type="password"
                  placeholder="Новый пароль"
                  icon="i-i-lucide-lock-keyhole"
                  required
                />
              </UFormField>
              <UFormField label="Повтор пароля" name="conf_pswd" required>
                <UInput
                  v-model="loginForm.conf_pswd"
                  type="password"
                  placeholder="Подтверждение пароля"
                  icon="i-i-lucide-lock-keyhole"
                  required
                />
              </UFormField>
            </div>
            <div class="flex justify-between mt-2">
              <UButton
                :label="action === 'login' ? 'Войти' : 'Изменить'"
                color="success"
                variant="outline"
                type="submit"
              />
              <UButton
                v-if="action === 'login'"
                label="Изменить"
                color="secondary"
                variant="outline"
                @click="action = 'update'"
              />
              <UButton
                v-if="action === 'update'"
                label="Отмена"
                color="error"
                variant="outline"
                @click="action = 'login'"
              />
            </div>
          </UForm>
        </UCard>
      </div>
    </div>
  </UContainer>
</template>
