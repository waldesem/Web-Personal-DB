<script setup lang="ts">

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Contact>,
    default: () => ({}),
  },
});

const contactForm = toRef(props.item as Contact);
</script>

<template>
  <UForm
    :state="contactForm"
    @submit.prevent="emit('update', contactForm)"
  >
    <UFormField label="Вид контакта" name="view" required>
      <USelect
        v-model="contactForm.view"
        :items="['Телефон', 'Электронная почта', 'Другое']"
        placeholder="Выберите вид контакта"
        required
      />
    </UFormField>
    <UFormField label="Контакт" name="contact" required>
      <UInput
        v-model.trim.lazy="contactForm.contact"
        placeholder="Контакт"
        maxlength="255"
        required
      />
    </UFormField>
    <UButton label="Принять" color="success" variant="outline" type="submit" />
  </UForm>
</template>
