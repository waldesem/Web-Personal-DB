<script setup lang="ts">
import { defineAsyncComponent, toRef } from "vue";
import { Pfo } from "@/interfaces";
import { clearForm } from "@/utilities";
import { stateClassify } from "@/state";

const TextArea = defineAsyncComponent(
  () => import("@components/content/elements/TextArea.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);
const SelectObject = defineAsyncComponent(
  () => import("@components/content/elements/SelectObject.vue")
);
const BtnGroupContent = defineAsyncComponent(
  () => import("@components/content/elements/GroupContent.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);

const emit = defineEmits(["submit", "cancel"]);

const props = defineProps({
  poligraf: {
    type: Object as () => Pfo,
    default: {},
  },
  action: {
    type: String,
    default: "create",
  },
});

const poligrafForm = toRef(props.poligraf as Pfo);
</script>

<template>
  <form
    @submit.prevent="
      emit('submit', poligrafForm, props.action);
      clearForm(poligrafForm);
    "
    class="form form-check p-3"
    role="form"
  >
    <LabelSlot :label="'Тема проверки'">
      <SelectObject
        :name="'theme'"
        :select="stateClassify.poligrafs"
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
    <BtnGroup>
      <BtnGroupContent @cancel="emit('cancel')"/>
    </BtnGroup>
  </form>
</template>
