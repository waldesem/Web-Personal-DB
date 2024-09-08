<script setup lang="ts">
import { toRef } from "vue";
import { stateClassify } from "@/state/state";
import type { Relation } from "@/utils/interfaces";

const emit = defineEmits(["cancel", "submit"]);

const props = defineProps({
  relation: {
    type: Object as () => Relation,
    default: {} as Relation,
  },
});

const classifyState = stateClassify();

const relationForm = toRef(props.relation as Relation);

function submitRelation() {
  emit("submit", relationForm.value);
  clearForm();
}

function cancelAction() {
  emit('cancel');
  clearForm();
}

function clearForm() {
  Object.assign(relationForm.value, {
    relation: "",
    relation_id: "",
  } as Relation);
}
</script>

<template>
  <UForm :state="relationForm" @submit.prevent="submitRelation">
    <UFormGroup class="mb-3" label="Тип связи">
      <USelect
        v-model.trim.lazy="relationForm['relation']"
        required
        :options="Object.values(classifyState.classes.value.relations)"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="ID связи">
      <UInput
        v-model.trim.lazy="relationForm['relation_id']"
        required
        type="number"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="cancelAction"/>
  </UForm>
</template>
