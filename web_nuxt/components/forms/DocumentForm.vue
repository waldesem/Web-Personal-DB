<script setup lang="ts">
import type { Document } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  docs: {
    type: Object as () => Document,
    default: {} as Document,
  },
});

const docForm = ref(props.docs as Document);
docForm.value.issue = docForm.value.issue
  ? new Date(docForm.value.issue).toISOString().split("T", 1)[0]
  : "";

const validate = (state: Document) => {
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
    <UFormGroup class="mb-3" label="Вид документа" name="view" required>
      <USelect
        v-model="docForm['view']"
        required
        :options="['Паспорт', 'Иностранный паспорт', 'Другое']"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Серия документа" name="series">
      <UInput
        v-model.trim.lazy="docForm['series']"
        placeholder="Серия документа"
        maxlength="12"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Номер документа" name="digits" required>
      <UInput
        v-model.trim.lazy="docForm['digits']"
        required
        placeholder="Номер документа"
        maxlength="12"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Кем выдан" name="agency">
      <UInput
        v-model.trim="docForm['agency']"
        placeholder="Кем выдан"
        maxlength="255"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Дата выдачи" name="issue" required>
      <UInput v-model.trim.lazy="docForm['issue']" required type="date" />
    </UFormGroup>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
