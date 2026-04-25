<script setup lang="ts">
import type { Passport } from "@/types";
import { schemaDoc } from "@/schema";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Passport>,
    default: () => ({}),
  },
});

const form = ref({
  id: props.item.id ?? null,
  view: props.item.view || "",
  series: props.item.series || "",
  digits: props.item.digits || "",
  agency: props.item.agency || "",
  issue: props.item.issue || "",
});
</script>

<template>
  <UForm
    :state="form"
    :schema="schemaDoc"
    @submit.prevent="emit('update', form)"
  >
    <UFormField label="Вид документа" name="view" required>
      <USelect
        v-model="form.view"
        :items="['Паспорт', 'Иностранный паспорт', 'Другое']"
        placeholder="Выберите вид документа"
      />
    </UFormField>
    <UFormField label="Серия документа" name="series">
      <UInput
        v-model.trim.lazy="form.series"
        placeholder="Серия документа"
        maxlength="12"
      />
    </UFormField>
    <UFormField label="Номер документа" name="digits" required>
      <UInput
        v-model.trim.lazy="form.digits"
        placeholder="Номер документа"
        maxlength="12"
        required
      />
    </UFormField>
    <UFormField label="Кем выдан" name="agency">
      <UInput
        v-model.trim="form.agency"
        placeholder="Кем выдан"
        maxlength="255"
      />
    </UFormField>
    <UFormField label="Дата выдачи" name="issue" required>
      <UInput
        v-model="form.issue"
        type="date"
        :max="new Date().toISOString().split('T')[0]"
        min="1990-01-01"
        required
      />
    </UFormField>
    <UButton label="Принять" color="success" variant="outline" type="submit" />
  </UForm>
</template>
