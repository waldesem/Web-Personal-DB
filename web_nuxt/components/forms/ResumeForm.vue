<script setup lang="ts">
import type { Persons } from "@/types";

const emit = defineEmits(["cancel", "update", "clear"]);

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
  if (state.surname && !state.surname.match(/^[а-яёЁА-Я-\s]+$/)) {
    errors.push({
      path: "surname",
      message: "Поле должно содержать только русские буквы",
    });
  }
  if (state.firstname && !state.firstname.match(/^[а-яёЁА-Я-\s]+$/)) {
    errors.push({
      path: "firstname",
      message: "Поле должно содержать только русские буквы",
    });
  }
  if (state.patronymic && !state.patronymic.match(/^[а-яёЁА-Я-\s]+$/)) {
    errors.push({
      path: "patronymic",
      message: "Поле должно содержать только русские буквы",
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
    <UFormField class="mb-3" label="Фамилия" name="surname" required>
      <UInput
        v-model.trim="resumeForm.surname"
        required
        placeholder="Фамилия"
        maxlength="255"
      />
    </UFormField>
    <UFormField class="mb-3" label="Имя" name="firstname" required>
      <UInput
        v-model.trim="resumeForm.firstname"
        required
        placeholder="Имя"
        maxlength="255"
      />
    </UFormField>
    <UFormField class="mb-3" label="Отчество" name="patronymic">
      <UInput
        v-model.trim="resumeForm.patronymic"
        placeholder="Отчество"
        maxlength="255"
      />
    </UFormField>
    <UFormField class="mb-3" label="Дата рождения" name="birthday" required>
      <UInput v-model="resumeForm.birthday" required type="date" />
    </UFormField>
    <UFormField class="mb-3" label="Место рождения" name="birthplace">
      <UInput
        v-model.trim.lazy="resumeForm.birthplace"
        placeholder="Место рождения"
        maxlength="255"
      />
    </UFormField>
    <UFormField class="mb-3" label="Гражданство" name="citizenship">
      <UInput
        v-model.trim.lazy="resumeForm.citizenship"
        placeholder="Гражданство"
        maxlength="255"
      />
    </UFormField>
    <UFormField class="mb-3" label="Двойное гражданство" name="dual">
      <UInput
        v-model.trim.lazy="resumeForm.dual"
        placeholder="Двойное гражданство"
        maxlength="255"
      />
    </UFormField>
    <UFormField class="mb-3" label="СНИЛС" name="snils">
      <UInput
        v-model.trim.lazy="resumeForm.snils"
        placeholder="СНИЛС"
        maxlength="11"
      />
    </UFormField>
    <UFormField class="mb-3" label="ИНН" name="inn">
      <UInput
        v-model.trim.lazy="resumeForm.inn"
        placeholder="ИНН"
        maxlength="12"
      />
    </UFormField>
    <UFormField class="mb-3" label="Семейное положение" name="marital">
      <UInput
        v-model.trim.lazy="resumeForm.marital"
        placeholder="Семейное положение"
        maxlength="255"
      />
    </UFormField>
    <UFormField class="mb-3" label="Дополнительно" name="addition">
      <UTextarea
        v-model.trim.lazy="resumeForm.addition"
        placeholder="Дополнительно"
      />
    </UFormField>
    <ElementsBtnGroup
      @cancel="emit('cancel')"
      @clear="
        emit('clear');
        resumeForm = {} as Persons;
      "
    />
  </UForm>
</template>
