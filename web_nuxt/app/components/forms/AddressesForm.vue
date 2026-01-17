<script setup lang="ts">
import type { Address } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Address>,
    default: () => ({}),
  },
});

const form = toRef(props.item);
</script>

<template>
  <UForm :state="form" @submit.prevent="emit('update', form)">
    <UFormField label="Вид адреса" name="view" required>
      <USelect
        v-model="form.view"
        :items="['Адрес регистрации', 'Адрес проживания', 'Другое']"
        placeholder="Выберите вид адреса"
        required
      />
    </UFormField>
    <UFormField label="Адрес" name="address" required>
      <UTextarea
        v-model.trim.lazy="form.address"
        placeholder="Адрес"
        required
      />
    </UFormField>
    <ElementSubmitButton />
  </UForm>
</template>
