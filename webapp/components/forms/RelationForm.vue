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
  <form
    @submit.prevent="submitRelation"
    class="form form-check"
  >
    <ElementsLabelSlot :label="'Тип связи'">
      <ElementsSelectDiv
          :name="'relation'"
          :need="true"
          :select="classifyState.classes.value.relations"
          v-model="relationForm['relation']"
        />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'ID связи'">
      <ElementsInputElement
        :typeof="'number'"
        :name="'relation_id'"
        :place="'ID связи'"
        :need="true"
        v-model="relationForm['relation_id']"
      />
    </ElementsLabelSlot>
    <ElementsBtnGroup @cancel="emit('cancel')"/>
  </form>
</template>
