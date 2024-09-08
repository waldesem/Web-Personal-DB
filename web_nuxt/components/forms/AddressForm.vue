<script setup lang="ts">
import { toRef } from "vue";
import { stateClassify } from "@/state/state";
import type { Address } from "@/utils/interfaces";

const emit = defineEmits(["cancel", "submit"]);

const props = defineProps({
  addrs: {
    type: Object as () => Address,
    default: {} as Address,
  },
});

const classifyState = stateClassify();

const addressForm = toRef(props.addrs as Address);

function submitAddress() {
  emit("submit", addressForm.value)
  clearForm();
}

function cancelAction() {
  emit('cancel');
  clearForm();
}

function clearForm() {
  Object.assign(addressForm.value, {
    view: "",
    addresses: "",
  } as Address);
}
</script>

<template>
  <UForm :state="addressForm" @submit.prevent="submitAddress">
    <UFormGroup class="mb-3" label="Вид адреса">
      <USelect
        v-model.trim.lazy="addressForm['view']"
        required
        :options="Object.values(classifyState.classes.value.addresses)"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Адрес">
      <UInput
        v-model.trim.lazy="addressForm['addresses']"
        required
        placeholder="Адрес"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelAction" />
  </UForm>
</template>
