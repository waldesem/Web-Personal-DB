<script setup lang="ts">
import { computed, defineAsyncComponent } from "vue";
import { Needs } from "@/interfaces/interface";

const TextLabel = defineAsyncComponent(
  () => import("@components/elements/TextLabel.vue")
);
const InputLabel = defineAsyncComponent(
  () => import("@components/elements/InputLabel.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/elements/BtnGroup.vue")
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
    <TextLabel
      :name="'info'"
      :label="'Информация'"
      v-model="inquiryForm['info']"
    />
    <InputLabel
      :name="'initiator'"
      :label="'Инициатор'"
      v-model="inquiryForm['initiator']"
    />
    <InputLabel
      :name="'source'"
      :label="'Источник'"
      v-model="inquiryForm['source']"
    />
    <BtnGroup>
      <button
        class="btn btn-outline-primary btn-md"
        name="submit"
        type="submit"
      >
        Принять
      </button>
      <button 
        class="btn btn-outline-secondary btn-md"
        name="reset" 
        type="reset"
      >
        Очистить
      </button>
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
