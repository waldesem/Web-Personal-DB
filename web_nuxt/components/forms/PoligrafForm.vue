<script setup lang="ts">
import type { Pfo } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  item: {
    type: Object as () => Pfo,
    default: {} as Pfo,
  },
});

const poligrafForm = ref(props.item as Pfo);
</script>

<template>
  <UForm :state="poligrafForm" @submit.prevent="emit('update', poligrafForm)">
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
        :items="[
          'БЕЗ ЗАМЕЧАНИЙ',
          'С КОММЕНТАРИЯМИ',
          'НЕГАТИВ',
        ]"
        placeholder="Выберите результат"
      />
    </UFormField>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
