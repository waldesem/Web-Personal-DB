<script setup lang="ts">
import { toRef } from "vue";
import type { Inquisition } from "@/utils/interfaces";

const emit = defineEmits(["cancel", "submit"]);

const props = defineProps({
  investigation: {
    type: Object as () => Inquisition,
    default: {} as Inquisition,
  },
});

const investigationForm = toRef(props.investigation as Inquisition);

function submitInvestigations() {
  emit('submit', investigationForm.value);
  cancelAction();
}

function cancelAction() {
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
        v-model.trim.lazy="investigationForm['theme']"
        required
        placeholder="Тема проверки"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Информация">
      <UTextarea
        v-model.trim.lazy="investigationForm['info']"
        required
        placeholder="Информация"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelAction"/>
  </UForm>
</template>
