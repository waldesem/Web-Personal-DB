<script setup lang="ts">
import { toRef } from "vue";
import { stateAnketa, stateClassify } from "@/state/state";
import type { Relation } from "@/utils/interfaces";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  relation: {
    type: Object as () => Relation,
    default: <Relation>({}),
  },
});

const anketaState = stateAnketa();
const classifyState = stateClassify();

const relationForm = toRef(props.relation as Relation);

function submitRelation() {
  anketaState.updateItem("relations", relationForm.value)
  emit('cancel');
  Object.keys(relationForm.value).forEach(
    (key) => delete relationForm.value[key as keyof typeof relationForm.value]
  );
}
</script>

<template>
  <UForm :state="relationForm" @submit.prevent="submitRelation">
    <UFormGroup class="mb-3" label="Тип связи" required>
      <USelect
        v-model="relationForm['relation']"
        :options="Object.values(classifyState.classes.value.relations)"
      />
    </UFormGroup>
    <UFormGroup class="mb-3" label="ID связи" required>
      <UInput
        v-model="relationForm['relation_id']"
        placeholder="ID связи"
        type="number"
      />
    </UFormGroup>
    <ElementsBtnGroup @cancel="emit('cancel')"/>
  </UForm>
</template>
