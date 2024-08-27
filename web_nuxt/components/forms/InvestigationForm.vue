<script setup lang="ts">
import { toRef } from "vue";
import { stateAnketa } from "@/state/state";
import type { Inquisition } from "@/utils/interfaces";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  investigation: {
    type: Object as () => Inquisition,
    default: {} as Inquisition,
  },
});

const anketaState = stateAnketa();

const investigationForm = toRef(props.investigation as Inquisition);

function submitInvestigations() {
  anketaState.updateItem("investigations", investigationForm.value)
  emit('cancel');
  Object.assign(investigationForm.value, {
    theme: "",
    info: "",
  } as Inquisition);
}
</script>

<template>
  <UForm :state="investigationForm" @submit.prevent="submitInvestigations">
    <UFormGroup class="mb-3" label="Тема проверки">
      <UInput
        v-model="investigationForm['theme']"
        required
        placeholder="Тема проверки"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Информация">
      <UTextarea
        v-model="investigationForm['info']"
        required
        placeholder="Информация"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="emit('cancel')"/>
  </UForm>
</template>
