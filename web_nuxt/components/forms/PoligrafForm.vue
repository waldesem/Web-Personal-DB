<script setup lang="ts">
import type { Pfo } from "@/types";
import * as v from "valibot";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Pfo>,
    default: () => ({}),
  },
});

const schema = v.object({
  theme: v.string(),
  results: v.string(),
  conclusion: v.string(),
});

const poligrafForm = toRef(props.item as Pfo);
</script>

<template>
  <UForm
    :schema="schema"
    :state="poligrafForm"
    @submit.prevent="emit('update', poligrafForm)"
  >
    <UFormField label="Тема проверки" name="theme" required>
      <USelect
        v-model="poligrafForm.theme"
        required
        :items="[
          'Проверка кандидата',
          'Служебная проверка',
          'Служебное расследование',
          'Плановое мероприятие',
        ]"
        placeholder="Выберите тему проверки"
      />
    </UFormField>
    <UFormField label="Результат" name="results" required>
      <UTextarea
        v-model.trim.lazy="poligrafForm.results"
        required
        autoresize
        placeholder="Результат"
      />
    </UFormField>
    <UFormField label="Результат" name="conclusion" required>
      <USelect
        v-model="poligrafForm.conclusion"
        required
        :items="['БЕЗ ЗАМЕЧАНИЙ', 'С КОММЕНТАРИЯМИ', 'НЕГАТИВ']"
        placeholder="Выберите результат"
      />
    </UFormField>
    <UButton label="Принять" color="success" variant="outline" type="submit" />
  </UForm>
</template>
