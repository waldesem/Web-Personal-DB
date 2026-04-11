<script setup lang="ts">
import type { FormSubmitEvent } from "@nuxt/ui";
import type { Auth, Login } from "@/types";

definePageMeta({ layout: false });

onBeforeMount(() => clearNuxtData());

const alerts = useAlert();

// Объявляем переменные для формы и состояния
const method = ref<"POST" | "PATCH">("POST");

// Объявляем функцию для отправки формы
async function onSubmit(payload: FormSubmitEvent<Partial<Login>>) {
  const resp = await $fetch
    .raw("/routes/auth/login", {
      method: method.value,
      body: payload.data,
    })
    .catch((error) => {
      if (error.data.status_code === 401) {
        alerts.setAlert(
          "i-lucide-triangle-alert",
          "error",
          "Ошибка",
          "Неправильный логин или пароль. Попробуйте еще раз.",
        );
      } else console.error(error.data);
      alerts.setAlert(
        "i-lucide-triangle-alert",
        "error",
        "Внимание",
        "Ошибка соединения с сервером.",
      );
    });
  if (resp?.status === 200) {
    method.value = "POST";
    alerts.setAlert(
      "i-lucide-octagon-alert",
      "success",
      "Информация",
      "Пароль успешно изменен. Войдите с новым паролем.",
    );
  } else if (resp?.status === 201) {
    const { message, access_token, refresh_token } = resp._data as Auth;
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
      [token.value, refresh.value] = [access_token, refresh_token];
      return navigateTo("/persons");
    } else {
      alerts.setAlert(
        "i-lucide-octagon-alert",
        "warning",
        "Предупреждение",
        "Пароль просрочен. Измените пароль.",
      );
      method.value = "PATCH";
    }
  } else {
    alerts.setAlert(
      "i-lucide-triangle-alert",
      "error",
      "Ошибка",
      "Неправильный логин или пароль. Попробуйте еще раз.",
    );
  }
}
</script>

<template>
  <UPageCard class="w-full max-w-md m-auto my-[20vh]">
    <UAuthForm
      description="Доступ в систему кадровой безопасности."
      icon="i-lucide-user-lock"
      :validate="method === 'POST' ? validatorLogin : validatorUpdate"
      :fields="method == 'POST' ? fieldsLogin : fieldsUpdate"
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
          :icon="alerts.alert.value.icon"
          :color="alerts.alert.value.color"
          :title="alerts.alert.value.title"
          :description="alerts.alert.value.description"
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
                alerts.setAlert(
                  'i-lucide-octagon-alert',
                  'info',
                  'Информация',
                  'Введите новый пароль и подтверждение.',
                );
              } else {
                method = 'POST';
                alerts.setAlert(
                  'i-lucide-circle-alert',
                  'success',
                  'Информация',
                  'Введите логин и пароль',
                );
              }
            }
          "
        />
      </template>
    </UAuthForm>
  </UPageCard>
</template>
