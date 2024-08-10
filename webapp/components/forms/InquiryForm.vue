<script setup lang="ts">
import { toRef } from "vue";
import { stateAnketa } from "@/state/state";
import type { Needs } from "@/utils/interfaces";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  inquiry: {
    type: Object as () => Needs,
    default: <Needs>({}),
  },
});

const anketaState = stateAnketa();

const inquiryForm = toRef(props.inquiry as Needs);

function submitIquiry() {
  anketaState.updateItem("inquiries", inquiryForm.value)
  emit('cancel');
  Object.keys(inquiryForm.value).forEach(
    (key) => delete inquiryForm.value[key as keyof typeof inquiryForm.value]
  );
}
</script>

<template>
  <UForm @submit.prevent="submitIquiry">
    <UFormGroup class="mb-3" size="md" label="Информация" required>
      <UInput
        v-model="inquiryForm['info']"
        placeholder="Информация"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" size="md" label="Инициатор" required>
      <UInput
        v-model="inquiryForm['origins']"
        placeholder="Инициатор"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="emit('cancel')"/>
  </UForm>
</template>
