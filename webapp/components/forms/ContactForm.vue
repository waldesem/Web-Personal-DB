<script setup lang="ts">
import { computed, toRef } from "vue";
import { stateAnketa, stateClassify } from "@/state/state";
import type { Contact } from "@/utils/interfaces";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  contact: {
    type: Object as () => Contact,
    default: <Contact>({}),
  },
});

const anketaState = stateAnketa();
const classifyState = stateClassify();

const contactForm = toRef(props.contact as Contact);

function submitContact() {
  anketaState.updateItem("contacts", contactForm.value)
  emit('cancel');
  Object.keys(contactForm.value).forEach(
    (key) => delete contactForm.value[key as keyof typeof contactForm.value]
  );
}

const view = computed(() => {
  if (contactForm.value["view"] === "Телефон") {
    return "tel";
  } else if (contactForm.value["view"] === "E-mail") {
    return "email";
  } else {
    return "text";
  }
});
</script>

<template>
  <UForm :state="contactForm" @submit.prevent="submitContact">
    <UFormGroup class="mb-3" size="lg" label="Вид контакта" required>
      <USelect
        v-model="contactForm['view']"
        :options="classifyState.classes.value.contacts"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" size="lg" label="Контакт" required>
      <UInput
        v-model="contactForm['contact']"
        placeholder="Контакт"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="emit('cancel')"/>
  </UForm>
</template>
