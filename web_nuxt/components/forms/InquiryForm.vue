<script setup lang="ts">
import { toRef } from "vue";
import { stateAnketa } from "@/state/state";
import type { Needs } from "@/utils/interfaces";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  inquiry: {
    type: Object as () => Needs,
    default: {} as Needs,
  },
});

const anketaState = stateAnketa();

const inquiryForm = toRef(props.inquiry as Needs);

function submitIquiry() {
  anketaState.updateItem("inquiries", inquiryForm.value)
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
      <UInput
        v-model="inquiryForm['info']"
        required
        placeholder="Информация"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Инициатор">
      <UTextarea
        v-model="inquiryForm['origins']"
        required
        placeholder="Инициатор"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="emit('cancel')"/>
  </UForm>
</template>
