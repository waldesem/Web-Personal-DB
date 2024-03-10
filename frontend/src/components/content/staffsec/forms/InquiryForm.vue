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

const emit = defineEmits(["submit", "cancel"]);

const props = defineProps({
  inquiry: {
    type: Object as () => Needs,
    default: {},
  },
});

const inquiryForm = ref({
  form: <Needs>{},
  });
</script>

<template>
  <form
    @submit.prevent="emit('submit', inquiryForm.form)"
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
