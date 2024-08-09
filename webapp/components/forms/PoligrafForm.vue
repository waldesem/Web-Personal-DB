<script setup lang="ts">
import { toRef } from "vue";
import { stateAnketa, stateClassify } from "@/state/state";
import type { Pfo } from "@/utils/interfaces";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  poligraf: {
    type: Object as () => Pfo,
    default: <Pfo>({}),
  },
});

const anketaState = stateAnketa();
const classifyState = stateClassify();

const poligrafForm = toRef(props.poligraf as Pfo);

function submitPoligraf() {
  anketaState.updateItem("poligrafs", poligrafForm.value)
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
  >
    <ElementsLabelSlot :label="'Тема проверки'">
      <ElementsSelectDiv
        :name="'theme'"
        :need="true"
        :select="classifyState.classes.value.poligrafs"
        v-model="poligrafForm['theme']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Результат'">
      <ElementsTextArea
        :name="'results'"
        :place="'Результат'"
        v-model="poligrafForm['results']"
      >
      </ElementsTextArea>
    </ElementsLabelSlot>
    <ElementsBtnGroup @cancel="emit('cancel')"/>
  </form>
</template>
