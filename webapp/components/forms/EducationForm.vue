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
  <UForm state="educationForm" @submit.prevent="submitEducation">
    <UFormGroup class="mb-3" size="lg" label="Вид образования" required>
      <USelect
        v-model="educationForm['view']"
        :options="classifyState.classes.value.educations"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" size="lg" label="Название учебного заведения" required>
      <UInput
        v-model="educationForm['institution']"
        placeholder="Название учебного заведения"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" size="lg" label="Год окончания" required>
      <UInput
        v-model="educationForm['finished']"
        placeholder="Год окончания"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" size="lg" label="Специальность" required>
      <UInput
        v-model="educationForm['specialty']"
        placeholder="Специальность"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="emit('cancel')"/>
  </UForm>
</template>
