<script setup lang="ts">
import { computed, defineAsyncComponent } from "vue";
import { Inquisition } from "@/interfaces/interface";

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
    <InputElement
      :name="'theme'"
      :label="'Тема проверки'"
      :need="true"
      v-model="investigationForm['theme']"
    />
    <TextArea
      :name="'info'"
      :label="'Информация'"
      v-model="props.investigation['info']"
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
