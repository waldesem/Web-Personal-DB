<script setup lang="ts">
import type { Work } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  item: {
    type: Object as () => Work,
    default: () => ({}),
  },
});

const workForm = toRef(props.item as Work);

workForm.value.starts = workForm.value.starts
  ? new Date(workForm.value.starts).toISOString().split("T", 1)[0]
  : "";
workForm.value.finished = workForm.value.finished
  ? new Date(workForm.value.finished).toISOString().split("T", 1)[0]
  : "";

const validate = (state: Partial<Work>) => {
  const errors = [];
  if (state.starts && !state.starts.match(/^\d{4}-\d{2}-\d{2}$/)) {
    errors.push({
      path: "issue",
      message: "Поле должно содержать корректную дату",
    });
  }
  if (state.finished && !state.finished.match(/^\d{4}-\d{2}-\d{2}$/)) {
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
    :state="workForm"
    :validate="validate"
    @submit.prevent="emit('update', workForm)"
  >
    <UFormField label="Текущая работа" name="now_work">
      <UCheckbox v-model="workForm.now_work" />
    </UFormField>
    <UFormField label="Начало работы" name="starts" required>
      <UInput
        v-model="workForm.starts"
        required
        placeholder="Начало работы"
        type="date"
      />
    </UFormField>
    <UFormField label="Окончание работы" name="finished" required>
      <UInput
        v-model="workForm.finished"
        required
        placeholder="Окончание работы"
        type="date"
      />
    </UFormField>
    <UFormField label="Место работы" name="workplace" required>
      <UInput
        v-model.trim.lazy="workForm.workplace"
        required
        placeholder="Место работы"
        maxlength="255"
      />
    </UFormField>
    <UFormField label="Должность" name="position" required>
      <UInput
        v-model.trim.lazy="workForm.position"
        required
        placeholder="Должность"
        maxlength="255"
      />
    </UFormField>
    <UFormField label="Адрес организации" name="addresses">
      <UTextarea
        v-model.trim.lazy="workForm.addresses"
        placeholder="Адрес организации"
      />
    </UFormField>
    <UFormField label="Причина увольнения" name="reason">
      <UTextarea
        v-model.trim.lazy="workForm.reason"
        placeholder="Причина увольнения"
      />
    </UFormField>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
