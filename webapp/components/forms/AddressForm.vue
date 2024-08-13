<script setup lang="ts">
import { toRef } from "vue";
import { stateAnketa, stateClassify } from "@/state/state";
import type { Address } from "@/utils/interfaces";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  addrs: {
    type: Object as () => Address,
    default: {} as Address,
  },
});

const anketaState = stateAnketa();
const classifyState = stateClassify();

const addressForm = toRef(props.addrs as Address);

function submitAddress() {
  anketaState.updateItem("addresses", addressForm.value)
  emit('cancel');
  addressForm.value = {} as Address;
}
</script>

<template>
  <UForm :state="addressForm" @submit.prevent="submitAddress">
    <UFormGroup class="mb-3" label="Вид адреса" required>
      <USelect
        v-model="addressForm['view']"
        :options="Object.values(classifyState.classes.value.addresses)"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Адрес" required>
      <UInput
        v-model="addressForm['addresses']"
        placeholder="Адрес"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
