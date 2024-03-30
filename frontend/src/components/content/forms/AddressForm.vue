<script setup lang="ts">
import { defineAsyncComponent, computed } from "vue";
import { Address } from "@/interfaces/interface";

const InputLabel = defineAsyncComponent(
  () => import("@components/content/elements/InputLabel.vue")
);
const SelectArray = defineAsyncComponent(
  () => import("@components/content/elements/SelectArray.vue")
);
const BtnGroupContent = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroupContent.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
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
</script>

<template>
  <form
    @submit.prevent="emit('submit', addressForm)"
    class="form form-check"
    role="form"
  >
    <SelectArray
      :name="''"
      :label="''"
      :select="['Адрес регистрации', 'Адрес проживания', 'Другое']"
      v-model="addressForm['view']"
    />
    <InputLabel
      :name="'region'"
      :label="'Регион'"
      :need="true"
      v-model="addressForm['region']"
    />
    <InputLabel
      :name="'address'"
      :label="'Адрес'"
      :need="true"
      v-model="addressForm['address']"
    />
    <BtnGroup>
      <BtnGroupContent/>
    </BtnGroup>
  </form>
</template>
