<script setup lang="ts">

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Needs>,
    default: () => ({}),
  },
});

const inquiryForm = toRef(props.item);
</script>

<template>
  <UForm
    :state="inquiryForm"
    @submit.prevent="emit('update', inquiryForm)"
  >
    <UFormField label="Информация" name="info" required>
      <UTextarea
        v-model.trim.lazy="inquiryForm.info"
        autoresize
        placeholder="Информация"
        required
      />
    </UFormField>
    <UFormField label="Инициатор" name="initiator" required>
      <UInput
        v-model.trim.lazy="inquiryForm.initiator"
        placeholder="Инициатор"
        maxlength="255"
        required
      />
    </UFormField>
    <UButton label="Принять" color="success" variant="outline" type="submit" />
  </UForm>
</template>
