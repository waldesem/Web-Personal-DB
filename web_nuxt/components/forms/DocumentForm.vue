<script setup lang="ts">
import type { Passport } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Passport>,
    default: () => ({}),
  },
});

const docForm = toRef(props.item as Passport);

docForm.value.issue = docForm.value.issue
  ? new Date(docForm.value.issue).toISOString().split("T", 1)[0]
  : "";
</script>

<template>
  <UForm
    :state="docForm"
    @submit.prevent="emit('update', docForm)"
  >
    <UFormField label="Вид документа" name="view" required>
      <USelect
        v-model="docForm.view"
        :items="['Паспорт', 'Иностранный паспорт', 'Другое']"
        placeholder="Выберите вид документа"
      />
    </UFormField>
    <UFormField label="Серия документа" name="series">
      <UInput
        v-model.trim.lazy="docForm.series"
        placeholder="Серия документа"
        maxlength="4"
      />
    </UFormField>
    <UFormField label="Номер документа" name="digits" required>
      <UInput
        v-model.trim.lazy="docForm.digits"
        placeholder="Номер документа"
        maxlength="8"
      />
    </UFormField>
    <UFormField label="Кем выдан" name="agency">
      <UInput
        v-model.trim="docForm.agency"
        placeholder="Кем выдан"
        maxlength="255"
      />
    </UFormField>
    <UFormField label="Дата выдачи" name="issue" required>
      <UInput v-model.trim.lazy="docForm.issue" type="date" />
    </UFormField>
    <UButton label="Принять" color="success" variant="outline" type="submit" />
  </UForm>
</template>
