<script setup lang="ts">
import type { Work } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Work>,
    default: () => ({}),
  },
});

const form = toRef(props.item);

const workNow = ref(false);

// Преобразование даты в формат YYYY-MM-DD для корректного отображения в форме
form.value.starts = form.value.starts
  ? new Date(form.value.starts).toLocaleDateString()
  : "";
form.value.finished = form.value.finished
  ? new Date(form.value.finished).toLocaleDateString()
  : "";
</script>

<template>
  <UForm :state="form" @submit.prevent="emit('update', form)">
    <UFormField label="Текущая работа" name="now_work">
      <UCheckbox v-model="workNow" />
    </UFormField>
    <UFormField label="Начало работы" name="starts" required>
      <UInput
        v-model="form.starts"
        type="date"
        :max="new Date().toISOString().split('T')[0]"
        min="1900-01-01"
        required
      />
    </UFormField>
    <UFormField v-if="!workNow" label="Окончание работы" name="finished">
      <UInput v-model="form.finished" type="date" />
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
    <ElementSubmitButton />
  </UForm>
</template>
