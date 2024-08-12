<script setup lang="ts">
import { toRef } from "vue";
import { stateAnketa } from "@/state/state";
import type { Staff } from "@/utils/interfaces";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  staff: {
    type: Object as () => Staff,
    default: <Staff>({}),
  },
});

const anketaState = stateAnketa();

const staffForm = toRef(props.staff as Staff);

function submitStaff() {
  anketaState.updateItem("staffs", staffForm.value)
  emit('cancel');
  Object.keys(staffForm.value).forEach(
    (key) => delete staffForm.value[key as keyof typeof staffForm.value]
  );
}
</script>

<template>
  <UForm :state="staffForm" @submit.prevent="submitStaff">
    <UFormGroup class="mb-3" label="Должность" required>
      <UInput
        v-model="staffForm['position']"
        placeholder="Должность"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Подразделение">
      <UInput
        v-model="staffForm['department']"
        placeholder="Подразделение"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
