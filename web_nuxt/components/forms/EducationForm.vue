<script setup lang="ts">
import { toRef } from "vue";
import { stateClassify } from "@/state/state";
import type { Education } from "@/utils/interfaces";

const emit = defineEmits(["cancel", "submit"]);

const props = defineProps({
  education: {
    type: Object as () => Education,
    default: {} as Education,
  },
});

const classifyState = stateClassify();

const educationForm = toRef(props.education as Education);

function submitEducation() {
  emit("submit", educationForm.value);
  cancelAction();
}

function cancelAction() {
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
        v-model.trim.lazy="educationForm['institution']"
        required
        placeholder="Название учебного заведения"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Год окончания">
      <UInput
        v-model.trim.lazy="educationForm['finished']"
        placeholder="Год окончания"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Специальность">
      <UInput
        v-model.trim.lazy="educationForm['specialty']"
        placeholder="Специальность"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelAction"/>
  </UForm>
</template>
