<script setup lang="ts">
import type { Staff } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  item: {
    type: Object as () => Staff,
    default: {} as Staff,
  },
});

const staffForm = ref(props.item as Staff);
</script>

<template>
  <UForm
    :state="staffForm"
    @submit.prevent="emit('update', staffForm)"
  >
    <UFormField class="mb-3" label="Должность" name="position" required>
      <UInput
        v-model.trim.lazy="staffForm.position"
        required
        placeholder="Должность"
        maxlength="255"
      />
    </UFormField>
    <UFormField class="mb-3" label="Подразделение" name="department">
      <UInput
        v-model.trim.lazy="staffForm.department"
        placeholder="Подразделение"
        maxlength="255"
      />
    </UFormField>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
