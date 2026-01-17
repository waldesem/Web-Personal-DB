<script setup lang="ts">
import type { UserForm } from "@/types";

const emit = defineEmits(["update"]);

const toasts = useToasts();

const { $api } = useNuxtApp();

const form = ref({} as UserForm);

async function submitUser() {
  const { message } = await $api<Record<string, string>>("/routes/user", {
    method: "POST",
    body: form.value,
  });
  if (message === "success") {
    emit("update");
    form.value = {} as UserForm;
    toasts.create("success", "Пользователь успешно добавлен");
  } else {
    toasts.create();
  }
}
</script>

<template>
  <UForm :state="form" @submit.prevent="submitUser">
    <UFormField label="Имя пользователя" name="fullname" required>
      <UInput
        v-model.lazy.trim="form.fullname"
        placeholder="Имя пользователя"
        maxlength="255"
        required
        pattern="^[а-яёЁА-Я-\s]+$"
      />
    </UFormField>
    <UFormField label="Логин" name="username" required>
      <UInput
        v-model.lazy.trim="form.username"
        placeholder="Логин"
        required
        pattern="^[a-z0-9_-]{3,255}$"
      />
    </UFormField>
    <UFormField label="Email" name="email" type="email" required>
      <UInput v-model.lazy.trim="form.email" placeholder="Email" required />
    </UFormField>
    <ElementSubmitButton />
  </UForm>
</template>
