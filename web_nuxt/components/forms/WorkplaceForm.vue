<script setup lang="ts">
import { z } from "zod";
import type { Work } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  work: {
    type: Object as () => Work,
    default: {} as Work,
  },
});

const schema = z.object({
  now_work: z.boolean().nullable().optional(),
  starts: z
    .string()
    .regex(/^\d{4}-\d{2}-\d{2}$/, "Поле должно содержать корректную дату"),
  finished: z
    .string()
    .regex(/^\d{4}-\d{2}-\d{2}$/, "Поле должно содержать корректную дату"),
  workplace: z
    .string({ required_error: "Обязательное поле" })
    .max(255, "Максимум 255 символов")
    .optional(),
  position: z
    .string({ required_error: "Обязательное поле" })
    .max(255, "Максимум 255 символов")
    .optional(),
  addresses: z.string().max(255, "Максимум 255 символов").nullable().optional(),
  reason: z.string().max(255, "Максимум 255 символов").nullable().optional(),
});

const workForm = toRef(props.work as Work);

workForm.value.starts = workForm.value.starts
  ? new Date(workForm.value.starts).toISOString().split("T", 1)[0]
  : "";
workForm.value.finished = workForm.value.finished
  ? new Date(workForm.value.finished).toISOString().split("T", 1)[0]
  : "";

function submitWorkplace() {
  emit("update", workForm.value);
  clearForm();
}

function cancelAction() {
  emit("cancel");
  clearForm();
}

function clearForm() {
  Object.assign(workForm.value, {
    now_work: false,
    starts: "",
    finished: "",
    workplace: "",
    position: "",
    addresses: "",
    reason: "",
  } as Work);
}
</script>

<template>
  <UForm :state="workForm" :schema="schema" @submit.prevent="submitWorkplace">
    <UFormGroup class="mb-3" label="Текущая работа" name="now_work">
      <UCheckbox v-model="workForm['now_work']" />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Начало работы" name="starts" required>
      <UInput
        v-model="workForm['starts']"
        required
        placeholder="Начало работы"
        type="date"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Окончание работы" name="finished" required>
      <UInput
        v-model="workForm['finished']"
        required
        placeholder="Окончание работы"
        type="date"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Место работы" name="workplace" required>
      <UInput
        v-model.trim.lazy="workForm['workplace']"
        required
        placeholder="Место работы"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Должность" name="position" required>
      <UInput
        v-model.trim.lazy="workForm['position']"
        required
        placeholder="Должность"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Адрес организации" name="addresses">
      <UInput
        v-model.trim.lazy="workForm['addresses']"
        placeholder="Адрес организации"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Причина увольнения" name="reason">
      <UInput
        v-model.trim.lazy="workForm['reason']"
        placeholder="Причина увольнения"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelAction" />
  </UForm>
</template>
