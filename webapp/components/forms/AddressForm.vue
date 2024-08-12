<script setup lang="ts">
import { toRef } from "vue";
import { stateAnketa, stateClassify } from "@/state/state";
import type { Address } from "@/utils/interfaces";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  addrs: {
    type: Object as () => Address,
    default: <Address>({}),
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
  <UForm :state="addressForm" @submit.prevent="submitAddress">
    <UFormGroup class="mb-3" size="lg" label="Вид адреса">
      <USelect
        v-model="addressForm['view']"
        :options="classifyState.classes.value.addresses"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" size="lg" label="Адрес" required>
      <UInput
        v-model="addressForm['addresses']"
        placeholder="Адрес"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
