<script setup lang="ts">
import { defineAsyncComponent, toRef } from "vue";
import { Document } from "@/interfaces";

const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
)
const SelectArray = defineAsyncComponent(
  () => import("@components/content/elements/SelectArray.vue")
);
const BtnGroupContent = defineAsyncComponent(
  () => import("@components/content/elements/GroupContent.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);

const emit = defineEmits(["submit", "cancel"]);

const props = defineProps({
  docs: {
    type: Object as () => Document,
    default: {},
  },
});

const docForm = toRef(props.docs as Document);

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
      <SelectArray
        :name="'view'"
        :select="selected_item"
        v-model="docForm['view']"
      />
    </LabelSlot>
    <LabelSlot :label="'Серия документа'">
      <InputElement
        :name="'series'"
        :place="'Серия документа'"
        v-model="docForm['series']"
      />
    </LabelSlot>
    <LabelSlot :label="'Номер документа'">
      <InputElement
        :name="'number'"
        :place="'Номер документа'"
        :need="true"
        v-model="docForm['number']"
      />
    </LabelSlot>
    <LabelSlot :label="'Кем выдан'">
      <InputElement
        :name="'agency'"
        :place="'Орган выдавший'"
        v-model="docForm['agency']"
      />
    </LabelSlot>
    <LabelSlot :label="'Дата выдачи'">
      <InputElement
        :name="'issue'"
        :place="'Дата выдачи'"
        :typeof="'date'"
        v-model="docForm['issue']"
      />
    </LabelSlot>
    <BtnGroup>
      <BtnGroupContent
        @cancel="emit('cancel')"
      />
    </BtnGroup>
  </form>
</template>
