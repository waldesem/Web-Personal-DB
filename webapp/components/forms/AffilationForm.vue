<script setup lang="ts">
import { toRef } from "vue";
import { stateAnketa, stateClassify } from "@/state/state";
import type { Affilation } from "@/utils/interfaces";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  affils: {
    type: Object as () => Affilation,
    default: <Affilation>({}),
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
  <UForm :state="affilationForm" @submit.prevent="submitAffilation">
    <UFormGroup class="mb-3" size="lg" label="Тип участия">
      <USelect
        v-model="affilationForm['view']"
        :options="classifyState.classes.value.affilations"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" size="lg" label="Организация" required>
      <UInput
        v-model="affilationForm['organization']"
        placeholder="Организация"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" size="lg" label="ИНН" required>
      <UInput
        v-model="affilationForm['inn']"
        placeholder="ИНН"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
