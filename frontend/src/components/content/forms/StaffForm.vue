<script setup lang="ts">
import { defineAsyncComponent, toRef } from "vue";
import { Staff } from "@/interfaces";

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

const emit = defineEmits(["submit", "cancel"]);

const props = defineProps({
  staff: {
    type: Object as () => Staff,
    default: {},
  },
});

const staffForm = toRef(props.staff as Staff);
</script>

<template>
  <form
    @submit.prevent="emit('submit', staffForm)"
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
