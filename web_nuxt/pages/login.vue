<script setup lang="ts">
import type { AlertProps } from "@nuxt/ui";
import type { Login } from "@/types";

// Определяем мета-данные для страницы - не показывать layout
definePageMeta({ layout: false });


// Объявляем переменные для формы и состояния
const action = ref("login");
const loginForm = ref({} as Login);

// Объявляем переменную для показа алерта
const alert = ref({
  color: "success",
  title: "Информация",
  description: "Введите логин и пароль",
  icon: "i-lucide-circle-alert",
});

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
    "/route/auth/" + action.value,
    {
      method: "POST",
      body: loginForm.value,
    }
  )) as { message: string; access_token: string; refresh_token: string };
  if (message === "success") {
    const token = useCookie("token", {
      maxAge: 60 * 59,
      sameSite: 'strict',
      watch: "shallow",
    });
    const refresh = useCookie("refresh", {
      maxAge: 60 * 60 * 24 * 30,
      sameSite: 'strict',
      watch: "shallow",
    });
    token.value = access_token.split(" ")[1];
    refresh.value = refresh_token.split(" ")[1];
    return navigateTo("/persons");
  } else if (message === "updated") {
    action.value = "login";
    Object.assign(alert.value, {
      color: "success",
      title: "Информация",
      description: "Войдите с новым паролем.",
      icon: "i-lucide-circle-alert",
    });
  } else if (message === "denied") {
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
        <!-- Алерт -->
        <UAlert
          variant="subtle"
          :color="(alert.color as AlertProps['color'])"
          :title="alert.title"
          :description="alert.description"
          :icon="alert.icon"
        />

        <!-- Заголовок -->
        <h3 class="text-2xl text-blue-800 font-bold my-6">
          Кадровая безопасность
        </h3>

        <!-- Форма логина -->
        <UCard>
          <h3 class="text-xl text-red-800 font-bold mb-2">Вход в систему</h3>
          <UForm
            :validate="validate"
            :state="loginForm"
            @submit.prevent="submitLogin()"
          >
            <UFormField label="Логин" name="username" required>
              <UInput
                v-model.trim="loginForm['username']"
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
            
            <!-- Кнопки для входа или изменения пароля -->
            <div class="flex justify-between mt-2">
              <UButton
                :label="action === 'login' ? 'Войти' : 'Изменить'"
                color="success"
                variant="outline"
                type="submit"
              />
              <UButton
                :label="action == 'login' ? 'Изменить' : 'Отмена'"
                color="secondary"
                variant="outline"
                @click="
                  action == 'login' ? (action = 'update') : (action = 'login')
                "
              />
            </div>
          </UForm>
        </UCard>
      </div>
    </div>
  </UContainer>
</template>
