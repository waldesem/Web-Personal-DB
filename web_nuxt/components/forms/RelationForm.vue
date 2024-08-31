<script setup lang="ts">
import { toRef } from "vue";
import { stateAnketa, stateClassify } from "@/state/state";
import type { Relation } from "@/utils/interfaces";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  relation: {
    type: Object as () => Relation,
    default: {} as Relation,
  },
});

const anketaState = stateAnketa();
const classifyState = stateClassify();

const relationForm = toRef(props.relation as Relation);

function submitRelation() {
  anketaState.updateItem("relations", relationForm.value)
  emit('cancel');
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
    <ElementsBtnGroup @cancel="emit('cancel')"/>
  </UForm>
</template>
