<script setup lang="ts">
import { z } from "zod";
import type { Needs } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  inquiry: {
    type: Object as () => Needs,
    default: {} as Needs,
  },
  candId: {
    type: String,
    default: "",
  },
});

const schema = z.object({
  info: z.string({ required_error: "Обязательное поле" }),
  initiator: z
    .string({ required_error: "Обязательное поле" })
    .max(255, "Максимум 255 символов"),
});

const inquiryForm = toRef(props.inquiry as Needs);

function submitIquiry() {
  emit("update", inquiryForm.value);
  clearForm();
}

function cancelAction() {
  emit("cancel");
  clearForm();
}

function clearForm() {
  Object.assign(inquiryForm.value, {
    info: "",
    initiator: "",
  } as Needs);
}
</script>

<template>
  <UForm :state="inquiryForm" :schema="schema" @submit.prevent="submitIquiry">
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
    <ElementsBtnGroup @cancel="cancelAction" />
  </UForm>
</template>
