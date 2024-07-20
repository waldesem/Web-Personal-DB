<script setup lang="ts">
import { defineAsyncComponent, toRef } from "vue";
import { Pfo } from "@/interfaces";
import { stateClassify, stateAnketa } from "@/state";

const TextArea = defineAsyncComponent(
  () => import("@components/content/elements/TextArea.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);
const SelectDiv = defineAsyncComponent(
  () => import("@components/content/elements/SelectDiv.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);

const emit = defineEmits(["cancel"]);

const props = defineProps({
  poligraf: {
    type: Object as () => Pfo,
    default: {},
  },
});

const poligrafForm = toRef(props.poligraf as Pfo);

function submitPoligraf() {
  stateAnketa.updateItem("poligrafs", poligrafForm.value)
  emit('cancel');
  Object.keys(poligrafForm.value).forEach(
    (key) => delete poligrafForm.value[key as keyof typeof poligrafForm.value]
  );
}
</script>

<template>
  <form
    @submit.prevent="submitPoligraf"
    class="form form-check p-3"
    role="form"
  >
    <LabelSlot :label="'Тема проверки'">
      <SelectDiv
        :name="'theme'"
        :need="true"
        :select="stateClassify.classes.poligrafs"
        v-model="poligrafForm['theme']"
      />
    </LabelSlot>
    <LabelSlot :label="'Результат'">
      <TextArea
        :name="'results'"
        :place="'Результат'"
        v-model="poligrafForm['results']"
      >
      </TextArea>
    </LabelSlot>
    <BtnGroup @cancel="emit('cancel')"/>
  </form>
</template>
