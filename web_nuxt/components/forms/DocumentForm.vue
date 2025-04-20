<script setup lang="ts">
import type { Passport } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  docs: {
    type: Object as () => Passport,
    default: {} as Passport,
  },
});

const docForm = ref(props.docs as Partial<Passport>);
docForm.value.issue = docForm.value.issue
  ? new Date(docForm.value.issue).toISOString().split("T", 1)[0]
  : "";

const validate = (state: Partial<Passport>) => {
  const errors = [];
  if (state.issue && !state.issue.match(/^\d{4}-\d{2}-\d{2}$/)) {
    errors.push({
      path: "issue",
      message: "Поле должно содержать корректную дату",
    });
  }
  return errors;
};
</script>

<template>
  <UForm
    :state="docForm"
    :validate="validate"
    @submit.prevent="emit('update', docForm)"
  >
    <UFormField class="mb-3" label="Вид документа" name="view" required>
      <USelect
        v-model="docForm.view"
        required
        :items="['Паспорт', 'Иностранный паспорт', 'Другое']"
      />
    </UFormField>
    <UFormField class="mb-3" label="Серия документа" name="series">
      <UInput
        v-model.trim.lazy="docForm.series"
        placeholder="Серия документа"
        maxlength="12"
      />
    </UFormField>
    <UFormField class="mb-3" label="Номер документа" name="digits" required>
      <UInput
        v-model.trim.lazy="docForm.digits"
        required
        placeholder="Номер документа"
        maxlength="12"
      />
    </UFormField>
    <UFormField class="mb-3" label="Кем выдан" name="agency">
      <UInput
        v-model.trim="docForm.agency"
        placeholder="Кем выдан"
        maxlength="255"
      />
    </UFormField>
    <UFormField class="mb-3" label="Дата выдачи" name="issue" required>
      <UInput v-model.trim.lazy="docForm.issue" required type="date" />
    </UFormField>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
