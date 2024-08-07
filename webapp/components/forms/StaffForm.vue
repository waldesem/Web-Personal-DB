<script setup lang="ts">
import { toRef } from "vue";
import { stateAnketa } from "@/state/state";
import type { Staff } from "@/utils/interfaces";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  staff: {
    type: Object as () => Staff,
    default: {},
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
  <form
    @submit.prevent="submitStaff"
    class="form form-check"
    role="form"
  >
    <ElementsLabelSlot :label="'Должность'">
      <ElementsInputElement
        :name="'position'"
        :place="'Должность'"
        :need="true"
        v-model="staffForm['position']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Подразделение'">
      <ElementsInputElement
        :name="'department'"
        :place="'Подразделение'"
        v-model="staffForm['department']"
      />
    </ElementsLabelSlot>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </form>
</template>
