<script setup lang="ts">
import { defineAsyncComponent, computed } from "vue";
import { Document } from "@/interfaces/interface";

const InputLabel = defineAsyncComponent(
  () => import("@components/content/elements/InputLabel.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
)
const SelectInput = defineAsyncComponent(
  () => import("@components/content/elements/SelectInput.vue")
);
const BtnGroupContent = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroupContent.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
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

const selected_item = [
  "Паспорт гражданина России",
  "Иностранный докумен",
  "Другое",
];
</script>

<template>
  <form
    @submit.prevent="emit('submit', docForm)"
    class="form form-check"
    role="form"
  >
    <LabelSlot :label="'Вид документа'">
      <SelectInput
        :name="'view'"
        :select="selected_item"
        v-model="docForm['view']"
      />
    </LabelSlot>
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
      <BtnGroupContent/>
    </BtnGroup>
  </form>
</template>
