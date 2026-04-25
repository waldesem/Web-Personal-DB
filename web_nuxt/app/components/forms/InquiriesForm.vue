<script setup lang="ts">
import type { Needs } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Needs>,
    default: () => ({}),
  },
});

const form = toRef(props.item);
</script>

<template>
  <UForm :state="form" @submit.prevent="emit('update', form)">
    <UFormField label="Информация" name="info" required>
      <UTextarea
        v-model.trim.lazy="form.info"
        autoresize
        placeholder="Информация"
        required
        maxlength="4096"
      />
    </UFormField>
    <UFormField label="Инициатор" name="initiator" required>
      <UInput
        v-model.trim.lazy="form.initiator"
        placeholder="Инициатор"
        maxlength="255"
        required
      />
    </UFormField>
    <UButton label="Принять" color="success" variant="outline" type="submit" />
  </UForm>
</template>
