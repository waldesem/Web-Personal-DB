<script setup lang="ts">
import type { Education } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Education>,
    default: () => ({}),
  },
});

const form = toRef(props.item);
</script>

<template>
  <UForm :state="form" @submit.prevent="emit('update', form)">
    <UFormField label="Тип образования" name="view" required>
      <USelect
        v-model="form.view"
        :items="[
          'Основное общее',
          'Среднее общее',
          'Среднее профессиональное',
          'Высшее',
          'Неоконченное высшее образование',
          'Другое образование',
        ]"
        placeholder="Выберите тип образования"
        required
      />
    </UFormField>
    <UFormField label="Название учебного заведения" name="institution" required>
      <UInput
        v-model.trim.lazy="form.institution"
        placeholder="Название учебного заведения"
        maxlength="255"
        required
      />
    </UFormField>
    <UFormField label="Год окончания" name="finished">
      <UInput v-model.trim.lazy="form.finished" placeholder="Год окончания" maxlength="4" />
    </UFormField>
    <UFormField label="Специальность" name="specialty">
      <UInput v-model.trim.lazy="form.specialty" placeholder="Специальность" maxlength="255" />
    </UFormField>
    <ElementSubmitButton />
  </UForm>
</template>
