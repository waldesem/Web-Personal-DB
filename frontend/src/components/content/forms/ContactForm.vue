<script setup lang="ts">
import { defineAsyncComponent, computed } from "vue";
import { Contact } from "@/interfaces/interface";

const InputLabel = defineAsyncComponent(
  () => import("@components/content/elements/InputLabel.vue")
);
const SelectArray = defineAsyncComponent(
  () => import("@components/content/elements/SelectArray.vue")
)
const BtnGroupContent = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroupContent.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);

const emit = defineEmits(["submit"]);

const props = defineProps({
  contact: {
    type: Object as () => Contact,
    default: {},
  },
});

const contactForm = computed(() => {
  return props.contact as Contact;
});

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
    @submit.prevent="emit('submit', contactForm)"
    class="form form-check"
    role="form"
  >
    <SelectArray
      :name="'view'"
      :label="'Выбрать'"
      :select="['Телефон', 'E-mail', 'Другое']"
      v-model="contactForm['view']"
    />
    <InputLabel
      :name="'contact'"
      :label="'Контакт'"
      :typeof="view"
      :need="true"
      v-model="contactForm['contact']"
    />
    <BtnGroup>
      <BtnGroupContent/>
    </BtnGroup>
  </form>
</template>
