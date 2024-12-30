<script setup lang="ts">
import { z } from "zod";
import type { Pfo } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  poligraf: {
    type: Object as () => Pfo,
    default: {} as Pfo,
  },
});

const poligrafForm = ref(props.poligraf as Pfo);

const schema = z.object({
  theme: z
    .string({ required_error: "Обязательное поле" })
    .max(255, "Максимум 255 символов"),
  results: z.string({ required_error: "Обязательное поле" }),
});
</script>

<template>
  <UForm
    :state="poligrafForm"
    :schema="schema"
    @submit.prevent="emit('update', poligrafForm)"
  >
    <UFormGroup class="mb-3" label="Тема проверки" name="theme" required>
      <USelect
        v-model="poligrafForm['theme']"
        required
        :options="[
          'Проверка кандидата',
          'Служебная проверка',
          'Служебное расследование',
          'Плановое мероприятие',
        ]"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Результат" name="results" required>
      <UTextarea
        v-model.trim.lazy="poligrafForm['results']"
        required
        autoresize
        placeholder="Результат"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
