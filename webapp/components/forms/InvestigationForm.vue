<script setup lang="ts">
import { toRef } from "vue";
import { stateAnketa } from "@/state/state";
import type { Inquisition } from "@/utils/interfaces";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  investigation: {
    type: Object as () => Inquisition,
    default: <Inquisition>({}),
  },
});

const anketaState = stateAnketa();

const investigationForm = toRef(props.investigation as Inquisition);

function submitInvestigations() {
  anketaState.updateItem("investigations", investigationForm.value)
  emit('cancel');
  Object.keys(investigationForm.value).forEach(
    (key) => delete investigationForm.value[key as keyof typeof investigationForm.value]
  );
}
</script>

<template>
  <UForm :state="investigationForm" @submit.prevent="submitInvestigations">
    <UFormGroup class="mb-3" label="Тема проверки" required>
      <UInput
        v-model="investigationForm['theme']"
        placeholder="Тема проверки"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Информация" required>
      <UTextarea
        v-model="investigationForm['info']"
        placeholder="Информация"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="emit('cancel')"/>
  </UForm>
</template>
