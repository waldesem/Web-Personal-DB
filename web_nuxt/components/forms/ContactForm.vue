<script setup lang="ts">
import type { Contact } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  contact: {
    type: Object as () => Contact,
    default: {} as Contact,
  },
});

const contactForm = ref(props.contact as Contact);
</script>

<template>
  <UForm :state="contactForm" @submit.prevent="emit('update', contactForm)">
    <UFormGroup class="mb-3" label="Вид контакта" name="view" required>
      <USelect
        v-model.trim.lazy="contactForm.view"
        required
        :options="['Телефон', 'Электронная почта', 'Другое']"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Контакт" name="contact" required>
      <UInput
        v-model.trim.lazy="contactForm.contact"
        required
        placeholder="Контакт"
        maxlength="255"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
