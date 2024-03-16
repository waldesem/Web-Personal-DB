<script setup lang="ts">
import { defineAsyncComponent, computed } from "vue";
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

const docForm = computed(() => {
  return props.docs as Document;
});

const selected_item = {
  "Паспорт гражданина России": "Паспорт гражданина России",
  "Иностранный докумен": "Иностранный докумен",
  "Другое": "Другое",
};
</script>

<template>
  <form
    @submit.prevent="emit('submit', docForm)"
    class="form form-check"
    role="form"
  >
    <SelectDiv
      :name="'view'"
      :label="'Выбрать'"
      :select="selected_item"
      v-model="docForm['view']"
    />
    <InputLabel
      :name="'series'"
      :label="'Серия документа'"
      v-model="docForm['series']"
    />
    <InputLabel
      :name="'number'"
      :label="'Номер документа'"
      :need="true"
      v-model="docForm['number']"
    />
    <InputLabel
      :name="'agency'"
      :label="'Орган выдавший'"
      v-model="docForm['agency']"
    />
    <InputLabel
      :name="'issue'"
      :label="'Дата выдачи'"
      :typeof="'date'"
      v-model="docForm['issue']"
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
