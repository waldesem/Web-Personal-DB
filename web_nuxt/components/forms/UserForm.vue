<script setup lang="ts">
import type { UserForm } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const form = ref({} as UserForm);

const validate = (state: Partial<UserForm>) => {
  const errors = [];
  if (state.fullname && !state.fullname.match(/^[а-яёЁА-Я-\s]+$/)) {
    errors.push({
      path: "fullname",
      message: "Поле должно содержать только русские буквы",
    });
  }
  if (state.username && !state.username.match(/^[a-zA-Z_\s]+$/)) {
    errors.push({
      path: "username",
      message:
        "Поле должно содержать только латинские буквы и знаки подчеркивания",
    });
  }
  if (
    state.email &&
    !state.email.match(/^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/)
  ) {
    errors.push({
      path: "email",
      message: "Поле должно содержать корректную почту",
    });
  }
  return errors;
};

async function submitUser() {
  const { message } = (await useFetchAuth("/route/user", {
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
    <UForm :validate="validate" :state="form" @submit.prevent="submitUser">
      <UFormField label="Имя пользователя" name="fullname" required>
        <UInput
          v-model="form.fullname"
          placeholder="Имя пользователя"
          required
        />
      </UFormField>
      <UFormField label="Логин" name="username" required>
        <UInput v-model="form.username" placeholder="Логин" />
      </UFormField>
      <UFormField label="Email" name="email" required>
        <UInput v-model="form.email" placeholder="Email" />
      </UFormField>
      <ElementsBtnGroup
        @cancel="
          emit('cancel');
          form = {} as UserForm;
        "
      />
    </UForm>
  </div>
</template>
