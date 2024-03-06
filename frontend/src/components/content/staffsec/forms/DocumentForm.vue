<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { Document } from "@/interfaces/interface";

const InputLabel = defineAsyncComponent(
  () => import("@components/elements/InputLabel.vue")
);
const SelectDiv = defineAsyncComponent(
  () => import("@components/elements/SelectDiv.vue")
);
const BtnGroupForm = defineAsyncComponent(
  () => import("@components/elements/BtnGroupForm.vue")
);

const emit = defineEmits(["submit"]);

const props = defineProps({
  docs: {
    type: Object as () => Record<string, any>,
    default: () => {},
  },
});

const docForm = ref({
  form: <Document>{},
  selected_item: {
    passport: "Паспорт гражданина России",
    foreign: "Иностранный докумен",
    others: "Другое",
  },

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
    @submit.prevent="docForm.updateItem"
    class="form form-check"
    role="form"
  >
    <SelectDiv
      :name="'view'"
      :label="'Выбрать'"
      :select="docForm.selected_item"
      :model="props.docs['view']"
      @input-event="docForm.form['view'] = $event.target.value"
    />
    <InputLabel
      :name="'series'"
      :label="'Серия документа'"
      :model="props.docs['series']"
      @input-event="
        docForm.form['series'] = $event.target.value
      "
    />
    <InputLabel
      :name="'number'"
      :label="'Номер документа'"
      :need="true"
      :model="props.docs['number']"
      @input-event="
        docForm.form['number'] = $event.target.value
      "
    />
    <InputLabel
      :name="'agency'"
      :label="'Орган выдавший'"
      :model="props.docs['agency']"
      @input-event="
        docForm.form['agency'] = $event.target.value
      "
    />
    <InputLabel
      :name="'issue'"
      :label="'Дата выдачи'"
      :typeof="'date'"
      :model="props.docs['issue']"
      @input-event="
        docForm.form['issue'] = $event.target.value
      "
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
