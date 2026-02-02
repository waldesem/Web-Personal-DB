<script setup lang="ts">
import type { Person } from "@/types";

const emit = defineEmits(["update"]);

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
  ? new Date(form.value.birthday).toLocaleDateString()
  : "";

async function submitPerson() {
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
  if (!state.surname?.match(/^[А-ЯЁ][А-ЯЁIV\-.,'()\s]*[А-ЯЁ]$/)) {
    errors.push({
      name: "surname",
      message: "Введите корректную фамилию",
    });
  }
  if (!state.firstname?.match(/^[А-ЯЁ][А-ЯЁIV\-.,'()\s]*[А-ЯЁ]$/)) {
    errors.push({
      name: "firstname",
      message: "Введите корректное имя",
    });
  }
  if (
    state.patronymic &&
    !state.patronymic?.match(/^[А-ЯЁ][А-ЯЁIV\-.,'()\s]*[А-ЯЁ]$/)
  ) {
    errors.push({
      name: "patronymic",
      message: "Введите корректное отчество",
    });
  }
  return errors;
};
</script>

<template>
  <UForm :state="form" :validate="validate" @submit.prevent="submitPerson()">
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
      <UInput
        v-model="form.birthday"
        type="date"
        :max="new Date().toISOString().split('T')[0]"
        min="1990-01-01"
        required
      />
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
        pattern="^[0-9]{11}$"
      />
    </UFormField>
    <UFormField label="ИНН" name="inn">
      <UInput
        v-model.lazy.trim="form.inn"
        placeholder="ИНН"
        pattern="^[0-9]{12}$"
      />
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
