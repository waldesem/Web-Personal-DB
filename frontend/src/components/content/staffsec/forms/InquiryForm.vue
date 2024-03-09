<script setup lang="ts">
import { ref, defineAsyncComponent } from "vue";
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

const emit = defineEmits(["submit"]);

const props = defineProps({
  inquiry: {
    type: Object as () => Needs,
    default: {},
  },
});

const inquiryForm = ref({
  form: <Needs>{},
  });

function updateItem() {
  emit("submit", inquiryForm.value.form);
  Object.keys(inquiryForm.value.form).forEach((key) => {
    delete inquiryForm.value.form[key as keyof typeof inquiryForm.value.form];
  });
};
</script>

<template>
  <form
    @submit.prevent="updateItem"
    class="form form-check"
    role="form"
  >
    <TextLabel
      :name="'info'"
      :label="'Информация'"
      :model="props.inquiry['info']"
      @input-event="inquiryForm.form['info'] = $event.target.value"
    />
    <InputLabel
      :name="'initiator'"
      :label="'Инициатор'"
      :model="props.inquiry['initiator']"
      @input-event="inquiryForm.form['initiator'] = $event.target.value"
    />
    <InputLabel
      :name="'source'"
      :label="'Источник'"
      :model="props.inquiry['source']"
      @input-event="inquiryForm.form['source'] = $event.target.value"
    />
    <BtnGroup>
      <button
        class="btn btn-outline-primary btn-md"
        data-bs-dismiss="modal"
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
    </BtnGroup>
  </form>
</template>
