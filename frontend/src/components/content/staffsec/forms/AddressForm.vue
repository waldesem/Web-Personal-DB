<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { Address } from "@/interfaces/interface";

const InputLabel = defineAsyncComponent(
  () => import("@components/elements/InputLabel.vue")
);
const TextLabel = defineAsyncComponent(
  () => import("@components/elements/TextLabel.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/elements/BtnGroup.vue")
);
const SelectDiv = defineAsyncComponent(
  () => import("@components/elements/SelectDiv.vue")
);

const emit = defineEmits(["submit"]);

const props = defineProps({
  addrs: {
    type: Object as () => Address,
    default: {},
  },
});

const addressForm = ref({
  form: <Address>{},
  selected_item: {
    registration: "Адрес регистрации",
    live: "Адрес проживания",
    others: "Другое",
  },
});
</script>

<template>
  <form
    @submit.prevent="emit('submit', addressForm.form)"
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
    <BtnGroup :cls="false">
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
