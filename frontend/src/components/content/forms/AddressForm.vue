<script setup lang="ts">
import { defineAsyncComponent, toRef } from "vue";
import { Address } from "@/interfaces";
import { stateClassify, stateAnketa } from "@/state";

const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
)
const SelectDiv = defineAsyncComponent(
  () => import("@components/content/elements/SelectDiv.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);

const emit = defineEmits(["cancel"]);

const props = defineProps({
  addrs: {
    type: Object as () => Address,
    default: {},
  },
});

const addressForm = toRef(props.addrs as Address);

function submitAddress() {
  stateAnketa.updateItem("addresses", addressForm.value)
  emit('cancel');
  Object.keys(addressForm.value).forEach(
    (key) => delete addressForm.value[key as keyof typeof addressForm.value]
  );
}
</script>

<template>
  <form
    @submit.prevent="submitAddress"
    class="form form-check"
    role="form"
  >
    <LabelSlot :label="'Вид адреса'">
      <SelectDiv
        :name="'view'"
        :select="stateClassify.addresses"
        v-model="addressForm['view']"
      />
    </LabelSlot>
    <LabelSlot
      :label="'Адрес'"
    >
      <InputElement
        :name="'address'"
        :place="'Адрес'"
        :need="true"
        v-model="addressForm['address']"
      />
    </LabelSlot>
    <BtnGroup @cancel="emit('cancel')"/>
  </form>
</template>
