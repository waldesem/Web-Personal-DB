<script setup lang="ts">
import { toRef } from "vue";
import { stateAnketa, stateClassify } from "@/state/state";
import type { Contact } from "@/utils/interfaces";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  contact: {
    type: Object as () => Contact,
    default: {} as Contact,
  },
});

const anketaState = stateAnketa();
const classifyState = stateClassify();

const contactForm = toRef(props.contact as Contact);

function submitContact() {
  anketaState.updateItem("contacts", contactForm.value)
  emit('cancel');
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
        v-model="contactForm['view']"
        required
        :options="Object.values(classifyState.classes.value.contacts)"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Контакт">
      <UInput
        v-model="contactForm['contact']"
        required
        placeholder="Контакт"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="emit('cancel')"/>
  </UForm>
</template>
