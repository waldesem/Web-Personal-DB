<script setup lang="ts">
import { computed, toRef } from "vue";
import type { Contact } from "@/utils/interfaces";
import { stateClassify, stateAnketa } from "@/utils/state";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  contact: {
    type: Object as () => Contact,
    default: {},
  },
});

const contactForm = toRef(props.contact as Contact);

function submitContact() {
  stateAnketa.updateItem("contacts", contactForm.value)
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
    role="form"
  >
    <ElementsLabelSlot :label="'Вид контакта'">
      <ElementsSelectDiv
        :name="'view'"
        :select="stateClassify.classes.contacts"
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
