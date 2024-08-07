<script setup lang="ts">
import { toRef } from "vue";
import { stateAnketa, stateClassify } from "@/state/state";
import type { Affilation } from "@/utils/interfaces";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  affils: {
    type: Object as () => Affilation,
    default: {},
  },
});

const anketaState = stateAnketa();
const classifyState = stateClassify();

const affilationForm = toRef(props.affils as Affilation);

function submitAffilation() {
  anketaState.updateItem("affilations", affilationForm.value)
  emit('cancel');
  Object.keys(affilationForm.value).forEach(
    (key) => delete affilationForm.value[key as keyof typeof affilationForm.value]
  );
}
</script>

<template>
  <form
    @submit.prevent="submitAffilation"
    class="form form-check"
    role="form"
  >
    <ElementsLabelSlot :label="'Тип участия'">
      <ElementsSelectDiv
        :name="'view'"
        :select="classifyState.classes.value.affilations"
        v-model="affilationForm['view']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Организация'">
      <ElementsInputElement
        :name="'name'"
        :place="'Организация'"
        :need="true"
        v-model="affilationForm['organization']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'ИНН'">
      <ElementsInputElement
        :name="'inn'"
        :place="'ИНН'"
        :pattern="'[0-9]{12}'"
        v-model="affilationForm['inn']"
      />
    </ElementsLabelSlot>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </form>
</template>
