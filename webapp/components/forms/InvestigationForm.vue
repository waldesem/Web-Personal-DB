<script setup lang="ts">
import { toRef } from "vue";
import { stateAnketa } from "@/state/state";
import type { Inquisition } from "@/utils/interfaces";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  investigation: {
    type: Object as () => Inquisition,
    default: <Inquisition>({}),
  },
});

const anketaState = stateAnketa();

const investigationForm = toRef(props.investigation as Inquisition);

function submitInvestigations() {
  anketaState.updateItem("investigations", investigationForm.value)
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
  >
    <ElementsLabelSlot :label="'Тема проверки'">
      <ElementsInputElement
        :name="'theme'"
        :place="'Тема проверки'"
        :need="true"
        v-model="investigationForm['theme']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Информация'">
      <ElementsTextArea
        :name="'info'"
        :place="'Информация'"
        v-model="investigationForm['info']"
      >
      </ElementsTextArea>
    </ElementsLabelSlot>
    <ElementsBtnGroup @cancel="emit('cancel')"/>
  </form>
</template>
