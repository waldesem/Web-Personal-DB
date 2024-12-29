<script setup lang="ts">
import { z } from "zod";
import type { Education } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  education: {
    type: Object as () => Education,
    default: {} as Education,
  },
});

const schema = z.object({
  view: z
    .string({ required_error: "Обязательное поле" }),
  institution: z
    .string({ required_error: "Обязательное поле" })
    .max(255, "Максимум 255 символов"),
  finished: z
    .string()
    .max(4, "Максимум 4 символа")
    .nullable()
    .optional(),
  specialty: z
    .string()
    .max(255, "Максимум 255 символов")
    .nullable()
    .optional(),
});

const educationForm = toRef(props.education as Education);

function submitEducation() {
  emit("update", educationForm.value);
  clearForm();
}

function cancelAction() {
  emit("cancel");
  clearForm();
}

function clearForm() {
  Object.assign(educationForm.value, {
    view: "",
    institution: "",
    finished: "",
    specialty: "",
  } as Education);
}
</script>

<template>
  <UForm :state="educationForm" :schema="schema" @submit.prevent="submitEducation">
    <UFormGroup class="mb-3" label="Вид образования" name="view" required>
      <USelect
        v-model="educationForm['view']"
        required
        :options="[
          'Основное общее',
          'Среднее общее',
          'Среднее профессиональное',
          'Высшее',
          'Неоконченное высшее образование',
          'Другое образование',
        ]"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Название учебного заведения" name="institution" required>
      <UInput
        v-model.trim.lazy="educationForm['institution']"
        required
        placeholder="Название учебного заведения"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Год окончания" name="finished">
      <UInput
        v-model.trim.lazy="educationForm['finished']"
        placeholder="Год окончания"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Специальность" name="specialty">
      <UInput
        v-model.trim.lazy="educationForm['specialty']"
        placeholder="Специальность"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelAction" />
  </UForm>
</template>
