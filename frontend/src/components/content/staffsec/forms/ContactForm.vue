<script setup lang="ts">
import { defineAsyncComponent, ref, computed } from "vue";
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

const contactForm = ref({
  form: <Contact>{},
  selected_item: {
    phone: "Телефон",
    email: "E-mail",
    other: "Другое",
  }
});

function updateItem() {
  emit("submit", contactForm.value.form);
  Object.keys(contactForm.value.form).forEach((key) => {
    delete contactForm.value.form[key as keyof typeof contactForm.value.form];
  });
};

const view = computed(() => {
  if (contactForm.value.form["view"] === "Телефон") {
    return "tel";
  } else if (contactForm.value.form["view"] === "E-mail") {
    return "email";
  } else {
    return "text";
  }
});
</script>

<template>
  <form
    @submit.prevent="updateItem"
    class="form form-check"
    role="form"
  >
    <SelectDiv
      :name="'view'"
      :label="'Выбрать'"
      :select="contactForm.selected_item"
      :model="props.contact['view']"
      @input-event="contactForm.form['view'] = $event.target.value"
    />
    <InputLabel
      :name="'contact'"
      :label="'Контакт'"
      :typeof="view"
      :need="true"
      :model="props.contact['contact']"
      @input-event="
        contactForm.form['contact'] = $event.target.value
      "
    />
    <BtnGroup>
      <button
        class="btn btn-outline-primary btn-md"
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
