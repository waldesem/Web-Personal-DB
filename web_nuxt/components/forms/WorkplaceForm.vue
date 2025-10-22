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

const workForm = toRef(props.item);

// Преобразование даты в формат YYYY-MM-DD для корректного отображения в форме
const starts = useDateFormat(workForm.value.starts, "YYYY-MM-DD");
const finished = useDateFormat(workForm.value.finished, "YYYY-MM-DD");
</script>

<template>
  <UForm :state="workForm" @submit.prevent="emit('update', workForm)">
    <UFormField label="Текущая работа" name="now_work">
      <UCheckbox v-model="workForm.now_work" />
    </UFormField>
    <UFormField
      v-if="!workForm.now_work"
      label="Начало работы"
      name="starts"
      required
    >
      <UInput
        :value="starts"
        type="date"
        required
        @input="workForm.starts = $event.target.value"
      />
    </UFormField>
    <UFormField label="Окончание работы" name="finished" required>
      <UInput
        :value="finished"
        type="date"
        required
        @input="workForm.finished = $event.target.value"
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
    <UButton label="Принять" color="success" variant="outline" type="submit" />
  </UForm>
</template>
