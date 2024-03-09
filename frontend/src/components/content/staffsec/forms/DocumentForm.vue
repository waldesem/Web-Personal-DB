<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { Document } from "@/interfaces/interface";

const InputLabel = defineAsyncComponent(
  () => import("@components/elements/InputLabel.vue")
);
const SelectDiv = defineAsyncComponent(
  () => import("@components/elements/SelectDiv.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/elements/BtnGroup.vue")
);

const emit = defineEmits(["submit"]);

const props = defineProps({
  docs: {
    type: Object as () => Document,
    default: {},
  },
});

const docForm = ref({
  form: <Document>{},
  selected_item: {
    "Паспорт гражданина России": "Паспорт гражданина России",
    "Иностранный докумен": "Иностранный докумен",
    "Другое": "Другое",
  }
});

function updateItem() {
  emit("submit", docForm.value.form);
  Object.keys(docForm.value.form).forEach((key) => {
    delete docForm.value.form[key as keyof typeof docForm.value.form];
  });
};
</script>

<template>
  <form
    @submit.prevent="updateItem"
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
