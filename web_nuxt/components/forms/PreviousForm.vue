<script setup lang="ts">
import { z } from "zod";
import type { Previous } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  previous: {
    type: Object as () => Previous,
    default: {} as Previous,
  },
});

const schema = z.object({
  surname: z
    .string({ required_error: "Обязательное поле" })
    .max(255, "Максимум 255 символов"),
  firstname: z
    .string({ required_error: "Обязательное поле" })
    .max(255, "Максимум 255 символов"),
  patronymic: z
    .string()
    .max(255, "Максимум 255 символов")
    .nullable()
    .optional(),
  changed: z
    .string()
    .max(4, "Максимум 4 символа")
    .nullable()
    .optional(),
  reason: z
    .string()
    .max(255, "Максимум 255 символов")
    .nullable()
    .optional(),
});

const previousForm = toRef(props.previous as Previous);

function submitPrevious() {
  emit("update", previousForm.value);
  clearForm();
}

function cancelAction() {
  emit("cancel");
  clearForm();
}

function clearForm() {
  Object.assign(previousForm.value, {
    surname: "",
    firstname: "",
    patronymic: "",
    changed: "",
    reason: "",
  } as Previous);
}
</script>

<template>
  <UForm :state="previousForm" :schema="schema" @submit.prevent="submitPrevious">
    <UFormGroup class="mb-3" label="Фамилия" name="surname" required>
      <UInput
        v-model.trim.lazy="previousForm['surname']"
        required
        placeholder="Фамилия"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Имя" name="firstname" required>
      <UInput
        v-model.trim.lazy="previousForm['firstname']"
        required
        placeholder="Имя"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Отчество" name="patronymic">
      <UInput
        v-model.trim.lazy="previousForm['patronymic']"
        placeholder="Отчество"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Год изменения" name="changed">
      <UInput
        v-model.trim.lazy="previousForm['changed']"
        placeholder="Год изменения"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Причина изменения" name="reason">
      <UInput
        v-model.trim.lazy="previousForm['reason']"
        placeholder="Причина изменения"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelAction" />
  </UForm>
</template>
