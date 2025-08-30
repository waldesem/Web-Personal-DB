<script setup lang="ts">
import type { Pfo } from '@/types';
import { Decisions } from '@/types';

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Pfo>,
    default: () => ({}),
  },
});

const poligrafForm = toRef(props.item);
</script>

<template>
  <UForm :state="poligrafForm" @submit.prevent="emit('update', poligrafForm)">
    <UFormField label="Тема проверки" name="theme" required>
      <USelect
        v-model="poligrafForm.theme"
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
        v-model.trim.lazy="poligrafForm.results"
        autoresize
        placeholder="Результат"
        required
      />
    </UFormField>
    <UFormField label="Результат" name="conclusion" required>
      <USelect
        v-model="poligrafForm.conclusion"
        :items="Object.values(Decisions)"
        placeholder="Выберите результат"
        required
      />
    </UFormField>
    <ElementsSubmitButton />
  </UForm>
</template>
