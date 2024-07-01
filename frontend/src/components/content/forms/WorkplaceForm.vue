<script setup lang="ts">
import { defineAsyncComponent, toRef } from "vue";
import { Work } from "@/interfaces";
import { stateAnketa } from "@/state";

const SwitchBox = defineAsyncComponent(
  () => import("@components/content/elements/SwitchBox.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
)
const InputElement = defineAsyncComponent(
  () => import("@components/content/elements/InputElement.vue")
);
const BtnGroup = defineAsyncComponent(
  () => import("@components/content/elements/BtnGroup.vue")
);

const emit = defineEmits(["cancel"]);

const props = defineProps({
  work: {
    type: Object as () => Work,
    default: {},
  },
});

const workForm = toRef(props.work as Work);

function submitWorkplace() {
  stateAnketa.updateItem("workplaces", workForm.value)
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
    role="form"
  > 
    <LabelSlot :label="'Текущая работа'">
    <SwitchBox
        :name="'now_work'"
        :place="'Текущая работа'"
        v-model="workForm['now_work']"
      />
    </LabelSlot>
    <LabelSlot :label="'Начало работы'">
      <InputElement
        :name="'start_date'"
        :need="true"
        :place="'Начало работы'"
        :typeof="'date'"
        v-model="workForm['started']"
      />
    </LabelSlot>
    <LabelSlot
      v-if="!workForm['now_work']" 
      :label="'Окончание работы'">
      <InputElement
        :name="'end_date'"
        :place="'Окончание работы'"
        :typeof="'date'"
        v-model="workForm['finished']"
      />
    </LabelSlot>
    <LabelSlot :label="'Место работы'">
      <InputElement
        :name="'workplace'"
        :place="'Место работы'"
        :need="true"
        v-model="workForm['workplace']"
      />
    </LabelSlot>
    <LabelSlot :label="'Должность'">
      <InputElement
        :name="'position'"
        :place="'Должность'"
        :need="true"
        v-model="workForm['position']"
      />
    </LabelSlot>
    <LabelSlot :label="'Адрес организации'">
      <InputElement
        :name="'address'"
        :place="'Адрес организации'"
        v-model="workForm['address']"
      />
    </LabelSlot>
    <LabelSlot :label="'Причина увольнения'">
      <InputElement
        :name="'reason'"
        :place="'Причина увольнения'"
        v-model="workForm['reason']"
      />
    </LabelSlot>
    <BtnGroup @cancel="emit('cancel')" />
  </form>
</template>
