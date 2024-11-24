<script setup lang="ts">
import { z } from "zod";
import type { Contact } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  contact: {
    type: Object as () => Contact,
    default: {} as Contact,
  },
  candId: {
    type: String,
    default: "",
  },
});

const schema = z.object({
  view: z
    .string({ required_error: "Обязательное поле" })
    .max(255, "Максимум 255 символов"),
  contact: z
    .string({ required_error: "Обязательное поле" })
    .max(255, "Максимум 255 символов"),
});

const contactForm = toRef(props.contact as Contact);

function submitContact() {
  emit("update", contactForm.value);
  clearForm();
}

function cancelAction() {
  emit("cancel");
  clearForm();
}

function clearForm() {
  Object.assign(contactForm.value, {
    view: "",
    contact: "",
  } as Contact);
}
</script>

<template>
  <UForm :state="contactForm" :schema="schema" @submit.prevent="submitContact">
    <UFormGroup class="mb-3" label="Вид контакта" name="view" required>
      <USelect
        v-model.trim.lazy="contactForm['view']"
        required
        :options="['Телефон', 'Электронная почта', 'Другое']"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Контакт" name="contact" required>
      <UInput
        v-model.trim.lazy="contactForm['contact']"
        required
        placeholder="Контакт"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelAction" />
  </UForm>
</template>
