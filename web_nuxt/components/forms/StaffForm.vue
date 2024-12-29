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

const staffForm = toRef(props.staff as Staff);

function submitStaff() {
  emit("update", staffForm.value);
  clearForm();
}

function cancelAction() {
  emit("cancel");
  clearForm();
}

function clearForm() {
  Object.assign(staffForm.value, {
    position: "",
    department: "",
  } as Staff);
}
</script>

<template>
  <UForm :state="staffForm" :schema="staffSchema" @submit.prevent="submitStaff">
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
    <ElementsBtnGroup @cancel="cancelAction" />
  </UForm>
</template>
