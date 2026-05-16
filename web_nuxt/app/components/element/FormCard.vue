<script setup lang="ts">
import type { FormField } from "@/types";

const emit = defineEmits(["submit"]);

const props = defineProps({
  item: {
    type: Object,
    default: () => ({}),
  },
  fields: {
    type: Array as PropType<FormField[]>,
    required: true,
  },
});

const form = toRef(props.item);
</script>

<template>
  <UForm :state="form" @submit.prevent="emit('submit', form)">
    <UFormField
      v-for="field in props.fields"
      :key="field.key"
      :name="field.key"
      :label="field.label"
      :required="
        field.attrs ? (field.attrs.required as unknown as boolean) : false
      "
    >
      <UInput
        v-if="field.element === 'input'"
        v-model.trim.lazy="form[field.key]"
        v-bind="{ ...field.attrs }"
      />
      <USelect
        v-else-if="field.element === 'select'"
        v-model="form[field.key]"
        v-bind="{ ...field.attrs }"
        :items="field.items"
      />
      <UTextarea
        v-else-if="field.element === 'textarea'"
        v-model.trim.lazy="form[field.key]"
        v-bind="{ ...field.attrs }"
        autoresize
      />
    </UFormField>
    <UButton label="Принять" color="success" variant="outline" type="submit" />
  </UForm>
</template>
