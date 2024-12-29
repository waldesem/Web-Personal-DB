<script setup lang="ts">
import { z } from "zod";
import type { Relation } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  relation: {
    type: Object as () => Relation,
    default: {} as Relation,
  },
});

const schema = z.object({
  type: z
    .string({ required_error: "Обязательное поле" })
    .max(255, "Максимум 255 символов"),
  right_id: z
    .number({ required_error: "Обязательное поле" })
});

const relationForm = toRef(props.relation as Relation);

async function submitRelation() {
  emit("update", relationForm.value);
  clearForm();
}

function cancelAction() {
  emit("cancel");
  clearForm();
}

function clearForm() {
  Object.assign(relationForm.value, {
    type: "",
    right_id: "",
  } as Relation);
}
</script>

<template>
  <UForm :state="relationForm" :schema="schema" @submit.prevent="submitRelation">
    <UFormGroup class="mb-3" label="Тип связи" name="type" required>
      <USelect
        v-model.trim.lazy="relationForm['type']"
        required
        :options="[
          'Одно лицо',
          'Родители-Дети',
          'Братья-Сестры',
          'Супруг-Супруга',
          'Родственники',
          'Близкая связь',
        ]"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="ID связи" name="right_id" required>
      <UInput
        v-model.trim.lazy="relationForm['right_id']"
        required
        type="number"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelAction" />
  </UForm>
</template>
