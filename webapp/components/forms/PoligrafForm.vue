<script setup lang="ts">
import { toRef } from "vue";
import { stateAnketa, stateClassify } from "@/state/state";
import type { Pfo } from "@/utils/interfaces";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  poligraf: {
    type: Object as () => Pfo,
    default: {} as Pfo,
  },
});

const anketaState = stateAnketa();
const classifyState = stateClassify();

const poligrafForm = toRef(props.poligraf as Pfo);

function submitPoligraf() {
  anketaState.updateItem("poligrafs", poligrafForm.value)
  emit('cancel');
  poligrafForm.value = {} as Pfo
}
</script>

<template>
  <UForm :state="poligrafForm" @submit.prevent="submitPoligraf">
    <UFormGroup class="mb-3" label="Тема проверки" required>
      <USelect
        v-model="poligrafForm['theme']"
        :options="Object.values(classifyState.classes.value.poligrafs)"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Результат" required>
      <UTextarea
        v-model="poligrafForm['results']"
        placeholder="Результат"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="emit('cancel')"/>
  </UForm>
</template>
