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
  <form
    @submit.prevent="submitContact"
    class="form form-check"
  >
    <ElementsLabelSlot :label="'Вид контакта'">
      <ElementsSelectDiv
        :name="'view'"
        :select="classifyState.classes.value.contacts"
        v-model="contactForm['view']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Контакт'">
      <ElementsInputElement
        :name="'contact'"
        :place="'Контакт'"
        :typeof="view"
        :need="true"
        v-model="contactForm['contact']"
      />
    </ElementsLabelSlot>
    <ElementsBtnGroup @cancel="emit('cancel')"/>
  </form>
</template>
