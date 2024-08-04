<script setup lang="ts">
import { defineAsyncComponent, toRef } from "vue";
import { Relation } from "@/interfaces";
import { stateClassify, stateAnketa } from "@/state"

const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
)
const SelectDiv = defineAsyncComponent(
  () => import("@components/content/elements/SelectDiv.vue")
);
const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);

const emit = defineEmits(["cancel"]);

const props = defineProps({
  relation: {
    type: Object as () => Relation,
    default: {},
  },
});

const relationForm = toRef(props.relation as Relation);

function submitRelation() {
  stateAnketa.updateItem("relations", relationForm.value)
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
    role="form"
  >
    <LabelSlot :label="'Тип связи'">
      <SelectDiv
          :name="'relation'"
          :need="true"
          :select="stateClassify.classes.relations"
          v-model="relationForm['relation']"
        />
    </LabelSlot>
    <LabelSlot :label="'ID связи'">
      <InputElement
        :typeof="'number'"
        :name="'relation_id'"
        :place="'ID связи'"
        :need="true"
        v-model="relationForm['relation_id']"
      />
    </LabelSlot>
    <BtnGroup @cancel="emit('cancel')"/>
  </form>
</template>
