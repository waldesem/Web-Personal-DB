<script setup lang="ts">
import { ref, defineAsyncComponent } from "vue";
import { Needs } from "@/interfaces/interface";

const TextLabel = defineAsyncComponent(
  () => import("@components/elements/TextLabel.vue")
);
const InputLabel = defineAsyncComponent(
  () => import("@components/elements/InputLabel.vue")
);
const BtnGroupForm = defineAsyncComponent(
  () => import("@components/elements/BtnGroupForm.vue")
);

const emit = defineEmits(["submit"]);

const props = defineProps({
  inquiry: {
    type: Object as () => Record<string, any>,
    default: () => {},
  },
});

const inquiryForm = ref({
  form: <Needs>{},

  updateItem: function () {
    emit("submit", this.form);
    Object.keys(this.form).forEach((key) => {
      delete this.form[key as keyof typeof this.form];
    });
  },
});
</script>

<template>
  <form
    @submit.prevent="inquiryForm.updateItem"
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
    <BtnGroupForm :cls="false">
      <button
        class="btn btn-outline-success btn-md"
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
    </BtnGroupForm>
  </form>
</template>
