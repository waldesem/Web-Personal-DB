<script setup lang="ts">
import type { Staff } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  staff: {
    type: Object as () => Staff,
    default: {} as Staff,
  },
});

const staffForm = ref(props.staff as Staff);
</script>

<template>
  <UForm
    :state="staffForm"
    @submit.prevent="emit('update', staffForm)"
  >
    <UFormGroup class="mb-3" label="Должность" name="position" required>
      <UInput
        v-model.trim.lazy="staffForm['position']"
        required
        placeholder="Должность"
        maxlength="255"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Подразделение" name="department">
      <UInput
        v-model.trim.lazy="staffForm['department']"
        placeholder="Подразделение"
        maxlength="255"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
