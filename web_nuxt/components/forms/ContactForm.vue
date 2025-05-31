<script setup lang="ts">
import type { Contact } from "@/types";
import * as v from "valibot";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Contact>,
    default: () => ({}),
  },
});

const schema = v.object({
  view: v.string(),
  contact: v.pipe(
    v.string(),
    v.maxLength(255, "Максимальная длина 255 символов")
  ),
});

const contactForm = toRef(props.item as Contact);
</script>

<template>
  <UForm
    :schema="schema"
    :state="contactForm"
    @submit.prevent="emit('update', contactForm)"
  >
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
      />
    </UFormField>
    <UButton label="Принять" color="success" variant="outline" type="submit" />
  </UForm>
</template>
