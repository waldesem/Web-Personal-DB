<script setup lang="ts">
import { toRef } from "vue";
import { stateAnketa, stateClassify } from "@/state/state";
import type { Education } from "@/utils/interfaces";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  education: {
    type: Object as () => Education,
    default: <Education>({}),
  },
});

const anketaState = stateAnketa();
const classifyState = stateClassify();

const educationForm = toRef(props.education as Education);

function submitEducation() {
  anketaState.updateItem("educations", educationForm.value)
  emit('cancel');
  Object.keys(educationForm.value).forEach(
    (key) => delete educationForm.value[key as keyof typeof educationForm.value]
  );
}
</script>

<template>
  <form
    @submit.prevent="submitEducation"
    class="form form-check"
  >
    <ElementsLabelSlot :label="'Уровень образования'">
      <ElementsSelectDiv
        :name="'type'"
        :need="true"
        :select="classifyState.classes.value.educations"
        v-model="educationForm['view']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Название учебного заведения'">
      <ElementsInputElement
        :name="'name'"
        :place="'Название учебного заведения'"
        v-model="educationForm['institution']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Год окончания'">
      <ElementsInputElement
        :name="'finish'"
        :place="'Год окончания'"
        :need="true"
        v-model="educationForm['finished']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Специальность'">
      <ElementsInputElement
        :name="'specialty'"
        :place="'Специальность'"
        v-model="educationForm['specialty']"
      />
    </ElementsLabelSlot>
    <ElementsBtnGroup @cancel="emit('cancel')"/>
  </form>
</template>
