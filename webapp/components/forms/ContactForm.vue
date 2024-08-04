<script setup lang="ts">
import { defineAsyncComponent, computed, toRef } from "vue";
import { Contact } from "@/interfaces";
import { stateClassify, stateAnketa } from "@/state";

const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
)
const SelectDiv = defineAsyncComponent(
  () => import("@components/content/elements/SelectDiv.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);

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
    <LabelSlot :label="'Вид контакта'">
      <SelectDiv
        :name="'view'"
        :select="stateClassify.classes.contacts"
        v-model="contactForm['view']"
      />
    </LabelSlot>
    <LabelSlot :label="'Контакт'">
      <InputElement
        :name="'contact'"
        :place="'Контакт'"
        :typeof="view"
        :need="true"
        v-model="contactForm['contact']"
      />
    </LabelSlot>
    <BtnGroup @cancel="emit('cancel')"/>
  </form>
</template>
