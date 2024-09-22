<script setup lang="ts">
import type { Address } from "@/types/interfaces";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  addrs: {
    type: Object as () => Address,
    default: {} as Address,
  },
  candId: {
    type: String,
    default: "",
  },
});

const addressForm = toRef(props.addrs as Address);

function submitAddress() {
  emit("update", addressForm.value);
  clearForm();
}

function cancelAction() {
  emit("cancel");
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
        :options="['Адрес регистрации', 'Адрес проживания', 'Другое']"
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
