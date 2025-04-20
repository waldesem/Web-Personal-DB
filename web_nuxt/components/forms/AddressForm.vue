<script setup lang="ts">
import type { Address } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  addrs: {
    type: Object as () => Address,
    default: {} as Address,
  },
});

const addressForm = ref(props.addrs as Address);
</script>

<template>
  <UForm :state="addressForm" @submit.prevent="emit('update', addressForm)">
    <UFormField class="mb-3" label="Вид адреса" name="view" required>
      <USelect
        v-model.trim.lazy="addressForm.view"
        required
        :options="['Адрес регистрации', 'Адрес проживания', 'Другое']"
      />
    </UFormField>
    <UFormField class="mb-3" label="Адрес" name="addresses" required>
      <UTextarea
        v-model.trim.lazy="addressForm.addresses"
        required
        placeholder="Адрес"
      />
    </UFormField>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
