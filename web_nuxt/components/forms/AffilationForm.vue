<script setup lang="ts">
import { toRef } from "vue";
import { stateClassify } from "@/state/state";
import type { Affilation } from "@/utils/interfaces";

const emit = defineEmits(["cancel", "submit"]);

const props = defineProps({
  affils: {
    type: Object as () => Affilation,
    default: {} as Affilation,
  },
});

const classifyState = stateClassify();

const affilationForm = toRef(props.affils as Affilation);

function submitAffilation() {
  emit("submit", affilationForm.value);
  clearForm();
}

function cancelAction() {
  emit('cancel');
  clearForm();
}

function clearForm() {
  Object.assign(affilationForm.value, {
    view: "",
    organization: "",
    inn: "",
  } as Affilation);
}
</script>

<template>
  <UForm :state="affilationForm" @submit.prevent="submitAffilation">
    <UFormGroup class="mb-3" label="Тип участия">
      <USelect
        v-model.trim.lazy="affilationForm['view']"
        required
        :options="Object.values(classifyState.classes.value.affiliates)"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Организация">
      <UInput
        v-model.trim.lazy="affilationForm['organization']"
        required
        placeholder="Организация"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="ИНН">
      <UInput
        v-model.trim.lazy="affilationForm['inn']"
        placeholder="ИНН"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelAction" />
  </UForm>
</template>
