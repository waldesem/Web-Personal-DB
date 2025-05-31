<script setup lang="ts">
import type { Inquisition } from "@/types";
import * as v from "valibot";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Inquisition>,
    default: () => ({}),
  },
});

const schema = v.object({
  theme: v.pipe(v.string(), v.maxLength(255, "Максимальная длина 255 символов")),
  info: v.string(),
});

const investigationForm = toRef(props.item as Inquisition);
</script>

<template>
  <UForm
    :schema="schema"
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
    <UButton label="Принять" color="success" variant="outline" type="submit" />
  </UForm>
</template>
