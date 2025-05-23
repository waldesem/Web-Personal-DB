<script setup lang="ts">
import type { Contact } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  item: {
    type:  Object as PropType<Contact>,
    default: () => ({}),
  },
});

const contactForm = toRef(props.item as Contact);
</script>

<template>
  <UForm :state="contactForm" @submit.prevent="emit('update', contactForm)">
    <UFormField label="Вид контакта" name="view" required>
      <USelect
        v-model="contactForm.view"
        required
        :items="['Телефон', 'Электронная почта', 'Другое']"
        placeholder="Выберите вид контакта"
      />
    </UFormField>
    <UFormField label="Контакт" name="contact" required>
      <UInput
        v-model.trim.lazy="contactForm.contact"
        required
        placeholder="Контакт"
        maxlength="255"
      />
    </UFormField>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
