<script setup lang="ts">
import { z } from "zod";
import type { Affilation } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  affils: {
    type: Object as () => Affilation,
    default: {} as Affilation,
  },
  candId: {
    type: String,
    default: "",
  },
});

const schema = z.object({
  view: z
    .string({ required_error: "Обязательное поле" }),
  organization: z
    .string({ required_error: "Обязательное поле" })
    .max(255, "Максимум 255 символов"),
  inn: z
    .string()
    .max(12, "Максимум 12 символов")
    .nullable()
    .optional(),
});

const affilationForm = toRef(props.affils as Affilation);

function submitAffilation() {
  emit("update", affilationForm.value);
  clearForm();
}

function cancelAction() {
  emit("cancel");
  clearForm();
}

function clearForm() {
  Object.assign(affilationForm.value, {
    view: "",
    organization: "",
    inn: "",
  } as Affilation);
}
</script>

<template>
  <UForm :state="affilationForm" :schema="schema" @submit.prevent="submitAffilation">
    <UFormGroup class="mb-3" label="Тип участия" name="view" required>
      <USelect
        v-model.trim.lazy="affilationForm['view']"
        required
        :options="[
          'Являлся государственным/муниципальным служащим',
          'Являлся государственным должностным лицом',
          'Связанные лица работают в государственных организациях',
          'Участвует в деятельности коммерческих организаций',
        ]"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Организация" name="organization" required>
      <UInput
        v-model.trim.lazy="affilationForm['organization']"
        required
        placeholder="Организация"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="ИНН" name="inn">
      <UInput v-model.trim.lazy="affilationForm['inn']" placeholder="ИНН" />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelAction" />
  </UForm>
</template>
