<script setup lang="ts">
import type { UserForm } from "@/types";
import * as v from "valibot";

const schema = v.object({
  fullname: v.pipe(
    v.string(),
    v.maxLength(255, "Максимальная длина 255 символов"),
    v.minLength(3, "Минимальная длина 3 символа"),
    v.regex(/^[а-яёЁА-Я-\s]+$/, "Поле должно содержать только русские буквы от 3 до 255 символов")
  ),
  username: v.pipe(
    v.string(),
    v.maxLength(255, "Максимальная длина 255 символов"),
    v.minLength(3, "Минимальная длина 3 символа"),
    v.regex(
      /^[a-zA-Z_\s]+$/,
      "Поле должно содержать только латинские буквы и знаки подчеркивания"
    )
  ),
  email: v.pipe(v.string(), v.email("Некорректный email")),
});

const emit = defineEmits(["update"]);

const form = ref({} as UserForm);

async function submitUser() {
  const { message } = (await fetchAuth("/route/user", {
    method: "POST",
    body: form.value,
  })) as Record<string, string>;
  if (message === "success") {
    emit("update");
    form.value = {} as UserForm;
    makeToast("success", "Пользователь успешно добавлен");
  } else {
    makeToast();
  }
}
</script>

<template>
  <div class="m-4">
    <UForm :schema="schema" :state="form" @submit.prevent="submitUser">
      <UFormField label="Имя пользователя" name="fullname" required>
        <UInput
          v-model.lazy.trim="form.fullname"
          placeholder="Имя пользователя"
        />
      </UFormField>
      <UFormField label="Логин" name="username" required>
        <UInput v-model.lazy.trim="form.username" placeholder="Логин" />
      </UFormField>
      <UFormField label="Email" name="email" required>
        <UInput v-model.lazy.trim="form.email" placeholder="Email" />
      </UFormField>
      <UButton
        label="Принять"
        color="success"
        variant="outline"
        type="submit"
      />
    </UForm>
  </div>
</template>
