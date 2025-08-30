<script setup lang="ts">
import type { Address } from '@/types';

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Address>,
    default: () => ({}),
  },
});

const addressForm = toRef(props.item);
</script>

<template>
  <UForm :state="addressForm" @submit.prevent="emit('update', addressForm)">
    <UFormField label="Вид адреса" name="view" required>
      <USelect
        v-model="addressForm.view"
        :items="['Адрес регистрации', 'Адрес проживания', 'Другое']"
        placeholder="Выберите вид адреса"
        required
      />
    </UFormField>
    <UFormField label="Адрес" name="address" required>
      <UTextarea
        v-model.trim.lazy="addressForm.address"
        placeholder="Адрес"
        required
      />
    </UFormField>
    <ElementsSubmitButton />
  </UForm>
</template>
