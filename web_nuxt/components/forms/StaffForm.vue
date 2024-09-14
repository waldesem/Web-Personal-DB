<script setup lang="ts">
import { toRef } from "vue";
import type { Staff } from "@/types/interfaces";

const emit = defineEmits(["cancel", "submit"]);

const props = defineProps({
  staff: {
    type: Object as () => Staff,
    default: {} as Staff,
  },
});

const staffForm = toRef(props.staff as Staff);

function submitStaff() {
  emit("submit", staffForm.value);
  clearForm();
}

function cancelAction() {
  emit('cancel');
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
  <UForm :state="staffForm" @submit.prevent="submitStaff">
    <UFormGroup class="mb-3" label="Должность">
      <UInput
        v-model.trim.lazy="staffForm['position']"
        required
        placeholder="Должность"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Подразделение">
      <UInput
        v-model.trim.lazy="staffForm['department']"
        placeholder="Подразделение"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelAction" />
  </UForm>
</template>
