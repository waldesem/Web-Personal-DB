<script setup lang="ts">
import { toRef } from "vue";
import type { Needs } from "@/utils/interfaces";

const emit = defineEmits(["cancel", "submit"]);

const props = defineProps({
  inquiry: {
    type: Object as () => Needs,
    default: {} as Needs,
  },
});

const inquiryForm = toRef(props.inquiry as Needs);

function submitIquiry() {
  emit('submit', inquiryForm.value);
  cancelAction();
}

function cancelAction() {
  emit('cancel');
  Object.assign(inquiryForm.value, {
    info: "",
    origins: "",
  } as Needs);
}
</script>

<template>
  <UForm :state="inquiryForm" @submit.prevent="submitIquiry">
    <UFormGroup class="mb-3" label="Информация">
      <UTextarea
        v-model.trim.lazy="inquiryForm['info']"
        required
        placeholder="Информация"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Инициатор">
      <UInput
        v-model.trim.lazy="inquiryForm['origins']"
        required
        placeholder="Инициатор"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelAction"/>
  </UForm>
</template>
