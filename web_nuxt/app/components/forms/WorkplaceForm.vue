<script setup lang="ts">
import { useDateFormat } from "@vueuse/core";
import type { Work } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Work>,
    default: () => ({}),
  },
});

const form = toRef(props.item);

// Преобразование даты в формат YYYY-MM-DD для корректного отображения в форме
form.value.starts = form.value.starts
  ? useDateFormat(form.value.starts, "YYYY-MM-DD").value
  : "";
form.value.finished = form.value.finished
  ? useDateFormat(form.value.finished, "YYYY-MM-DD").value
  : "";
</script>

<template>
  <UForm :state="form" @submit.prevent="emit('update', form)">
    <UFormField label="Текущая работа" name="now_work">
      <UCheckbox v-model="form.now_work" />
    </UFormField>
    <UFormField
      v-if="!form.now_work"
      label="Начало работы"
      name="starts"
      required
    >
      <UInput
        v-model="form.starts"
        type="date"
        required
      />
    </UFormField>
    <UFormField label="Окончание работы" name="finished" required>
      <UInput
        v-model="form.finished"
        type="date"
        required
      />
    </UFormField>
    <UFormField label="Место работы" name="workplace" required>
      <UInput
        v-model.trim.lazy="form.workplace"
        placeholder="Место работы"
        maxlength="255"
        required
      />
    </UFormField>
    <UFormField label="Должность" name="position" required>
      <UInput
        v-model.trim.lazy="form.position"
        placeholder="Должность"
        maxlength="255"
        required
      />
    </UFormField>
    <UFormField label="Адрес организации" name="address">
      <UTextarea
        v-model.trim.lazy="form.address"
        placeholder="Адрес организации"
      />
    </UFormField>
    <UFormField label="Причина увольнения" name="reason">
      <UTextarea
        v-model.trim.lazy="form.reason"
        placeholder="Причина увольнения"
      />
    </UFormField>
    <ElementsSubmitButton />
  </UForm>
</template>
