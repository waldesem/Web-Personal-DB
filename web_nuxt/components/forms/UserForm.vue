<script setup lang="ts">

const toast = useToast();

const emit = defineEmits(["cancel", "update"]);

type UserForm = {
  fullname: string;
  username: string;
  email: string;
};

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
    toast.add({
      icon: "i-heroicons-check-circle",
      title: "Информация",
      description: "Пользователь успешно добавлен",
      color: "success",
    });
  } else {
    toast.add({
      icon: "i-heroicons-information-circle",
      title: "Внимание",
      description: "Ошибка данных или пользователь уже существует",
      color: "error",
    });
  }
}
</script>

<template>
   <UCard class="m-2">
    <UForm :validate="validate" :state="form" @submit.prevent="submitUser">
      <UFormField
        class="mb-3"
        label="Имя пользователя"
        name="fullname"
        required
      >
        <UInput
          v-model="form.fullname"
          placeholder="Имя пользователя"
          required
        />
      </UFormField>
      <UFormField class="mb-3" label="Логин" name="username">
        <UInput v-model="form.username" placeholder="Логин" required />
      </UFormField>
      <UFormField class="mb-3" label="Email" name="email">
        <UInput v-model="form.email" placeholder="Email" required />
      </UFormField>
      <ElementsBtnGroup
        @cancel="
          emit('cancel');
          form = {} as UserForm;
        "
      />
    </UForm>
  </UCard>
</template>
