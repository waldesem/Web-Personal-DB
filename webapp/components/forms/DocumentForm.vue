<script setup lang="ts">
import { toRef } from "vue";
import { stateAnketa, stateClassify } from "@/state/state";
import type { Document } from "@/utils/interfaces";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  docs: {
    type: Object as () => Document,
    default: {},
  },
});

const anketaState = stateAnketa();
const classifyState = stateClassify();

const docForm = toRef(props.docs as Document);

function submitDocument() {
  anketaState.updateItem("documents", docForm.value)
  emit('cancel');
  Object.keys(docForm.value).forEach(
    (key) => delete docForm.value[key as keyof typeof docForm.value]
  );
}
</script>

<template>
  <form
    @submit.prevent="submitDocument"
    class="form form-check"
    role="form"
  >
    <ElementsLabelSlot :label="'Вид документа'">
      <ElementsSelectDiv
        :name="'view'"
        :need="true"
        :select="classifyState.classes.value.documents"
        v-model="docForm['view']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Серия документа'">
      <ElementsInputElement
        :name="'series'"
        :place="'Серия документа'"
        v-model="docForm['series']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Номер документа'">
      <ElementsInputElement
        :name="'number'"
        :place="'Номер документа'"
        :need="true"
        v-model="docForm['digits']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Кем выдан'">
      <ElementsInputElement
        :name="'agency'"
        :place="'Орган выдавший'"
        v-model="docForm['agency']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Дата выдачи'">
      <ElementsInputElement
        :name="'issue'"
        :place="'Дата выдачи'"
        :typeof="'date'"
        v-model="docForm['issue']"
      />
    </ElementsLabelSlot>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </form>
</template>
