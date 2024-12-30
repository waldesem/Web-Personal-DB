<script setup lang="ts">
import { z } from "zod";
import type { Document } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  docs: {
    type: Object as () => Document,
    default: {} as Document,
  },
});

const docForm = ref(props.docs as Document);
docForm.value.issue = docForm.value.issue
  ? new Date(docForm.value.issue).toISOString().split("T", 1)[0]
  : "";

const schema = z.object({
  view: z
    .string({ required_error: "Обязательное поле" })
    .max(255, "Максимум 255 символов"),
  series: z.string().max(12, "Максимум 12 символов").nullable().optional(),
  digits: z
    .string({ required_error: "Обязательное поле" })
    .max(12, "Максимум 12 символов"),
  agency: z.string().max(255, "Максимум 255 символов").nullable().optional(),
  issue: z
    .string()
    .regex(/^\d{4}-\d{2}-\d{2}$/, "Поле должно содержать корректную дату"),
});
</script>

<template>
  <UForm
    :state="docForm"
    :schema="schema"
    @submit.prevent="emit('update', docForm)"
  >
    <UFormGroup class="mb-3" label="Вид документа" name="view" required>
      <USelect
        v-model="docForm['view']"
        required
        :options="['Паспорт', 'Иностранный паспорт', 'Другое']"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Серия документа" name="series">
      <UInput
        v-model.trim.lazy="docForm['series']"
        placeholder="Серия документа"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Номер документа" name="digits" required>
      <UInput
        v-model.trim.lazy="docForm['digits']"
        required
        placeholder="Номер документа"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Кем выдан" name="agency">
      <UInput v-model.trim="docForm['agency']" placeholder="Кем выдан" />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Дата выдачи" name="issue" required>
      <UInput v-model.trim.lazy="docForm['issue']" required type="date" />
    </UFormGroup>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
