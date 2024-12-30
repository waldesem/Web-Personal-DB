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

const previousForm = ref(props.previous as Previous);

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
  changed: z.string().max(4, "Максимум 4 символа").nullable().optional(),
  reason: z.string().max(255, "Максимум 255 символов").nullable().optional(),
});
</script>

<template>
  <UForm
    :state="previousForm"
    :schema="schema"
    @submit.prevent="emit('update', previousForm)"
  >
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
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
