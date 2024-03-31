<script setup lang="ts">
import { computed, defineAsyncComponent } from "vue";
import { Needs } from "@/interfaces/interface";

const TextArea = defineAsyncComponent(
  () => import("@components/content/elements/TextArea.vue")
);
const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const BtnGroupContent = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroupContent.vue")
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

const inquiryForm = computed(() => {
  return props.inquiry as Needs;
});
</script>

<template>
  <form
    @submit.prevent="emit('submit', inquiryForm)"
    class="form form-check"
    role="form"
  >
    <TextArea
      :name="'info'"
      :label="'Информация'"
      v-model="props.inquiry['info']"
    />
    <InputElement
      :name="'initiator'"
      :label="'Инициатор'"
      v-model="inquiryForm['initiator']"
    />
    <InputElement
      :name="'source'"
      :label="'Источник'"
      v-model="inquiryForm['source']"
    />
    <BtnGroup>
      <BtnGroupContent/>
      <button
        class="btn btn-outline-danger btn-md"
        type="button"
        @click="emit('cancel')"
        name="cancel"
      >
      Отмена
      </button>
    </BtnGroup>
  </form>
</template>
