<script setup lang="ts">
import type { Staff } from "@/types";
import * as v from "valibot";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type:  Object as PropType<Staff>,
    default: () => ({}),
  },
});

const schema = v.object({
  position: v.pipe(
    v.string(),
    v.maxLength(255, "Максимальная длина 255 символов")
  ),
  department: v.pipe(
    v.string(),
    v.maxLength(255, "Максимальная длина 255 символов")
  ),
});

const staffForm = toRef(props.item as Staff);
</script>

<template>
  <UForm
  :schema="schema"
    :state="staffForm"
    @submit.prevent="emit('update', staffForm)"
  >
    <UFormField label="Должность" name="position" required>
      <UInput
        v-model.trim.lazy="staffForm.position"
        required
        placeholder="Должность"
      />
    </UFormField>
    <UFormField label="Подразделение" name="department">
      <UInput
        v-model.trim.lazy="staffForm.department"
        placeholder="Подразделение"
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
