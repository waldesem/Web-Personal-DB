<script setup lang="ts">
import { defineAsyncComponent, toRef } from "vue";
import { Education } from "@/interfaces";
import { stateClassify, stateAnketa } from "@/state";

const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
)
const SelectDiv = defineAsyncComponent(
  () => import("@components/content/elements/SelectDiv.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);

const emit = defineEmits(["cancel"]);

const props = defineProps({
  education: {
    type: Object as () => Education,
    default: {},
  },
});

const educationForm = toRef(props.education as Education);

function submitEducation() {
  stateAnketa.updateItem("educations", educationForm.value)
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
    role="form"
  >
    <LabelSlot :label="'Уровень образования'">
      <SelectDiv
        :name="'type'"
        :need="true"
        :select="stateClassify.educations"
        v-model="educationForm['view']"
      />
    </LabelSlot>
    <LabelSlot :label="'Название учебного заведения'">
      <InputElement
        :name="'name'"
        :place="'Название учебного заведения'"
        v-model="educationForm['institution']"
      />
    </LabelSlot>
    <LabelSlot :label="'Год окончания'">
      <InputElement
        :name="'finish'"
        :place="'Год окончания'"
        :need="true"
        v-model="educationForm['finished']"
      />
    </LabelSlot>
    <LabelSlot :label="'Специальность'">
      <InputElement
        :name="'specialty'"
        :place="'Специальность'"
        v-model="educationForm['specialty']"
      />
    </LabelSlot>
    <BtnGroup @cancel="emit('cancel')"/>
  </form>
</template>
