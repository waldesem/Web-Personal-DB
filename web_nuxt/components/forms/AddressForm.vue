<script setup lang="ts">
import { z } from "zod";
import type { Address } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  addrs: {
    type: Object as () => Address,
    default: {} as Address,
  },
});

const schema = z.object({
  view: z
    .string({ required_error: "Обязательное поле" }),
  addresses: z
    .string({ required_error: "Обязательное поле" })
    .max(255, "Максимум 255 символов"),
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
  <UForm :state="addressForm" :schema="schema" @submit.prevent="submitAddress">
    <UFormGroup class="mb-3" label="Вид адреса" name="view" required>
      <USelect
        v-model.trim.lazy="addressForm['view']"
        required
        :options="['Адрес регистрации', 'Адрес проживания', 'Другое']"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Адрес" name="addresses" required>
      <UInput
        v-model.trim.lazy="addressForm['addresses']"
        required
        placeholder="Адрес"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelAction" />
  </UForm>
</template>
