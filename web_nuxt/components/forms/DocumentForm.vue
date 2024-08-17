<script setup lang="ts">
import { toRef } from "vue";
import { stateAnketa, stateClassify } from "@/state/state";
import type { Document } from "@/utils/interfaces";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  docs: {
    type: Object as () => Document,
    default: {} as Document,
  },
});

const anketaState = stateAnketa();
const classifyState = stateClassify();

const docForm = toRef(props.docs as Document);

function submitDocument() {
  anketaState.updateItem("documents", docForm.value)
  emit('cancel');
  docForm.value = {} as Document
}
</script>

<template>
  <UForm :state="docForm" @submit.prevent="submitDocument">
    <UFormGroup class="mb-3" label="Вид документа">
      <USelect
        v-model="docForm['view']"
        required
        :options="Object.values(classifyState.classes.value.documents)"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Серия документа">
      <UInput
        v-model="docForm['series']"
        placeholder="Серия документа"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Номер документа">
      <UInput
        v-model="docForm['digits']"
        required
        placeholder="Номер документа"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Кем выдан">
      <UInput
        v-model="docForm['agency']"
        placeholder="Кем выдан"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Дата выдачи">
      <UInput
        v-model="docForm['issue']"
        type="date"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
