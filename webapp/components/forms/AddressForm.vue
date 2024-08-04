<script setup lang="ts">
import { toRef } from "vue";
import type { Address } from "../../utils/interfaces";
import { stateClassify, stateAnketa } from "../../utils/state";

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
    <ElementsLabelSlot :label="'Вид адреса'">
      <ElementsSelectDiv
        :name="'view'"
        :select="stateClassify.classes.addresses"
        v-model="addressForm['view']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot
      :label="'Адрес'"
    >
      <ElementsInputElement
        :name="'address'"
        :place="'Адрес'"
        :need="true"
        v-model="addressForm['addresses']"
      />
    </ElementsLabelSlot>
    <ElementsBtnGroup @cancel="emit('cancel')"/>
  </form>
</template>
