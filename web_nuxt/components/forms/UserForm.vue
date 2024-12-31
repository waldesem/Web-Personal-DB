<script setup lang="ts">
import { z } from "zod";

const authFetch = useFetchAuth();

const toast = useToast();

const emit = defineEmits(["cancel", "update"]);

type UserForm = z.infer<typeof schema>;

const form = ref({} as UserForm);

const schema = z.object({
  username: z
    .string({ required_error: "Обязательное поле" })
    .max(255)
    .regex(
      /^[a-zA-Z_\s]+$/,
      "Поле должно содержать только латинские буквы и знаки подчеркивания"
    ),
  fullname: z
    .string({ required_error: "Обязательное поле" })
    .max(255)
    .regex(/^[а-яёЁА-Я-\s]+$/, "Поле должно содержать только русские буквы"),
  email: z
    .string({ required_error: "Обязательное поле" })
    .max(255)
    .regex(
      /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
      "Поле должно содержать корректную почту"
    ),
});

async function submitUser() {
  const { message } = (await authFetch("/route/user", {
    method: "POST",
    body: form.value,
  })) as Record<string, string>;
  if (message === "success") {
    emit("update");
    form.value = {} as UserForm;
    toast.add({
      icon: "i-heroicons-check-circle",
      title: "Информация",
      description: "Пользователь успешно добавлен",
      color: "green",
    });
  } else {
    toast.add({
      icon: "i-heroicons-information-circle",
      title: "Внимание",
      description: "Ошибка данных или пользователь уже существует",
      color: "red",
    });
  }
}
</script>

<template>
  <ElementsCardDiv>
    <UForm :schema="schema" :state="form" @submit.prevent="submitUser">
      <UFormGroup
        class="mb-3"
        label="Имя пользователя"
        name="fullname"
        required
      >
        <UInput
          v-model="form['fullname']"
          placeholder="Имя пользователя"
          required
        />
      </UFormGroup>
      <UFormGroup class="mb-3" label="Логин" name="username">
        <UInput v-model="form['username']" placeholder="Логин" required />
      </UFormGroup>
      <UFormGroup class="mb-3" label="Email" name="email">
        <UInput v-model="form['email']" placeholder="Email" required />
      </UFormGroup>
      <ElementsBtnGroup
        @cancel="
          emit('cancel');
          form = {} as UserForm;
        "
      />
    </UForm>
  </ElementsCardDiv>
</template>
