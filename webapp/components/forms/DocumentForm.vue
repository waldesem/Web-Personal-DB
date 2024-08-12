<script setup lang="ts">
import { toRef } from "vue";
import { stateAnketa, stateClassify } from "@/state/state";
import type { Document } from "@/utils/interfaces";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  docs: {
    type: Object as () => Document,
    default: <Document>({}),
  },
});

const anketaState = stateAnketa();
const classifyState = stateClassify();

const docForm = toRef(props.docs as Document);

function submitDocument() {
  anketaState.updateItem("documents", docForm.value)
  emit('cancel');
  Object.keys(docForm.value).forEach(
    (key) => delete docForm.value[key as keyof typeof docForm.value]
  );
}
</script>

<template>
  <UForm :state="docForm" @submit.prevent="submitDocument">
    <UFormGroup class="mb-3" label="Вид документа" required>
      <USelect
        v-model="docForm['view']"
        :options="Object.values(classifyState.classes.value.documents)"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Серия документа" required>
      <UInput
        v-model="docForm['series']"
        placeholder="Серия документа"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Номер документа" required>
      <UInput
        v-model="docForm['digits']"
        placeholder="Номер документа"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Кем выдан" required>
      <UInput
        v-model="docForm['agency']"
        placeholder="Кем выдан"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Дата выдачи" required>
      <UInput
        v-model="docForm['issue']"
        type="date"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </UForm>
</template>
