<script setup lang="ts">
import { toRef } from "vue";
import { stateAnketa, stateClassify } from "@/state/state";
import type { Education } from "@/utils/interfaces";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  education: {
    type: Object as () => Education,
    default: {} as Education,
  },
});

const anketaState = stateAnketa();
const classifyState = stateClassify();

const educationForm = toRef(props.education as Education);

function submitEducation() {
  anketaState.updateItem("educations", educationForm.value)
  emit('cancel');
  Object.assign(educationForm.value, {
    view: "",
    institution: "",
    finished: "",
    specialty: "",
  } as Education);
}
</script>

<template>
  <UForm :state="educationForm" @submit.prevent="submitEducation">
    <UFormGroup class="mb-3" label="Вид образования">
      <USelect
        v-model="educationForm['view']"
        required
        :options="Object.values(classifyState.classes.value.educations)"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Название учебного заведения">
      <UInput
        v-model="educationForm['institution']"
        required
        placeholder="Название учебного заведения"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Год окончания">
      <UInput
        v-model="educationForm['finished']"
        placeholder="Год окончания"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Специальность">
      <UInput
        v-model="educationForm['specialty']"
        placeholder="Специальность"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="emit('cancel')"/>
  </UForm>
</template>
