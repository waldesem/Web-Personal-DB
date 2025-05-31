<script setup lang="ts">
import type { Education } from "@/types";
import * as v from "valibot";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Education>,
    default: () => ({}),
  },
});

const schema = v.object({
  view: v.string(),
  institution: v.string(v.maxLength(255)),
  specialty: v.string(v.maxLength(255)),
  finished: v.string(v.maxLength(4)),
});

const educationForm = toRef(props.item as Education);
</script>

<template>
  <UForm
    :schema="schema"
    :state="educationForm"
    @submit.prevent="emit('update', educationForm)"
  >
    <UFormField label="Тип образования" name="view" required>
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
    <UFormField label="Название учебного заведения" name="institution" required>
      <UInput
        v-model.trim.lazy="educationForm.institution"
        required
        placeholder="Название учебного заведения"
        maxlength="255"
      />
    </UFormField>
    <UFormField label="Год окончания" name="finished">
      <UInput
        v-model.trim.lazy="educationForm.finished"
        placeholder="Год окончания"
        maxlength="4"
      />
    </UFormField>
    <UFormField label="Специальность" name="specialty">
      <UInput
        v-model.trim.lazy="educationForm.specialty"
        placeholder="Специальность"
        maxlength="255"
      />
    </UFormField>
    <UButton label="Принять" color="success" variant="outline" type="submit" />
  </UForm>
</template>
