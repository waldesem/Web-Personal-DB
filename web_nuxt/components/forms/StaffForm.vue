<script setup lang="ts">
import { z } from "zod";
import type { Staff } from "@/types";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  staff: {
    type: Object as () => Staff,
    default: {} as Staff,
  },
});

const staffForm = ref(props.staff as Staff);

const staffSchema = z.object({
  position: z
    .string({ required_error: "Обязательное поле" })
    .max(255, "Максимум 255 символов"),
  department: z
    .string()
    .max(255, "Максимум 255 символов")
    .nullable()
    .optional(),
});
</script>

<template>
  <UForm
    :state="staffForm"
    :schema="staffSchema"
    @submit.prevent="emit('update', staffForm)"
  >
    <UFormGroup class="mb-3" label="Должность" name="position" required>
      <UInput
        v-model.trim.lazy="staffForm['position']"
        required
        placeholder="Должность"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Подразделение" name="department">
      <UInput
        v-model.trim.lazy="staffForm['department']"
        placeholder="Подразделение"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
