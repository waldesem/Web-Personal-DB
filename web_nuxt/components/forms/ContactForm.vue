<script setup lang="ts">
import type { Contact } from "@/types";

const emit = defineEmits(["cancel", "update", 'clear']);

const props = defineProps({
  item: {
    type: Object as () => Contact,
    default: {} as Contact,
  },
});

const contactForm = ref(props.item as Contact);
</script>

<template>
  <UForm :state="contactForm" @submit.prevent="emit('update', contactForm)">
    <UFormField class="mb-3" label="Вид контакта" name="view" required>
      <USelect
        v-model="contactForm.view"
        required
        :items="['Телефон', 'Электронная почта', 'Другое']"
        placeholder="Выберите вид контакта"
      />
    </UFormField>
    <UFormField class="mb-3" label="Контакт" name="contact" required>
      <UInput
        v-model.trim.lazy="contactForm.contact"
        required
        placeholder="Контакт"
        maxlength="255"
      />
    </UFormField>
    <ElementsBtnGroup @cancel="emit('cancel')" @clear="emit('clear')" />
  </UForm>
</template>
