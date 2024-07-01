<script setup lang="ts">
import { toRef, defineAsyncComponent } from "vue";
import { Inquisition } from "@/interfaces";
import { stateAnketa } from "@/state";

const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);
const TextArea = defineAsyncComponent(
  () => import("@components/content/elements/TextArea.vue")
);
const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);

const emit = defineEmits(["cancel"]);

const props = defineProps({
  investigation: {
    type: Object as () => Inquisition,
    default: {},
  },
});

const investigationForm = toRef(props.investigation as Inquisition);

function submitInvestigations() {
  stateAnketa.updateItem("investigations", investigationForm.value)
  emit('cancel');
  Object.keys(investigationForm.value).forEach(
    (key) => delete investigationForm.value[key as keyof typeof investigationForm.value]
  );
}
</script>

<template>
  <form
    @submit.prevent="submitInvestigations"
    class="form form-check p-3"
    role="form"
  >
    <LabelSlot :label="'Тема проверки'">
      <InputElement
        :name="'theme'"
        :place="'Тема проверки'"
        :need="true"
        v-model="investigationForm['theme']"
      />
    </LabelSlot>
    <LabelSlot :label="'Информация'">
      <TextArea
        :name="'info'"
        :place="'Информация'"
        v-model="investigationForm['info']"
      >
      </TextArea>
    </LabelSlot>
    <BtnGroup @cancel="emit('cancel')"/>
  </form>
</template>
