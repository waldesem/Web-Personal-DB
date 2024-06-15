<script setup lang="ts">
import { toRef, defineAsyncComponent } from "vue";
import { Needs } from "@/interfaces";
import { clearForm } from "@/utilities";

const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
)
const TextArea = defineAsyncComponent(
  () => import("@components/content/elements/TextArea.vue")
);
const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const BtnGroupContent = defineAsyncComponent(
  () => import("@components/content/elements/GroupContent.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);

const emit = defineEmits(["submit", "cancel"]);

const props = defineProps({
  inquiry: {
    type: Object as () => Needs,
    default: {},
  },
  action: {
    type: String,
    default: "create",
  }
});

const inquiryForm = toRef(props.inquiry as Needs);
</script>

<template>
  <form
    @submit.prevent="
      emit('submit', inquiryForm, props.action); 
      clearForm(inquiryForm)
    "
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
        :name="'initiator'"
        :place="'Инициатор'"
        v-model="inquiryForm['initiator']"
      />
    </LabelSlot>
    <BtnGroup>
      <BtnGroupContent
        @cancel="emit('cancel')"
      />
    </BtnGroup>
  </form>
</template>
