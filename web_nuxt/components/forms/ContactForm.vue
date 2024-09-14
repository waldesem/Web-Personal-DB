<script setup lang="ts">
import { toRef } from "vue";
import { stateClassify } from "@/state/state";
import type { Contact } from "@/types/interfaces";

const emit = defineEmits(["cancel", "submit"]);

const props = defineProps({
  contact: {
    type: Object as () => Contact,
    default: {} as Contact,
  },
});

const classifyState = stateClassify();

const contactForm = toRef(props.contact as Contact);

function submitContact() {
  emit("submit", contactForm.value);
  clearForm();
}

function cancelAction() {
  emit('cancel');
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
        :options="Object.values(classifyState.classes.value.contacts)"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Контакт">
      <UInput
        v-model.trim.lazy="contactForm['contact']"
        required
        placeholder="Контакт"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelAction"/>
  </UForm>
</template>
