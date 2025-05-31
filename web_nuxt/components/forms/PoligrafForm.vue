<script setup lang="ts">
import type { Pfo } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Pfo>,
    default: () => ({}),
  },
});

const poligrafForm = toRef(props.item as Pfo);
</script>

<template>
  <UForm
    :state="poligrafForm"
    @submit.prevent="emit('update', poligrafForm)"
  >
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
      />
    </UFormField>
    <UFormField label="Результат" name="results" required>
      <UTextarea
        v-model.trim.lazy="poligrafForm.results"
        autoresize
        placeholder="Результат"
      />
    </UFormField>
    <UFormField label="Результат" name="conclusion" required>
      <USelect
        v-model="poligrafForm.conclusion"
        :items="['БЕЗ ЗАМЕЧАНИЙ', 'С КОММЕНТАРИЯМИ', 'НЕГАТИВ']"
        placeholder="Выберите результат"
      />
    </UFormField>
    <UButton label="Принять" color="success" variant="outline" type="submit" />
  </UForm>
</template>
