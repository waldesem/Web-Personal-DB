<script setup lang="ts">
import { toRef } from "vue";
import { stateClassify } from "@/state/state";
import type { Document } from "@/utils/interfaces";

const emit = defineEmits(["cancel", "submit"]);

const props = defineProps({
  docs: {
    type: Object as () => Document,
    default: {} as Document,
  },
});

const classifyState = stateClassify();

const docForm = toRef(props.docs as Document);
docForm.value.issue = docForm.value.issue
  ? new Date(docForm.value.issue).toISOString().slice(0, 10)
  : "";

function submitDocument() {
  emit("submit", docForm.value);
  cancelAction();
}

function cancelAction() {
  emit("cancel");
  Object.assign(docForm.value, {
    view: "",
    series: "",
    digits: "",
    agency: "",
    issue: "",
  } as Document);
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
      <UInput v-model.trim.lazy="docForm['series']" placeholder="Серия документа" />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Номер документа">
      <UInput
        v-model.trim.lazy="docForm['digits']"
        required
        placeholder="Номер документа"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Кем выдан">
      <UInput v-model.trim.lazy="docForm['agency']" placeholder="Кем выдан" />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Дата выдачи">
      <UInput v-model.trim.lazy="docForm['issue']" type="date" />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelAction" />
  </UForm>
</template>
