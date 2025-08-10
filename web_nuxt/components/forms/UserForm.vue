<script setup lang="ts">
const emit = defineEmits(["update"]);

interface UserForm {
  fullname: string;
  username: string;
  email: string;
}

const { $api } = useNuxtApp();

const form = ref({} as UserForm);

const validate = (state: Partial<UserForm>) => {
  const errors = [];
  if (state.fullname && !state.fullname.match(/^[а-яёЁА-Я-\s]+$/)) {
    errors.push({
      name: "fullname",
      message: "Поле содержит недопустимые символы",
    });
  }
  if (state.username && !state.username.match(/^[a-z0-9_-]{3,16}$/)) {
    errors.push({
      name: "username",
      message: "Поле содержит недопустимые символы",
    });
  }
  return errors;
};

async function submitUser() {
  const { message } = await $api<Record<string, string>>("/route/user", {
    method: "POST",
    body: form.value,
  });
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
  <UForm :validate="validate" :state="form" @submit.prevent="submitUser">
    <UFormField label="Имя пользователя" name="fullname" required>
      <UInput
        v-model.lazy.trim="form.fullname"
        placeholder="Имя пользователя"
        maxlength="255"
        required
      />
    </UFormField>
    <UFormField label="Логин" name="username" required>
      <UInput
        v-model.lazy.trim="form.username"
        placeholder="Логин"
        maxlength="255"
        minlength="3"
        required
      />
    </UFormField>
    <UFormField label="Email" name="email" type="email" required>
      <UInput v-model.lazy.trim="form.email" placeholder="Email" required />
    </UFormField>
    <ElementsSubmitButton />
  </UForm>
</template>
