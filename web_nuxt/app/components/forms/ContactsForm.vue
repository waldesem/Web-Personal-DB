<script setup lang="ts">
import type { Contact } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Contact>,
    default: () => ({}),
  },
});

const form = toRef(props.item);
</script>

<template>
  <UForm :state="form" @submit.prevent="emit('update', form)">
    <UFormField label="Вид контакта" name="view" required>
      <USelect
        v-model="form.view"
        :items="['Телефон', 'Электронная почта', 'Другое']"
        placeholder="Выберите вид контакта"
        required
      />
    </UFormField>
    <UFormField label="Контакт" name="contact" required>
      <UInput
        v-model.trim.lazy="form.contact"
        placeholder="Контакт"
        maxlength="255"
        required
        :type="form.view === 'Электронная почта' ? 'email' : 'text'"
      />
    </UFormField>
    <UButton label="Принять" color="success" variant="outline" type="submit" />
  </UForm>
</template>
