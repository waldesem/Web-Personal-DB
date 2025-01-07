<script setup lang="ts">
import type { Inquisition } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  investigation: {
    type: Object as () => Inquisition,
    default: {} as Inquisition,
  },
});

const investigationForm = ref(props.investigation as Inquisition);
</script>

<template>
  <UForm
    :state="investigationForm"
    @submit.prevent="emit('update', investigationForm)"
  >
    <UFormGroup class="mb-3" label="Тема проверки" name="theme" required>
      <UInput
        v-model.trim.lazy="investigationForm.theme"
        required
        placeholder="Тема проверки"
        maxlength="255"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Информация" name="info" required>
      <UTextarea
        v-model.trim.lazy="investigationForm.info"
        required
        autoresize
        placeholder="Информация"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
