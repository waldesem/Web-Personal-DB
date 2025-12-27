<script setup lang="ts">
import type { Inquisition } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Inquisition>,
    default: () => ({}),
  },
});

const form = toRef(props.item);
</script>

<template>
  <UForm :state="form" @submit.prevent="emit('update', form)">
    <UFormField label="Тема проверки" name="theme" required>
      <UInput
        v-model.trim.lazy="form.theme"
        placeholder="Тема проверки"
        maxlength="255"
        required
      />
    </UFormField>
    <UFormField label="Информация" name="info" required>
      <UTextarea
        v-model.trim.lazy="form.info"
        autoresize
        placeholder="Информация"
        required
      />
    </UFormField>
    <ElementSubmitButton />
  </UForm>
</template>
