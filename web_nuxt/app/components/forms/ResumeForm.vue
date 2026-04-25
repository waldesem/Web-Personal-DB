<script setup lang="ts">
import { schemaResume } from "@/schema";
import type { Person } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  resume: {
    type: Object as PropType<Person>,
    default: () => ({}),
  },
});

const form = ref({
  surname: props.resume.surname ?? "",
  firstname: props.resume.firstname ?? "",
  patronymic: props.resume.patronymic ?? "",
  birthday: props.resume.birthday ?? "",
  birthplace: props.resume.birthplace ?? "",
  citizenship: props.resume.citizenship ?? "",
  dual: props.resume.dual ?? "",
  snils: props.resume.snils ?? "",
  inn: props.resume.inn ?? "",
  marital: props.resume.marital ?? "",
  addition: props.resume.addition ?? "",
});

const upperCase = (ev: { target: HTMLInputElement }) => {
  const field = ev.target.name;
  form.value[field as keyof typeof form.value] = ev.target.value.toUpperCase();
};
</script>

<template>
  <UForm
    :state="form"
    :schema="schemaResume"
    @submit.prevent="emit('update', form)"
  >
    <UFormField label="Фамилия" name="surname" required>
      <UInput :value="form.surname" placeholder="Фамилия" @input="upperCase" />
    </UFormField>
    <UFormField label="Имя" name="firstname" required>
      <UInput :value="form.firstname" placeholder="Имя" @input="upperCase" />
    </UFormField>
    <UFormField label="Отчество" name="patronymic">
      <UInput
        :value="form.patronymic"
        placeholder="Отчество"
        @input="upperCase"
      />
    </UFormField>
    <UFormField label="Дата рождения" name="birthday" required>
      <UInput v-model="form.birthday" type="date" />
    </UFormField>
    <UFormField label="Место рождения" name="birthplace">
      <UInput
        v-model.lazy.trim="form.birthplace"
        placeholder="Место рождения"
      />
    </UFormField>
    <UFormField label="Гражданство" name="citizenship">
      <UInput v-model.lazy.trim="form.citizenship" placeholder="Гражданство" />
    </UFormField>
    <UFormField label="Двойное гражданство" name="dual">
      <UInput v-model.lazy.trim="form.dual" placeholder="Двойное гражданство" />
    </UFormField>
    <UFormField label="СНИЛС" name="snils">
      <UInput v-model.lazy.trim="form.snils" placeholder="СНИЛС" />
    </UFormField>
    <UFormField label="ИНН" name="inn">
      <UInput v-model.lazy.trim="form.inn" placeholder="ИНН" />
    </UFormField>
    <UFormField label="Семейное положение" name="marital">
      <UInput
        v-model.lazy.trim="form.marital"
        placeholder="Семейное положение"
      />
    </UFormField>
    <UFormField label="Дополнительно" name="addition">
      <UTextarea
        v-model.lazy.trim="form.addition"
        placeholder="Дополнительно"
      />
    </UFormField>
    <UButton label="Принять" color="success" variant="outline" type="submit" />
  </UForm>
</template>
