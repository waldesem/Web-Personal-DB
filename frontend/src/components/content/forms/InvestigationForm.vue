<script setup lang="ts">
import { computed, defineAsyncComponent } from "vue";
import { Inquisition } from "@/interfaces/interface";

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
  investigation: {
    type: Object as () => Inquisition,
    default: {},
  },
});

const investigationForm = computed(() => {
  return props.investigation as Inquisition;
});
</script>

<template>
  <form
    @submit.prevent="emit('submit', investigationForm)"
    class="form form-check"
    role="form"
  >
    <LabelSlot :label="'Тема проверки'">
      <InputElement
        :name="'theme'"
        :place="'Тема проверки'"
        :need="true"
        v-model="investigationForm['theme']"
      />
    </LabelSlot>
    <LabelSlot :label="'Информация'">
      <TextArea
        :name="'info'"
        :place="'Информация'"
        v-model="props.investigation['info']"
      />
    </LabelSlot>
    <BtnGroup>
      <BtnGroupContent
        @cancel="emit('cancel')"
      />
    </BtnGroup>
  </form>
</template>
