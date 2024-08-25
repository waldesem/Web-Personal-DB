<script setup lang="ts">
import { toRef } from "vue";
import { stateAnketa, stateClassify } from "@/state/state";
import type { Affilation } from "@/utils/interfaces";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  affils: {
    type: Object as () => Affilation,
    default: {} as Affilation,
  },
});

const anketaState = stateAnketa();
const classifyState = stateClassify();

const affilationForm = toRef(props.affils as Affilation);

function submitAffilation() {
  anketaState.updateItem("affilations", affilationForm.value)
  emit('cancel');
  affilationForm.value = {} as Affilation;
}
</script>

<template>
  <UForm :state="affilationForm" @submit.prevent="submitAffilation">
    <UFormGroup class="mb-3" label="Тип участия">
      <USelect
        v-model="affilationForm['view']"
        required
        :options="Object.values(classifyState.classes.value.affiliates)"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Организация">
      <UInput
        v-model="affilationForm['organization']"
        required
        placeholder="Организация"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="ИНН">
      <UInput
        v-model="affilationForm['inn']"
        placeholder="ИНН"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
