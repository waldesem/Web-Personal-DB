<script setup lang="ts">
import type { Document } from "@/types/interfaces";
import { useDateFormat } from "@vueuse/core";

const emit = defineEmits(["cancel", "update"]);

const props = defineProps({
  docs: {
    type: Object as () => Document,
    default: {} as Document,
  },
  candId: {
    type: String,
    default: "",
  },
});

const docForm = toRef(props.docs as Document);
docForm.value.issue = docForm.value.issue
  ? useDateFormat(docForm.value.issue, "YYYY-MM-DD").value 
  : "";

function submitDocument() {
  emit("update", docForm.value);
  clearForm();
}

function cancelAction() {
  emit('cancel');
  clearForm();
}

function clearForm() {
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
        :options="['Паспорт', 'Иностарнный паспорт', 'Другое']"
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
      <UInput v-model.trim="docForm['agency']" placeholder="Кем выдан" />
    </UFormGroup>
    <UFormGroup class="mb-3" label="Дата выдачи">
      <UInput 
        v-model.trim.lazy="docForm['issue']" 
        required
        type="date" 
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelAction" />
  </UForm>
</template>
