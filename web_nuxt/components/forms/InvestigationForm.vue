<script setup lang="ts">
import { z } from "zod";
import type { Inquisition } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  investigation: {
    type: Object as () => Inquisition,
    default: {} as Inquisition,
  },
});

const investigationForm = ref(props.investigation as Inquisition);

const schema = z.object({
  theme: z
    .string({ required_error: "Обязательное поле" })
    .max(255, "Максимум 255 символов"),
  info: z.string({ required_error: "Обязательное поле" }),
});
</script>

<template>
  <UForm
    :state="investigationForm"
    :schema="schema"
    @submit.prevent="emit('update', investigationForm)"
  >
    <UFormGroup class="mb-3" label="Тема проверки" name="theme" required>
      <UInput
        v-model.trim.lazy="investigationForm['theme']"
        required
        placeholder="Тема проверки"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Информация" name="info" required>
      <UTextarea
        v-model.trim.lazy="investigationForm['info']"
        required
        autoresize
        placeholder="Информация"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
