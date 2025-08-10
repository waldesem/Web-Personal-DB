<script setup lang="ts">
import type { Work } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Work>,
    default: () => ({}),
  },
});

const workForm = toRef(props.item as Work);

workForm.value.starts =
  new Date(workForm.value.starts).toISOString().split("T", 1)[0] ?? "";
workForm.value.finished =
  new Date(workForm.value.finished).toISOString().split("T", 1)[0] ?? "";
</script>

<template>
  <UForm :state="workForm" @submit.prevent="emit('update', workForm)">
    <UFormField label="Текущая работа" name="now_work">
      <UCheckbox v-model="workForm.now_work" />
    </UFormField>
    <UFormField label="Начало работы" name="starts" required>
      <UInput
        v-model="workForm.starts"
        placeholder="Начало работы"
        type="date"
        required
      />
    </UFormField>
    <UFormField label="Окончание работы" name="finished" required>
      <UInput
        v-model="workForm.finished"
        placeholder="Окончание работы"
        type="date"
        required
      />
    </UFormField>
    <UFormField label="Место работы" name="workplace" required>
      <UInput
        v-model.trim.lazy="workForm.workplace"
        placeholder="Место работы"
        maxlength="255"
        required
      />
    </UFormField>
    <UFormField label="Должность" name="position" required>
      <UInput
        v-model.trim.lazy="workForm.position"
        placeholder="Должность"
        maxlength="255"
        required
      />
    </UFormField>
    <UFormField label="Адрес организации" name="address">
      <UTextarea
        v-model.trim.lazy="workForm.address"
        placeholder="Адрес организации"
      />
    </UFormField>
    <UFormField label="Причина увольнения" name="reason">
      <UTextarea
        v-model.trim.lazy="workForm.reason"
        placeholder="Причина увольнения"
      />
    </UFormField>
    <ElementsSubmitButton />
  </UForm>
</template>
