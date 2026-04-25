<script setup lang="ts">
import { schemaWork } from "@/schema";
import type { Work } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Work>,
    default: () => ({}),
  },
});

const workNow = ref(false);

const form = ref({
  id: props.item.id ?? null,
  starts: props.item.starts || "",
  finished: props.item.finished || "",
  workplace: props.item.workplace || "",
  position: props.item.position || "",
  address: props.item.address || "",
  reason: props.item.reason || "",
});
</script>

<template>
  <UForm
    :state="form"
    :schema="schemaWork"
    @submit.prevent="emit('update', form)"
  >
    <UFormField label="Текущая работа" name="now_work">
      <UCheckbox v-model="workNow" />
    </UFormField>
    <UFormField label="Начало работы" name="starts" required>
      <UInput v-model="form.starts" type="date" required />
    </UFormField>
    <UFormField v-if="!workNow" label="Окончание работы" name="finished">
      <UInput v-model="form.finished" type="date" />
    </UFormField>
    <UFormField label="Место работы" name="workplace" required>
      <UInput v-model.trim.lazy="form.workplace" placeholder="Место работы" />
    </UFormField>
    <UFormField label="Должность" name="position" required>
      <UInput v-model.trim.lazy="form.position" placeholder="Должность" />
    </UFormField>
    <UFormField label="Адрес организации" name="address">
      <UInput
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
    <UButton label="Принять" color="success" variant="outline" type="submit" />
  </UForm>
</template>
