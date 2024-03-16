<script setup lang="ts">
import { defineAsyncComponent, computed } from "vue";
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

const addressForm = computed(() => {
  return props.addrs as Address;
});

const selected_item = {
  registration: "Адрес регистрации",
  live: "Адрес проживания",
  others: "Другое",
};
</script>

<template>
  <form
    @submit.prevent="emit('submit', addressForm)"
    class="form form-check"
    role="form"
  >
    <SelectDiv
      :name="''"
      :label="''"
      :select="selected_item"
      v-model="addressForm['view']"
    />
    <InputLabel
      :name="'region'"
      :label="'Регион'"
      :need="true"
      v-model="addressForm['region']"
    />
    <TextLabel
      :name="'address'"
      :label="'Полный адрес'"
      v-model="addressForm['address']"
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
