<script setup lang="ts">
import { defineAsyncComponent, ref, computed } from "vue";
import { Contact } from "@/interfaces/interface";

const InputLabel = defineAsyncComponent(
  () => import("@components/elements/InputLabel.vue")
);
const SelectDiv = defineAsyncComponent(
  () => import("@components/elements/SelectDiv.vue")
)
const BtnGroupForm = defineAsyncComponent(
  () => import("@components/elements/BtnGroupForm.vue")
);

const emit = defineEmits(["submit", "cancel"]);

const props = defineProps({
  contact: {
    type: Object as () => Record<string, any>,
    default: () => {},
  },
});

const contactForm = ref({
  form: <Contact>{},
  selected_item: {
    phone: "Телефон",
    email: "E-mail",
    other: "Другое",
  },

  updateItem: function () {
    emit("submit", this.form);
    Object.keys(this.form).forEach((key) => {
      delete this.form[key as keyof typeof this.form];
    });
   },
});

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
    @submit.prevent="contactForm.updateItem"
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
    <BtnGroupForm :cls="false">
      <button
        class="btn btn-outline-success btn-md"
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
      <button 
        class="btn btn-outline-primary btn-md" 
        name="cancel" 
        type="button"
        @click="$emit('cancel')"
      >
        Отмена
      </button>
    </BtnGroupForm>
  </form>
</template>
