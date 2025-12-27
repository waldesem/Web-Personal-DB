<script setup lang="ts">
import { useDateFormat } from "@vueuse/core";
import type { Person } from "@/types";

const emit = defineEmits(["pending", "update"]);

const props = defineProps({
  resume: {
    type: Object as PropType<Person>,
    default: () => ({}),
  },
});

const form = toRef(props.resume);

const { $api } = useNuxtApp();

// Преобразование даты в формат YYYY-MM-DD
form.value.birthday = form.value.birthday
  ? useDateFormat(form.value.birthday, "YYYY-MM-DD").value
  : "";

async function submitPerson() {
  emit("pending");
  const { person_id, exists } = await $api<{
    person_id: number;
    exists: boolean;
  }>("/routes/persons", {
    method: "POST",
    body: form.value,
  });
  emit("update", person_id, exists);
}

const validate = (state: Partial<Person>) => {
  const errors = [];
  const namePathern = /^[А-яЁё][А-яЁёIV\-.,'()\s]*[А-яЁё\s]$/;
  if (state.surname && !state.surname.match(namePathern)) {
    errors.push({
      name: "surname",
      message: "Поле содержит недопустимые символы",
    });
  }
  if (state.firstname && !state.firstname.match(namePathern)) {
    errors.push({
      name: "firstname",
      message: "Поле содержит недопустимые символы",
    });
  }
  if (state.patronymic && !state.patronymic.match(namePathern)) {
    errors.push({
      name: "patronymic",
      message: "Поле содержит недопустимые символы",
    });
  }
  if (state.inn && !state.inn.match(/^[0-9]{12}$/)) {
    errors.push({
      name: "inn",
      message: "Поле должно содержать 12 цифр",
    });
  }
  if (state.snils && !state.snils.match(/^[0-9]{11}$/)) {
    errors.push({
      name: "snils",
      message: "Поле должно содержать 11 цифр",
    });
  }
  return errors;
};
</script>

<template>
  <UForm :validate="validate" :state="form" @submit.prevent="submitPerson()">
    <UFormField label="Фамилия" name="surname" required>
      <UInput
        v-model.lazy.trim="form.surname"
        placeholder="Фамилия"
        maxlength="255"
        required
      />
    </UFormField>
    <UFormField label="Имя" name="firstname" required>
      <UInput
        v-model.lazy.trim="form.firstname"
        placeholder="Имя"
        maxlength="255"
        required
      />
    </UFormField>
    <UFormField label="Отчество" name="patronymic">
      <UInput
        v-model.lazy.trim="form.patronymic"
        placeholder="Отчество"
        maxlength="255"
      />
    </UFormField>
    <UFormField label="Дата рождения" name="birthday" required>
      <UInput v-model="form.birthday" type="date" required />
    </UFormField>
    <UFormField label="Место рождения" name="birthplace">
      <UInput
        v-model.lazy.trim="form.birthplace"
        placeholder="Место рождения"
        maxlength="255"
      />
    </UFormField>
    <UFormField label="Гражданство" name="citizenship">
      <UInput
        v-model.lazy.trim="form.citizenship"
        placeholder="Гражданство"
        maxlength="255"
      />
    </UFormField>
    <UFormField label="Двойное гражданство" name="dual">
      <UInput
        v-model.lazy.trim="form.dual"
        placeholder="Двойное гражданство"
        maxlength="255"
      />
    </UFormField>
    <UFormField label="СНИЛС" name="snils">
      <UInput
        v-model.lazy.trim="form.snils"
        placeholder="СНИЛС"
        maxlength="11"
      />
    </UFormField>
    <UFormField label="ИНН" name="inn">
      <UInput v-model.lazy.trim="form.inn" placeholder="ИНН" maxlength="12" />
    </UFormField>
    <UFormField label="Семейное положение" name="marital">
      <UInput
        v-model.lazy.trim="form.marital"
        placeholder="Семейное положение"
        maxlength="255"
      />
    </UFormField>
    <UFormField label="Дополнительно" name="addition">
      <UTextarea
        v-model.lazy.trim="form.addition"
        placeholder="Дополнительно"
      />
    </UFormField>
    <ElementSubmitButton />
  </UForm>
</template>
