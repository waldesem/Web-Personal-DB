<script setup lang="ts">
import { toRef, defineAsyncComponent } from "vue";
import { Needs } from "@/interfaces";
import { stateAnketa } from "@/state";

const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
)
const TextArea = defineAsyncComponent(
  () => import("@components/content/elements/TextArea.vue")
);
const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);

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
    <LabelSlot :label="'Информация'">
      <TextArea
        :name="'info'"
        :place="'Информация'"
        v-model="inquiryForm['info']"
      >
      </TextArea>
    </LabelSlot>
    <LabelSlot :label="'Инициатор'">
      <InputElement
        :name="'origins'"
        :place="'Инициатор'"
        v-model="inquiryForm['origins']"
      />
    </LabelSlot>
    <BtnGroup @cancel="emit('cancel')"/>
  </form>
</template>
