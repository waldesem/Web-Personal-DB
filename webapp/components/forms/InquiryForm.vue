<script setup lang="ts">
import { toRef } from "vue";
import type { Needs } from "../../utils/interfaces";
import { stateAnketa } from "../../utils/state";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  inquiry: {
    type: Object as () => Needs,
    default: {},
  },
});

const inquiryForm = toRef(props.inquiry as Needs);

function submitIquiry() {
  stateAnketa.updateItem("inquiries", inquiryForm.value)
  emit('cancel');
  Object.keys(inquiryForm.value).forEach(
    (key) => delete inquiryForm.value[key as keyof typeof inquiryForm.value]
  );
}
</script>

<template>
  <form
    @submit.prevent="submitIquiry"
    class="form form-check p-3"
    role="form"
  >
    <ElementsLabelSlot :label="'Информация'">
      <ElementsTextArea
        :name="'info'"
        :place="'Информация'"
        v-model="inquiryForm['info']"
      >
      </ElementsTextArea>
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Инициатор'">
      <ElementsInputElement
        :name="'origins'"
        :place="'Инициатор'"
        v-model="inquiryForm['origins']"
      />
    </ElementsLabelSlot>
    <ElementsBtnGroup @cancel="emit('cancel')"/>
  </form>
</template>
