<script setup lang="ts">
import { toRef, defineAsyncComponent } from "vue";
import { Needs } from "@/interfaces/interface";

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
});

const inquiryForm = toRef(props.inquiry as Needs);
</script>

<template>
  <form
    @submit.prevent="emit('submit', inquiryForm)"
    class="form form-check"
    role="form"
  >
    <LabelSlot :label="'Информация'">
      <TextArea
        :name="'info'"
        :place="'Информация'"
        v-model="props.inquiry['info']"
      />
    </LabelSlot>
    <LabelSlot :label="'Инициатор'">
      <InputElement
        :name="'initiator'"
        :place="'Инициатор'"
        v-model="inquiryForm['initiator']"
      />
    </LabelSlot>
    <LabelSlot :label="'Источник'">
      <InputElement
        :name="'source'"
        :place="'Источник'"
        v-model="inquiryForm['source']"
      />
    </LabelSlot>
    <BtnGroup>
      <BtnGroupContent
        @cancel="emit('cancel')"
      />
    </BtnGroup>
  </form>
</template>
