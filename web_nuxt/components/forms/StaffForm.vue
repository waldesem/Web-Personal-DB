<script setup lang="ts">
import type { Staff } from "@/types/interfaces";
import { useFetchAuth } from "@/utils/auth";

const toast = useToast();

const authFetch = useFetchAuth();

const emit = defineEmits(["cancel", "close", "update"]);

const props = defineProps({
  staff: {
    type: Object as () => Staff,
    default: {} as Staff,
  },
  candId: {
    type: String,
    default: "",
  },
});

const staffForm = toRef(props.staff as Staff);

function submitStaff() {
  emit("close");
  authFetch("/api/staffs/" + props.candId, {
    method: "POST",
    body: staffForm.value,
  });
  toast.add({
    icon: "i-heroicons-check-circle",
    title: "Успешно",
    description: "Информация обновлена",
    color: "green",
  });
  emit("update");
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
