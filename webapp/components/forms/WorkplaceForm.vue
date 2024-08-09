<script setup lang="ts">
import { toRef } from "vue";
import { stateAnketa } from "@/state/state";
import type { Work } from "@/utils/interfaces";

const emit = defineEmits(["cancel"]);

const props = defineProps({
  work: {
    type: Object as () => Work,
    default: <Work>({}),
  },
});

const anketaState = stateAnketa();

const workForm = toRef(props.work as Work);

function submitWorkplace() {
  anketaState.updateItem("workplaces", workForm.value)
  emit('cancel');
  Object.keys(workForm.value).forEach(
    (key) => delete workForm.value[key as keyof typeof workForm.value]
  );
}
</script>

<template>
  <form
    @submit.prevent="submitWorkplace"
    class="form form-check"
  > 
    <ElementsLabelSlot :label="'Текущая работа'">
    <ElementsSwitchBox
        :name="'now_work'"
        v-model="workForm['now_work']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Начало работы'">
      <ElementsInputElement
        :name="'start_date'"
        :need="true"
        :place="'Начало работы'"
        :typeof="'date'"
        v-model="workForm['starts']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot
      v-if="!workForm['now_work']" 
      :label="'Окончание работы'">
      <ElementsInputElement
        :name="'end_date'"
        :place="'Окончание работы'"
        :typeof="'date'"
        v-model="workForm['finished']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Место работы'">
      <ElementsInputElement
        :name="'workplace'"
        :place="'Место работы'"
        :need="true"
        v-model="workForm['workplace']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Должность'">
      <ElementsInputElement
        :name="'position'"
        :place="'Должность'"
        :need="true"
        v-model="workForm['position']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Адрес организации'">
      <ElementsInputElement
        :name="'address'"
        :place="'Адрес организации'"
        v-model="workForm['addresses']"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Причина увольнения'">
      <ElementsInputElement
        :name="'reason'"
        :place="'Причина увольнения'"
        v-model="workForm['reason']"
      />
    </ElementsLabelSlot>
    <ElementsBtnGroup @cancel="emit('cancel')" />
  </form>
</template>
