<script setup lang="ts">
import type { Persons } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  resume: {
    type: Object as () => Persons,
    default: {} as Persons,
  },
});

const resumeForm = ref(props.resume);

resumeForm.value.birthday = resumeForm.value.birthday
  ? new Date(resumeForm.value.birthday).toISOString().split("T", 1)[0]
  : "";

const validate = (state: Partial<Persons>) => {
  const errors = [];
  const namePathern = /^[А-яЁё][А-яЁёIV\-.,'()\s]*[А-яЁё\s]$/
  if (state.surname && !state.surname.match(namePathern)) {
    errors.push({
      path: "surname",
      message: "Поле содержит недопустимые символы",
    });
  }
  if (state.firstname && !state.firstname.match(namePathern)) {
    errors.push({
      path: "firstname",
      message: "Поле содержит недопустимые символы",
    });
  }
  if (state.patronymic && !state.patronymic.match(namePathern)) {
    errors.push({
      path: "patronymic",
      message: "Поле содержит недопустимые символы",
    });
  }
  if (state.birthday && !state.birthday.match(/^\d{4}-\d{2}-\d{2}$/)) {
    errors.push({
      path: "birthday",
      message: "Поле должно содержать корректную дату",
    });
  }
  if (state.inn && !state.inn.match(/^[0-9]{12}$/)) {
    errors.push({
      path: "inn",
      message: "Поле должно содержать 12 цифр",
    });
  }
  if (state.snils && !state.snils.match(/^[0-9]{11}$/)) {
    errors.push({
      path: "snils",
      message: "Поле должно содержать 11 цифр",
    });
  }
  return errors;
};
</script>

<template>
  <UForm
    :state="resumeForm"
    :validate="validate"
    @submit.prevent="emit('update', resumeForm)"
  >
    <UFormField label="Фамилия" name="surname" required>
      <UInput
        v-model.trim="resumeForm.surname"
        required
        placeholder="Фамилия"
        maxlength="255"
      />
    </UFormField>
    <UFormField label="Имя" name="firstname" required>
      <UInput
        v-model.trim="resumeForm.firstname"
        required
        placeholder="Имя"
        maxlength="255"
      />
    </UFormField>
    <UFormField label="Отчество" name="patronymic">
      <UInput
        v-model.trim="resumeForm.patronymic"
        placeholder="Отчество"
        maxlength="255"
      />
    </UFormField>
    <UFormField label="Дата рождения" name="birthday" required>
      <UInput v-model="resumeForm.birthday" required type="date" />
    </UFormField>
    <UFormField label="Место рождения" name="birthplace">
      <UInput
        v-model.trim.lazy="resumeForm.birthplace"
        placeholder="Место рождения"
        maxlength="255"
      />
    </UFormField>
    <UFormField label="Гражданство" name="citizenship">
      <UInput
        v-model.trim.lazy="resumeForm.citizenship"
        placeholder="Гражданство"
        maxlength="255"
      />
    </UFormField>
    <UFormField label="Двойное гражданство" name="dual">
      <UInput
        v-model.trim.lazy="resumeForm.dual"
        placeholder="Двойное гражданство"
        maxlength="255"
      />
    </UFormField>
    <UFormField label="СНИЛС" name="snils">
      <UInput
        v-model.trim.lazy="resumeForm.snils"
        placeholder="СНИЛС"
        maxlength="11"
      />
    </UFormField>
    <UFormField label="ИНН" name="inn">
      <UInput
        v-model.trim.lazy="resumeForm.inn"
        placeholder="ИНН"
        maxlength="12"
      />
    </UFormField>
    <UFormField label="Семейное положение" name="marital">
      <UInput
        v-model.trim.lazy="resumeForm.marital"
        placeholder="Семейное положение"
        maxlength="255"
      />
    </UFormField>
    <UFormField label="Дополнительно" name="addition">
      <UTextarea
        v-model.trim.lazy="resumeForm.addition"
        placeholder="Дополнительно"
      />
    </UFormField>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
