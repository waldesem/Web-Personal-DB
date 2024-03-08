<script setup lang="ts">
import { ref, defineAsyncComponent } from "vue";
import { Inquisition } from "@/interfaces/interface";

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
  investigation: {
    type: Object as () => Inquisition,
    default: {},
  },
});

const investigationForm = ref({
  form: <Inquisition>{},
  });

function updateItem() {
  emit("submit", investigationForm.value.form);
  Object.keys(investigationForm.value.form).forEach((key) => {
    delete investigationForm.value.form[key as keyof typeof investigationForm.value.form];
  });
};
</script>

<template>
  <form
    @submit.prevent="updateItem"
    class="form form-check"
    role="form"
  >
    <InputLabel
      :name="'theme'"
      :label="'Тема проверки'"
      :need="true"
      :model="props.investigation['theme']"
      @input-event="
        investigationForm.form['theme'] = $event.target.value
      "
    />
    <TextLabel
      :name="'info'"
      :label="'Информация'"
      :model="props.investigation['info']"
      @input-event="investigationForm.form['info'] = $event.target.value"
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
    </BtnGroup>
  </form>
</template>
