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

const schema = z.object({
  theme: z
    .string({ required_error: "Обязательное поле" })
    .max(255, "Максимум 255 символов"),
  results: z.string({ required_error: "Обязательное поле" }),
});

const poligrafForm = toRef(props.poligraf as Pfo);

function submitPoligraf() {
  emit("update", poligrafForm.value);
  poligrafForm.value.theme = "";
  poligrafForm.value.results = "";
}

function cancelAction() {
  emit("cancel");
  poligrafForm.value.theme = "";
  poligrafForm.value.results = "";
}
</script>

<template>
  <UForm :state="poligrafForm" :schema="schema" @submit.prevent="submitPoligraf">
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
    <ElementsBtnGroup @cancel="cancelAction" />
  </UForm>
</template>
