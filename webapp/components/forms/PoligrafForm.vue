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
  <UForm @submit.prevent="submitPoligraf">
    <UFormGroup class="mb-3" size="md" label="Тема проверки" required>
      <USelect
        v-model="poligrafForm['theme']"
        :options="classifyState.classes.value.poligrafs"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" size="md" label="Результат" required>
      <UTextarea
        v-model="poligrafForm['results']"
        placeholder="Результат"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="emit('cancel')"/>
  </UForm>
</template>
