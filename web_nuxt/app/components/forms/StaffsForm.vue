<script setup lang="ts">
import type { Staff } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Staff>,
    default: () => ({}),
  },
});

const form = toRef(props.item);
</script>

<template>
  <UForm :state="form" @submit.prevent="emit('update', form)">
    <UFormField label="Должность" name="position" required>
      <UInput
        v-model.trim.lazy="form.position"
        placeholder="Должность"
        maxlength="255"
        required
      />
    </UFormField>
    <UFormField label="Подразделение" name="department">
      <UInput
        v-model.trim.lazy="form.department"
        placeholder="Подразделение"
        maxlength="255"
      />
    </UFormField>
    <UButton label="Принять" color="success" variant="outline" type="submit" />
  </UForm>
</template>
