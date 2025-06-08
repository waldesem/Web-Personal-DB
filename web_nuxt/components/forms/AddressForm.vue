<script setup lang="ts">

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Address>,
    default: () => ({}),
  },
});

const addressForm = toRef(props.item as Address);
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
    <UFormField label="Адрес" name="addresses" required>
      <UTextarea
        v-model.trim.lazy="addressForm.addresses"
        placeholder="Адрес"
        required
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
