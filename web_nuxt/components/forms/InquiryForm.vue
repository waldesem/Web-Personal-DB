<script setup lang="ts">
import { z } from "zod";
import type { Needs } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  inquiry: {
    type: Object as () => Needs,
    default: {} as Needs,
  },
});

const inquiryForm = ref(props.inquiry);

const schema = z.object({
  info: z.string({ required_error: "Обязательное поле" }),
  initiator: z
    .string({ required_error: "Обязательное поле" })
    .max(255, "Максимум 255 символов"),
});
</script>

<template>
  <UForm
    :state="inquiryForm"
    :schema="schema"
    @submit.prevent="emit('update', inquiryForm)"
  >
    <UFormGroup class="mb-3" label="Информация" name="info" required>
      <UTextarea
        v-model.trim.lazy="inquiryForm['info']"
        required
        autoresize
        placeholder="Информация"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Инициатор" name="initiator" required>
      <UInput
        v-model.trim.lazy="inquiryForm['initiator']"
        required
        placeholder="Инициатор"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
