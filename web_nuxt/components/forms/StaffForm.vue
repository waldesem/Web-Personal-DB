<script setup lang="ts">
import { toRef } from "vue";
import { stateAnketa } from "@/state/state";
import type { Staff } from "@/utils/interfaces";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  staff: {
    type: Object as () => Staff,
    default: {} as Staff,
  },
});

const anketaState = stateAnketa();

const staffForm = toRef(props.staff as Staff);

function submitStaff() {
  anketaState.updateItem("staffs", staffForm.value)
  emit('cancel');
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
        v-model="staffForm['position']"
        required
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
