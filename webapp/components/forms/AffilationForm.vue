<script setup lang="ts">
import { toRef } from "vue";
import type { Affilation } from "../../utils/interfaces";
import { stateClassify, stateAnketa } from "../../utils/state";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  affils: {
    type: Object as () => Affilation,
    default: {},
  },
});

const affilationForm = toRef(props.affils as Affilation);

function submitAffilation() {
  stateAnketa.updateItem("affilations", affilationForm.value)
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
        :select="stateClassify.classes.affilations"
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
