<script setup lang="ts">
import { defineAsyncComponent, computed } from "vue";
import { Contact } from "@/interfaces/interface";

const InputLabel = defineAsyncComponent(
  () => import("@components/elements/InputLabel.vue")
);
const SelectDiv = defineAsyncComponent(
  () => import("@components/elements/SelectDiv.vue")
)
const BtnGroup = defineAsyncComponent(
  () => import("@components/elements/BtnGroup.vue")
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
const selected_item = {
  phone: "Телефон",
  email: "E-mail",
  other: "Другое",
};

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
    <SelectDiv
      :name="'view'"
      :label="'Выбрать'"
      :select="selected_item"
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
      <button
        class="btn btn-outline-primary btn-md"
        data-bs-dismiss="modal"
        name="submit"
        type="submit"
      >
        Принять
      </button>
      <button 
        class="btn btn-outline-secondary btn-md" 
        name="reset" 
        type="reset"
      >
        Очистить
      </button>
    </BtnGroup>
  </form>
</template>
