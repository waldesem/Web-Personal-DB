<script setup lang="ts">
import type { Contact } from "@/types/interfaces";

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
  <UForm :state="contactForm" @submit.prevent="submitContact">
    <UFormGroup class="mb-3" label="Вид контакта">
      <USelect
        v-model.trim.lazy="contactForm['view']"
        required
        :options="['Телефон', 'Электронная почта', 'Другое']"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Контакт">
      <UInput
        v-model.trim.lazy="contactForm['contact']"
        required
        placeholder="Контакт"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelAction" />
  </UForm>
</template>
