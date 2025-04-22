<script setup lang="ts">
import type { Education } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  education: {
    type: Object as () => Education,
    default: {} as Education,
  },
});

const educationForm = ref(props.education as Education);
</script>

<template>
  <UForm :state="educationForm" @submit.prevent="emit('update', educationForm)">
    <UFormField class="mb-3" label="Тип образования" name="view" required>
      <USelect
        v-model="educationForm.view"
        required
        :items="[
          'Основное общее',
          'Среднее общее',
          'Среднее профессиональное',
          'Высшее',
          'Неоконченное высшее образование',
          'Другое образование',
        ]"
        placeholder="Выберите тип образования"
      />
    </UFormField>
    <UFormField
      class="mb-3"
      label="Название учебного заведения"
      name="institution"
      required
    >
      <UInput
        v-model.trim.lazy="educationForm.institution"
        required
        placeholder="Название учебного заведения"
        maxlength="255"
      />
    </UFormField>
    <UFormField class="mb-3" label="Год окончания" name="finished">
      <UInput
        v-model.trim.lazy="educationForm.finished"
        placeholder="Год окончания"
        maxlength="4"
      />
    </UFormField>
    <UFormField class="mb-3" label="Специальность" name="specialty">
      <UInput
        v-model.trim.lazy="educationForm.specialty"
        placeholder="Специальность"
        maxlength="255"
      />
    </UFormField>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
