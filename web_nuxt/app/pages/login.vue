<script setup lang="ts">
import type { FormSubmitEvent } from "@nuxt/ui";
import type { Login } from "@/types";

definePageMeta({ layout: false });

onBeforeMount(() => clearNuxtData());

const alerts = useAlertStore();

// Объявляем переменные для формы и состояния
const method = ref<"POST" | "PATCH">("POST");

// Объявляем функцию для отправки формы
async function onSubmit(payload: FormSubmitEvent<Partial<Login>>) {
  try {
    const resp = await $fetch.raw("/routes/auth/login", {
      method: method.value,
      body: payload.data,
    });
    if (resp.status === 200) {
      method.value = "POST";
      alerts.setAlert(
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
        alerts.setAlert(
          "warning",
          "Предупреждение",
          "Пароль просрочен. Измените пароль.",
        );
        method.value = "PATCH";
      }
    } else {
      alerts.setAlert(
        "error",
        "Ошибка",
        "Неправильный логин или пароль. Попробуйте еще раз.",
      );
    }
  } catch (error) {
    console.error(error);
    alerts.setAlert("error", "Внимание", "Ошибка соединения с сервером.");
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
          :color="alerts.alert.color"
          :title="alerts.alert.title"
          :description="alerts.alert.description"
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
                  'info',
                  'Информация',
                  'Введите новый пароль и подтверждение.',
                );
              } else {
                method = 'POST';
                alerts.setAlert(
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
