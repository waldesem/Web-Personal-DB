<script setup lang="ts">
import type { Previous } from "@/types";
import * as v from "valibot";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type:  Object as PropType<Previous>,
    default: () => ({}),
  },
});

const schema = v.object({
  surname: v.pipe(
    v.string(),
    v.maxLength(255, "Максимальная длина 255 символов")
  ),
  firstname: v.pipe(
    v.string(),
    v.maxLength(255, "Максимальная длина 255 символов")
  ),
  patronymic: v.pipe(
    v.string(),
    v.maxLength(255, "Максимальная длина 255 символов")
  ),
  changed: v.pipe(
    v.string(),
    v.maxLength(4, "Максимальная длина 4 символа")
  ),
  reason: v.pipe(
    v.string(),
    v.maxLength(255, "Максимальная длина 255 символа")
  ),
});

const previousForm = toRef(props.item as Previous);
</script>

<template>
  <UForm :schema="schema" :state="previousForm" @submit.prevent="emit('update', previousForm)">
    <UFormField label="Фамилия" name="surname" required>
      <UInput
        v-model.trim.lazy="previousForm.surname"
        required
        placeholder="Фамилия"
      />
    </UFormField>
    <UFormField label="Имя" name="firstname" required>
      <UInput
        v-model.trim.lazy="previousForm.firstname"
        required
        placeholder="Имя"
      />
    </UFormField>
    <UFormField label="Отчество" name="patronymic">
      <UInput
        v-model.trim.lazy="previousForm.patronymic"
        placeholder="Отчество"
      />
    </UFormField>
    <UFormField label="Год изменения" name="changed">
      <UInput
        v-model.trim.lazy="previousForm.changed"
        placeholder="Год изменения"
      />
    </UFormField>
    <UFormField label="Причина изменения" name="reason">
      <UInput
        v-model.trim.lazy="previousForm.reason"
        placeholder="Причина изменения"
      />
    </UFormField>
    <UButton
        label="Принять"
        color="success"
        variant="outline"
        type="submit"
      />
  </UForm>
</template>
