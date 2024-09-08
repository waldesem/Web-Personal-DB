<script setup lang="ts">
import { toRef } from "vue";
import { stateClassify } from "@/state/state";
import type { Pfo } from "@/utils/interfaces";

const emit = defineEmits(["cancel", "submit"]);

const props = defineProps({
  poligraf: {
    type: Object as () => Pfo,
    default: {} as Pfo,
  },
});

const classifyState = stateClassify();

const poligrafForm = toRef(props.poligraf as Pfo);

function submitPoligraf() {
  emit('submit', poligrafForm.value);
  cancelAction();
}

function cancelAction() {
  emit('cancel');
  Object.assign(poligrafForm.value, {
    theme: "",
    results: "",
  } as Pfo);
}
</script>

<template>
  <UForm :state="poligrafForm" @submit.prevent="submitPoligraf">
    <UFormGroup class="mb-3" label="Тема проверки">
      <USelect
        v-model="poligrafForm['theme']"
        required
        :options="Object.values(classifyState.classes.value.poligrafs)"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Результат">
      <UTextarea
        v-model.trim.lazy="poligrafForm['results']"
        required
        placeholder="Результат"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelAction"/>
  </UForm>
</template>
