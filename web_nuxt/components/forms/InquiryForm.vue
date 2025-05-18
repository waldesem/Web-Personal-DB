<script setup lang="ts">
import type { Needs } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  item: {
    type: Object as () => Needs,
    default: () => ({}),
  },
});

const inquiryForm = toRef(props.item);
</script>

<template>
  <UForm :state="inquiryForm" @submit.prevent="emit('update', inquiryForm)">
    <UFormField label="Информация" name="info" required>
      <UTextarea
        v-model.trim.lazy="inquiryForm.info"
        required
        autoresize
        placeholder="Информация"
      />
    </UFormField>
    <UFormField label="Инициатор" name="initiator" required>
      <UInput
        v-model.trim.lazy="inquiryForm.initiator"
        required
        placeholder="Инициатор"
        maxlength="255"
      />
    </UFormField>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
