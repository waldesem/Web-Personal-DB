<script setup lang="ts">
import { defineAsyncComponent, computed, toRef } from "vue";
import { Contact } from "@/interfaces";
import { clearForm } from "@/utilities";

const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
)
const SelectArray = defineAsyncComponent(
  () => import("@components/content/elements/SelectArray.vue")
);
const GroupContent = defineAsyncComponent(
  () => import("@components/content/elements/GroupContent.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);

const emit = defineEmits(["submit", "cancel"]);

const props = defineProps({
  contact: {
    type: Object as () => Contact,
    default: {},
  },
});

const contactForm = toRef(props.contact as Contact);

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
    @submit.prevent="emit('submit', contactForm); clearForm(contactForm)"
    class="form form-check"
    role="form"
  >
    <LabelSlot :label="'Вид контакта'">
      <SelectArray
        :name="'view'"
        :select="['Телефон', 'E-mail', 'Другое']"
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
    <BtnGroup>
      <GroupContent
        @cancel="emit('cancel')"
      />
    </BtnGroup>
  </form>
</template>
