<script setup lang="ts">
import { ref, defineAsyncComponent } from "vue";
import { Inquisition } from "@/interfaces/interface";

const TextLabel = defineAsyncComponent(
  () => import("@components/elements/TextLabel.vue")
);
const BtnGroupForm = defineAsyncComponent(
  () => import("@components/elements/BtnGroupForm.vue")
);

const emit = defineEmits(["submit"]);

const props = defineProps({
  investigation: {
    type: Object as () => Record<string, any>,
    default: () => {},
  },
});

const investigationForm = ref({
  form: <Inquisition>{},

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
    @submit.prevent="investigationForm.updateItem"
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
