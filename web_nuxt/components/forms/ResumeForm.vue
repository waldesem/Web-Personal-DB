<script setup lang="ts">
import { z } from "zod";
import type { Persons } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  resume: {
    type: Object as () => Persons,
    default: {} as Persons,
  },
});

const schema = z.object({
  surname: z
    .string()
    .max(255)
    .regex(/^[а-яёЁА-Я-\s]+$/, "Поле должно содержать только русские буквы"),
  firstname: z
    .string()
    .max(255)
    .regex(/^[а-яёЁА-Я-\s]+$/, "Поле должно содержать только русские буквы"),
  patronymic: z
    .string()
    .max(255)
    .regex(/^[а-яёЁА-Я-\s]+$/, "Поле должно содержать только русские буквы")
    .optional(),
  birthday: z
    .string()
    .regex(
      /^[0-9]{4}-[0-9]{2}-[0-9]{2}$/,
      "Поле должно содержать корректную дату"
    ),
  birthplace: z.string().max(255).optional(),
  citizenship: z.string().max(255).optional(),
  dual: z.string().max(255).optional(),
  inn: z
    .string()
    .regex(/^[0-9]{12}$/, "Поле должно содержать 12 цифр")
    .optional(),
  snils: z
    .string()
    .regex(/^[0-9]{11}$/, "Поле должно содержать 11 цифр")
    .optional(),
  marital: z.string().max(255).optional(),
  addition: z.string().optional(),
});

const resumeForm = toRef(props.resume);

resumeForm.value.birthday = resumeForm.value.birthday
  ? new Date(resumeForm.value.birthday).toISOString().split("T", 1)[0]
  : "";

function cancelOperation() {
  emit("cancel");
  cancelEdit();
}

function cancelEdit() {
  Object.assign(resumeForm.value, {
    surname: "",
    firstname: "",
    patronymic: "",
    birthday: "",
    birthplace: "",
    citizenship: "",
    dual: "",
    inn: "",
    snils: "",
    marital: "",
    addition: "",
  } as Persons);
}

async function submitResume() {
  emit("update", resumeForm.value);
  cancelEdit();
}
</script>

<template>
  <UForm :state="resumeForm" :schema="schema" @submit.prevent="submitResume">
    <UFormGroup class="mb-3" label="Фамилия" name="surname" required>
      <UInput
        v-model.trim="resumeForm['surname']"
        required
        placeholder="Фамилия"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Имя" name="firstname" required>
      <UInput
        v-model.trim="resumeForm['firstname']"
        required
        placeholder="Имя"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Отчество" name="patronymic">
      <UInput v-model.trim="resumeForm['patronymic']" placeholder="Отчество" />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Дата рождения" name="birthday" required>
      <UInput v-model="resumeForm['birthday']" required type="date" />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Место рождения">
      <UInput
        v-model.trim.lazy="resumeForm['birthplace']"
        placeholder="Место рождения"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Гражданство" name="citizenship">
      <UInput
        v-model.trim="resumeForm['citizenship']"
        placeholder="Гражданство"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Двойное гражданство" name="dual">
      <UInput
        v-model.trim="resumeForm['dual']"
        placeholder="Двойное гражданство"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="СНИЛС" name="snils">
      <UInput v-model.trim.lazy="resumeForm['snils']" placeholder="СНИЛС" />
    </UFormGroup>
    <UFormGroup class="mb-3" label="ИНН" name="inn">
      <UInput v-model.trim.lazy="resumeForm['inn']" placeholder="ИНН" />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Семейное положение" name="marital">
      <UInput
        v-model.trim.lazy="resumeForm['marital']"
        placeholder="Семейное положение"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Дополнительно">
      <UTextarea
        v-model.trim.lazy="resumeForm['addition']"
        placeholder="Дополнительно"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelOperation" />
  </UForm>
</template>
