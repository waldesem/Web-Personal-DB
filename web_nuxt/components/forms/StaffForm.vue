<script setup lang="ts">
import type { Staff } from '@/types';

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Staff>,
    default: () => ({}),
  },
});

const staffForm = toRef(props.item as Staff);
</script>

<template>
  <UForm :state="staffForm" @submit.prevent="emit('update', staffForm)">
    <UFormField label="Должность" name="position" required>
      <UInput
        v-model.trim.lazy="staffForm.position"
        placeholder="Должность"
        maxlength="255"
        required
      />
    </UFormField>
    <UFormField label="Подразделение" name="department">
      <UInput
        v-model.trim.lazy="staffForm.department"
        placeholder="Подразделение"
        maxlength="255"
      />
    </UFormField>
    <UButton label="Принять" color="success" variant="outline" type="submit" />
  </UForm>
</template>
