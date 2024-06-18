<script setup lang="ts">
import { defineAsyncComponent, toRef } from "vue";
import { Affilation } from "@/interfaces";
import { stateClassify } from "@/state";

const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
)
const SelectDiv = defineAsyncComponent(
  () => import("@components/content/elements/SelectDiv.vue")
);
const GroupContent = defineAsyncComponent(
  () => import("@components/content/elements/GroupContent.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);

const emit = defineEmits(["submit", "cancel"]);

const props = defineProps({
  affils: {
    type: Object as () => Affilation,
    default: {},
  },
});

const affilationForm = toRef(props.affils as Affilation);
</script>

<template>
  <form
    @submit.prevent="emit('submit', affilationForm)"
    class="form form-check"
    role="form"
  >
    <LabelSlot :label="'Тип участия'">
      <SelectDiv
        :name="'view'"
        :select="stateClassify.affilations"
        v-model="affilationForm['view']"
      />
    </LabelSlot>
    <LabelSlot :label="'Организация'">
      <InputElement
        :name="'name'"
        :place="'Организация'"
        :need="true"
        v-model="affilationForm['name']"
      />
    </LabelSlot>
    <LabelSlot :label="'ИНН'">
      <InputElement
        :name="'inn'"
        :place="'ИНН'"
        :pattern="'[0-9]{12}'"
        v-model="affilationForm['inn']"
      />
    </LabelSlot>
    <LabelSlot :label="'Должность'">
      <InputElement
        :name="'position'"
        :place="'Должность'"
        :need="true"
        v-model="affilationForm['position']"
      />
    </LabelSlot>
    <BtnGroup>
      <GroupContent
        @cancel="emit('cancel')"
      />
    </BtnGroup>
  </form>
</template>
