<script setup lang="ts">
import { defineAsyncComponent, computed } from "vue";
import { Address } from "@/interfaces/interface";

const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
)
const SelectInput = defineAsyncComponent(
  () => import("@components/content/elements/SelectInput.vue")
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
    <LabelSlot :label="'Вид адреса'">
      <SelectInput
        :name="'view'"
        :select="['Адрес регистрации', 'Адрес проживания', 'Другое']"
        v-model="addressForm['view']"
      />
    </LabelSlot>
    <InputElement
      :name="'region'"
      :label="'Регион'"
      :need="true"
      v-model="addressForm['region']"
    />
    <InputElement
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
