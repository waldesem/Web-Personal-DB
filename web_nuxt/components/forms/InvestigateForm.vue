<script setup lang="ts">
import type { Inquisition } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  item: {
    type:  Object as PropType<Inquisition>,
    default: () => ({}),
  },
});

const investigationForm = toRef(props.item as Inquisition);
</script>

<template>
  <UForm
    :state="investigationForm"
    @submit.prevent="emit('update', investigationForm)"
  >
    <UFormField label="Тема проверки" name="theme" required>
      <UInput
        v-model.trim.lazy="investigationForm.theme"
        required
        placeholder="Тема проверки"
        maxlength="255"
      />
    </UFormField>
    <UFormField label="Информация" name="info" required>
      <UTextarea
        v-model.trim.lazy="investigationForm.info"
        required
        autoresize
        placeholder="Информация"
      />
    </UFormField>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
