<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { Address } from "@/interfaces/interface";

const InputLabel = defineAsyncComponent(
  () => import("@components/elements/InputLabel.vue")
);
const TextLabel = defineAsyncComponent(
  () => import("@components/elements/TextLabel.vue")
);
const BtnGroupForm = defineAsyncComponent(
  () => import("@components/elements/BtnGroupForm.vue")
);

const emit = defineEmits(["submit", "cancel"]);

const props = defineProps({
  addrs: {
    type: Object as () => Record<string, any>,
    default: () => {},
  },
});

const addressForm = ref({
  form: <Address>{},
  selected_item: {
    registration: "Адрес регистрации",
    live: "Адрес проживания",
    others: "Другое",
  },

  updateItem: function () {
    emit("submit", this.form);
    Object.keys(this.form).forEach((key) => {
      delete this.form[key as keyof typeof this.form];
    });
   },
});
</script>

<template>
  <form
    @submit.prevent="addressForm.updateItem"
    class="form form-check"
    role="form"
  >
    <SelectDiv
      :name="''"
      :label="''"
      :select="addressForm.selected_item"
      :model="props.addrs['view']"
      @input-event="addressForm.form['view'] = $event.target.value"
    />
    <InputLabel
      :name="'region'"
      :label="'Регион'"
      :need="true"
      :model="props.addrs['region']"
      @input-event="
        addressForm.form['region'] = $event.target.value
      "
    />
    <TextLabel
      :name="'address'"
      :label="'Полный адрес'"
      :model="props.addrs['address']"
      @input-event="
        addressForm.form['address'] = $event.target.value
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
