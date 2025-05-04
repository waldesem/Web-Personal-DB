<script setup lang="ts">
import type { Address } from "@/types";

const emit = defineEmits(["cancel", "update", 'clear']);

const props = defineProps({
  item: {
    type: Object as () => Address,
    default: {} as Address,
  },
});

const addressForm = ref(props.item as Address);
</script>

<template>
  <UForm :state="addressForm" @submit.prevent="emit('update', addressForm)">
    <UFormField class="mb-3" label="Вид адреса" name="view" required>
      <USelect
        v-model="addressForm.view"
        required
        :items="['Адрес регистрации', 'Адрес проживания', 'Другое']"
        placeholder="Выберите вид адреса"
      />
    </UFormField>
    <UFormField class="mb-3" label="Адрес" name="addresses" required>
      <UTextarea
        v-model.trim.lazy="addressForm.addresses"
        required
        placeholder="Адрес"
      />
    </UFormField>
    <ElementsBtnGroup @cancel="emit('cancel')" @clear="emit('clear')" />
  </UForm>
</template>
