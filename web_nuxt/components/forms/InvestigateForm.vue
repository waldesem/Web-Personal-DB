<script setup lang="ts">

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Inquisition>,
    default: () => ({}),
  },
});

const investigationForm = toRef(props.item as Inquisition);
</script>

<template>
  <UForm
    :state="investigationForm"
    @submit.prevent="emit('update', investigationForm)"
  >
    <UFormField label="Тема проверки" name="theme" required>
      <UInput
        v-model.trim.lazy="investigationForm.theme"
        placeholder="Тема проверки"
        maxlength="255"
        required
      />
    </UFormField>
    <UFormField label="Информация" name="info" required>
      <UTextarea
        v-model.trim.lazy="investigationForm.info"
        autoresize
        placeholder="Информация"
        required
      />
    </UFormField>
    <UButton label="Принять" color="success" variant="outline" type="submit" />
  </UForm>
</template>
