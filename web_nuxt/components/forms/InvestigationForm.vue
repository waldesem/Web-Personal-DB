<script setup lang="ts">
import type { Inquisition } from "@/types/interfaces";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  investigation: {
    type: Object as () => Inquisition,
    default: {} as Inquisition,
  },
  candId: {
    type: String,
    default: "",
  },
});

const investigationForm = toRef(props.investigation as Inquisition);

function submitInvestigations() {
  emit("update", investigationForm.value);
  clearForm();
}

function cancelAction() {
  emit("cancel");
  clearForm();
}

function clearForm() {
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
        autoresize
        placeholder="Информация"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelAction" />
  </UForm>
</template>
