<script setup lang="ts">
import type { Pfo } from "@/types";
import { Decisions } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Pfo>,
    default: () => ({}),
  },
});

const form = toRef(props.item);
</script>

<template>
  <UForm :state="form" @submit.prevent="emit('update', form)">
    <UFormField label="Тема проверки" name="theme" required>
      <USelect
        v-model="form.theme"
        :items="[
          'Проверка кандидата',
          'Служебная проверка',
          'Служебное расследование',
          'Плановое мероприятие',
        ]"
        placeholder="Выберите тему проверки"
        required
      />
    </UFormField>
    <UFormField label="Результат" name="results" required>
      <UTextarea
        v-model.trim.lazy="form.results"
        autoresize
        placeholder="Результат"
        required
      />
    </UFormField>
    <UFormField label="Результат" name="conclusion" required>
      <USelect
        v-model="form.conclusion"
        :items="Object.values(Decisions)"
        placeholder="Выберите результат"
        required
      />
    </UFormField>
    <UButton label="Принять" color="success" variant="outline" type="submit" />
  </UForm>
</template>
