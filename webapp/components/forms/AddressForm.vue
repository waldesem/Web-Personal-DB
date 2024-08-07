<script setup lang="ts">
import { toRef } from "vue";
import { stateAnketa, stateClassify } from "@/state/state";
import type { Address } from "@/utils/interfaces";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  addrs: {
    type: Object as () => Address,
    default: {},
  },
});

const anketaState = stateAnketa();
const classifyState = stateClassify();

const addressForm = toRef(props.addrs as Address);

function submitAddress() {
  anketaState.updateItem("addresses", addressForm.value)
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
        :select="classifyState.classes.value.addresses"
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
