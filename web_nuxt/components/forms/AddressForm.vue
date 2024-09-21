<script setup lang="ts">
import type { Address } from "@/types/interfaces";
import { useFetchAuth } from "@/utils/auth";

const toast = useToast();

const authFetch = useFetchAuth();

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

async function submitAddress() {
  emit("cancel");
  await authFetch("/api/addresses/" + props.candId, {
    method: "POST",
    body: addressForm.value,
  });
  toast.add({
    icon: "i-heroicons-check-circle",
    title: "Успешно",
    description: "Информация обновлена",
    color: "green",
  });
  emit("update");
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
