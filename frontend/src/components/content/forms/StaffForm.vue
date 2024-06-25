<script setup lang="ts">
import { defineAsyncComponent, toRef } from "vue";
import { Staff } from "@/interfaces";
import { stateAnketa } from "@/state";

const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
)
const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);
const BtnGroupContent = defineAsyncComponent(
  () => import("@components/content/elements/GroupContent.vue")
);

const emit = defineEmits(["cancel"]);

const props = defineProps({
  staff: {
    type: Object as () => Staff,
    default: {},
  },
});

const staffForm = toRef(props.staff as Staff);

function submitStaff() {
  stateAnketa.updateItem("staffs", staffForm.value)
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
    <LabelSlot :label="'Должность'">
      <InputElement
        :name="'position'"
        :place="'Должность'"
        :need="true"
        v-model="staffForm['position']"
      />
    </LabelSlot>
    <LabelSlot :label="'Подразделение'">
      <InputElement
        :name="'department'"
        :place="'Подразделение'"
        v-model="staffForm['department']"
      />
    </LabelSlot>
    <BtnGroup>
      <BtnGroupContent
        @cancel="emit('cancel')"
      />
    </BtnGroup>
  </form>
</template>
