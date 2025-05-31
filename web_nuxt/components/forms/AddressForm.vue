<script setup lang="ts">
import type { Address } from "@/types";
import * as v from "valibot";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Address>,
    default: () => ({}),
  },
});

const schema = v.object({
  view: v.string(),
  addresses: v.string(),
});

const addressForm = toRef(props.item as Address);
</script>

<template>
  <UForm :schema="schema" :state="addressForm" @submit.prevent="emit('update', addressForm)">
    <UFormField label="Вид адреса" name="view" required>
      <USelect
        v-model="addressForm.view"
        required
        :items="['Адрес регистрации', 'Адрес проживания', 'Другое']"
        placeholder="Выберите вид адреса"
      />
    </UFormField>
    <UFormField label="Адрес" name="addresses" required>
      <UTextarea
        v-model.trim.lazy="addressForm.addresses"
        required
        placeholder="Адрес"
      />
    </UFormField>
    <UButton
        label="Принять"
        color="success"
        variant="outline"
        type="submit"
      />
  </UForm>
</template>
